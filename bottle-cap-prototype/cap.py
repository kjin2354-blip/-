"""
Push-to-open powder cap with a cross-blade cutter. Prototype for 3D printing.

Run:   python cap.py            (needs: pip install cadquery)
Out:   out/*.stl  (one per part, for the slicer)
       out/cap_assembly.step  (all parts in place, for CAD tools and manufacturers)

All dimensions are millimetres. z = 0 is the top rim of the bottle neck when the cap
is screwed fully on. Change the settings below, re-run, re-print.

How it works
  - The body screws onto the bottle like a normal cap and seals on the neck bore.
  - Powder sits in the chamber on top of a foil disc stuck to the flat ring around
    the floor opening.
  - Pressing the head drives a cross (X) blade down. Its slanted edges puncture the
    foil at the centre first, then cut outward, leaving four triangular flaps that
    fold down and stay attached.
  - The head bottoms out on the lid, which sets the stroke. The C-clip under the head
    stops accidental presses until it is pulled off.
"""
import math
import os
import cadquery as cq

# ---------------------------------------------------------------- settings ----
# Fit: gap between parts that slide (shaft in lid). Resin ~0.15-0.2, FDM ~0.3-0.4.
CLEARANCE = 0.2
# Lid press fit into the chamber (radial, + = looser). Resin ~0.05, FDM ~0.15.
LID_FIT = 0.05

# Bottle neck: PCO 1881 standard (28 mm, used on Dasani and many Coca-Cola bottles).
# Neck thread: single start, 2.70 mm lead, 650 deg (~1.8 turns), starting 1.70 mm below
# the rim. The root diameter is provisional; check it against a real bottle.
NECK_THREAD_OD = 27.40  # outside diameter across the bottle's threads
NECK_THREAD_ROOT = 24.94  # diameter at the bottom of the bottle's thread grooves
NECK_BORE = 21.74       # inside diameter of the neck opening
THREAD_STARTS = 1       # number of separate thread ridges on the neck (look from the top)
THREAD_LEAD = 2.70      # how far one ridge rises in one full turn
THREAD_TURNS = 1.5      # how far around the cap's ridge runs (neck has ~1.8 turns)
THREAD_TOP = 1.2        # cap ridge centre line starts this far below the rim
THREAD_CLEAR = 0.3      # radial clearance on the threads

# Seal washer between the bottle rim and the cap (silicone or printed TPU).
# Printed caps rarely seal well plastic-on-plastic. Set WASHER_T = 0 to leave it out.
WASHER_ID, WASHER_OD = 22.2, 27.0
WASHER_T = 1.0          # washer thickness
WASHER_SQUEEZE = 0.3    # how much the washer is compressed when the cap is tight

# Cap body
WALL = 1.6
COLLAR_H = 10.0         # skirt depth: covers the 1881 thread zone (~8 mm below the rim)
CHAMBER_R = 18.0        # chamber inner radius (36 mm inside)
CHAMBER_H = 40.0        # floor-land to lid height; ~34 mL of powder space
OPENING_R = 9.5         # floor opening radius (19 mm). Keep below NECK_BORE/2.
LAND_R = 12.0           # flat ring around the opening where the foil sticks
FLOOR_T = 2.0
FUNNEL_TOP_Z = 8.0      # funnel meets chamber wall here (steeper = better flow)
SEAL_RING_H = 2.5       # plug-seal ring that pushes into the neck bore
SEAL_INTERFERENCE = 0.05

# Cutter
BLADE_R = 9.0           # blade reach from centre; X span = 2 * BLADE_R (18 mm)
BLADE_H = 9.0           # rise of the slanted edge; BLADE_H = BLADE_R gives 45 deg
BLADE_T = 0.9           # blade thickness. Resin 0.8-1.0, FDM 1.2+
FOIL_GAP = 3.0          # gap from blade tip to foil before pressing
OVERTRAVEL = 2.0        # how far the full blade width goes past the foil
SHAFT_R = 3.5
HEAD_R = 12.0
# Return spring (buy it, e.g. from a compression-spring assortment): sits around the shaft
# between the lid and the head, and lifts the blade back out of the opening after a press.
SPRING_OD = 11.0        # outside diameter (fits over the 7 mm shaft, inside the head cup)
SPRING_WIRE = 0.8
SPRING_FREE = 25.0      # free length
SPRING_COILS = 7        # solid length = coils x wire = 5.6 mm
CUP_DEPTH = 6.5         # pocket under the head that holds the spring when fully pressed
HEAD_PLATE = 4.0
HEAD_H = CUP_DEPTH + HEAD_PLATE
LID_T = 3.0
GUIDE_L = 8.0           # guide tube under the lid, keeps the plunger straight

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

# ------------------------------------------------------------- derived ----
CH_OUT = CHAMBER_R + WALL
COLLAR_IN = NECK_THREAD_OD / 2 + THREAD_CLEAR
COLLAR_OUT = COLLAR_IN + 2.2
LID_Z = FLOOR_T + CHAMBER_H              # underside of lid / top of chamber wall
STROKE = FOIL_GAP + BLADE_H + OVERTRAVEL
TIP_Z = FLOOR_T + FOIL_GAP               # blade tip at rest
BLADE_TOP = TIP_Z + BLADE_H + 3.0
HEAD_Z = LID_Z + LID_T + STROKE          # underside of head at rest
GUIDE_BOTTOM = LID_Z - GUIDE_L
STOP_TOP = GUIDE_BOTTOM - 0.5            # retention collar sits just under the guide
BORE_R = SHAFT_R + CLEARANCE
PEG_R, PEG_H = 2.5, 3.0

assert WASHER_T == 0 or WASHER_ID / 2 > NECK_BORE / 2 + SEAL_INTERFERENCE, "washer must sit outside the seal ring"
assert OPENING_R < NECK_BORE / 2 - 0.5, "floor opening must fit inside the neck bore"
assert BLADE_R < OPENING_R - 0.3, "blade must pass through the floor opening"
assert BLADE_TOP < STOP_TOP - 2, "blade and retention collar overlap"
assert CUP_DEPTH >= SPRING_COILS * SPRING_WIRE + 0.5, "spring would go solid before the head reaches the lid"
assert SPRING_FREE > STROKE + CUP_DEPTH, "spring needs preload at rest"


def revolve(points):
    """Revolve a closed (r, z) outline 360 degrees about the z axis."""
    return (cq.Workplane("XZ").polyline(points).close()
            .revolve(360, (0, 0, 0), (0, 1, 0)))


# ------------------------------------------------------------------ body ----
def make_cap_thread():
    """Internal thread ridge(s) of the cap, in place."""
    r_base, r_crest = COLLAR_IN + 0.2, NECK_THREAD_ROOT / 2 + THREAD_CLEAR
    w_base, w_crest = 1.4, 0.8
    r_mid = (r_base + r_crest) / 2
    height = THREAD_LEAD * THREAD_TURNS
    helix = cq.Wire.makeHelix(pitch=THREAD_LEAD, height=height, radius=r_mid)
    profile = (cq.Workplane("XZ")
               .polyline([(r_base, -w_base / 2), (r_crest, -w_crest / 2),
                          (r_crest, w_crest / 2), (r_base, w_base / 2)]).close())
    ridge = profile.sweep(cq.Workplane().add(helix), isFrenet=True)
    z0 = -(THREAD_TOP + height)
    out = None
    for i in range(THREAD_STARTS):
        r = ridge.rotate((0, 0, 0), (0, 0, 1), 360 / THREAD_STARTS * i).translate((0, 0, z0))
        out = r if out is None else out.union(r)
    return out


def make_body():
    seal_out = NECK_BORE / 2 + SEAL_INTERFERENCE
    seal_in = seal_out - 1.0
    outline = [
        (COLLAR_IN, -COLLAR_H),
        (COLLAR_OUT - 0.6, -COLLAR_H),
        (COLLAR_OUT, -COLLAR_H + 0.6),
        (COLLAR_OUT, 0.0),
        (CH_OUT, 1.5),
        (CH_OUT, LID_Z),
        (CHAMBER_R, LID_Z),
        (CHAMBER_R, FUNNEL_TOP_Z),
        (LAND_R, FLOOR_T),            # funnel down to the foil land
        (OPENING_R, FLOOR_T),         # flat land for the foil
        (OPENING_R, 0.0),
        (seal_in, 0.0),               # plug-seal ring into the neck bore
        (seal_in, -SEAL_RING_H),
        (seal_out - 0.4, -SEAL_RING_H),
        (seal_out, -SEAL_RING_H + 0.6),
        (seal_out, 0.0),
        (COLLAR_IN, 0.0),             # neck rim seats against this face
    ]
    body = revolve(outline)

    body = body.union(make_cap_thread())
    # pocket for the seal washer, in the face the bottle rim presses against
    if WASHER_T > 0:
        pocket = (cq.Workplane("XY").circle(WASHER_OD / 2 + 0.15).circle(WASHER_ID / 2 - 0.15)
                  .extrude(WASHER_T - WASHER_SQUEEZE))
        body = body.cut(pocket)
    # grip ribs on the outside of the collar
    for i in range(36):
        a = 360 / 36 * i
        rib = (cq.Workplane("XY").box(0.9, 1.2, COLLAR_H - 2.5)
               .translate((COLLAR_OUT + 0.3, 0, -COLLAR_H / 2 - 0.6))
               .rotate((0, 0, 0), (0, 0, 1), a))
        body = body.union(rib)
    return body


# ------------------------------------------------------------------- lid ----
def make_lid():
    skirt_out = CHAMBER_R - LID_FIT
    plate = revolve([
        (BORE_R, LID_Z), (CH_OUT, LID_Z), (CH_OUT, LID_Z + LID_T - 0.6),
        (CH_OUT - 0.6, LID_Z + LID_T), (BORE_R, LID_Z + LID_T)])
    skirt = revolve([
        (skirt_out - 1.5, LID_Z - 4.0), (skirt_out - 0.3, LID_Z - 4.0),
        (skirt_out, LID_Z - 3.7), (skirt_out, LID_Z), (skirt_out - 1.5, LID_Z)])
    guide = revolve([
        (BORE_R, GUIDE_BOTTOM), (BORE_R + 2.3, GUIDE_BOTTOM),
        (BORE_R + 2.3, LID_Z), (BORE_R, LID_Z)])
    return plate.union(skirt).union(guide)


# --------------------------------------------------------------- plunger ----
def make_plunger():
    top = BLADE_TOP
    v = [(-BLADE_R, TIP_Z + BLADE_H), (0, TIP_Z), (BLADE_R, TIP_Z + BLADE_H),
         (BLADE_R, top), (-BLADE_R, top)]
    blade = cq.Workplane("XZ").polyline(v).close().extrude(BLADE_T / 2, both=True)
    cross = blade.union(blade.rotate((0, 0, 0), (0, 0, 1), 90))
    hub = cq.Workplane("XY").circle(SHAFT_R + 0.5).extrude(top - (TIP_Z + BLADE_H) + 0.5)\
        .translate((0, 0, TIP_Z + BLADE_H - 0.5))
    shaft = cq.Workplane("XY").circle(SHAFT_R).extrude(HEAD_Z + CUP_DEPTH - top).translate((0, 0, top))
    stop = cq.Workplane("XY").circle(SHAFT_R + 2.0).extrude(1.5).translate((0, 0, STOP_TOP - 1.5))
    peg = cq.Workplane("XY").circle(PEG_R).extrude(PEG_H).translate((0, 0, HEAD_Z + CUP_DEPTH))
    return cross.union(hub).union(shaft).union(stop).union(peg)


def make_head():
    head = (cq.Workplane("XY").circle(HEAD_R).extrude(HEAD_H)
            .edges(">Z").chamfer(0.8).translate((0, 0, HEAD_Z)))
    cup = cq.Workplane("XY").circle(SPRING_OD / 2 + 0.6).extrude(CUP_DEPTH).translate((0, 0, HEAD_Z))
    socket = cq.Workplane("XY").circle(PEG_R + 0.02).extrude(PEG_H + 0.3).translate((0, 0, HEAD_Z + CUP_DEPTH))
    dimple = cq.Workplane("XY").sphere(30).translate((0, 0, HEAD_Z + HEAD_H + 29.4))
    return head.cut(cup).cut(socket).cut(dimple)


def make_clip():
    h = STROKE - 0.2
    # horseshoe around the spring; its arms flex to snap over the spring
    r_in = SPRING_OD / 2 + 0.4
    ring = (cq.Workplane("XY").circle(r_in + 3.6).circle(r_in).extrude(h)
            .translate((0, 0, LID_Z + LID_T + 0.1)))
    gap = cq.Workplane("XY").box(12, SPRING_OD - 0.6, h + 2).translate((6, 0, LID_Z + LID_T + h / 2))
    tab = cq.Workplane("XY").box(7, 6, 2.0).translate((-(r_in + 3.6 + 2.5), 0, LID_Z + LID_T + 0.1 + h / 2))
    return ring.cut(gap).union(tab)


def make_washer():
    return (cq.Workplane("XY").circle(WASHER_OD / 2).circle(WASHER_ID / 2).extrude(WASHER_T)
            .translate((0, 0, -WASHER_SQUEEZE)))


def make_spring(length=None):
    """Reference model of the bought spring at rest (not a print part)."""
    length = length or (STROKE + CUP_DEPTH)
    r = SPRING_OD / 2 - SPRING_WIRE / 2
    run = length - SPRING_WIRE - 0.02          # wire centre line, so the coil ends touch the seats
    helix = cq.Wire.makeHelix(pitch=run / SPRING_COILS, height=run, radius=r)
    wire = cq.Workplane("XZ").center(r, 0).circle(SPRING_WIRE / 2)
    return (wire.sweep(cq.Workplane().add(helix), isFrenet=True)
            .translate((0, 0, LID_Z + LID_T + SPRING_WIRE / 2 + 0.01)))


def pressed(shape):
    return shape.translate((0, 0, -STROKE))


def main():
    os.makedirs(OUT, exist_ok=True)
    parts = {
        "body": make_body(),
        "lid": make_lid(),
        "plunger": make_plunger(),
        "head": make_head(),
        "safety_clip": make_clip(),
    }
    if WASHER_T > 0:
        parts["washer"] = make_washer()
    for name, wp in parts.items():
        cq.exporters.export(wp, os.path.join(OUT, f"{name}.stl"), tolerance=0.01, angularTolerance=0.1)

    asm = cq.Assembly(name="powder_cap")
    colors = {"body": (0.93, 0.94, 0.95, 0.6), "lid": (0.93, 0.94, 0.95, 1), "plunger": (0.2, 0.2, 0.22, 1),
              "head": (0.08, 0.08, 0.09, 1), "safety_clip": (1.0, 0.42, 0.07, 1), "washer": (0.2, 0.5, 0.9, 1)}
    for name, wp in parts.items():
        asm.add(wp, name=name, color=cq.Color(*colors[name]))
    asm.add(make_spring(), name="spring_bought_part", color=cq.Color(0.6, 0.62, 0.65, 1))
    asm.save(os.path.join(OUT, "cap_assembly.step"))

    # pack the STLs for viewer.html (web/*.json); cap_thread is a highlight, not a print part
    import base64, json, struct
    web = os.path.join(os.path.dirname(OUT), "web")
    os.makedirs(web, exist_ok=True)
    cq.exporters.export(make_cap_thread(), os.path.join(OUT, "_cap_thread.stl"), tolerance=0.01, angularTolerance=0.1)
    for name in list(parts) + ["_cap_thread"]:
        d = open(os.path.join(OUT, f"{name}.stl"), "rb").read()
        n = struct.unpack("<I", d[80:84])[0]
        pos = b"".join(d[84 + 50 * i + 12: 84 + 50 * i + 48] for i in range(n))
        with open(os.path.join(web, f"{name.lstrip('_')}.json"), "w") as f:
            json.dump({"name": name, "triangles": n, "positions": base64.b64encode(pos).decode()}, f)
    os.remove(os.path.join(OUT, "_cap_thread.stl"))

    print(f"stroke {STROKE:.1f} mm | cap height {HEAD_Z + HEAD_H + COLLAR_H:.1f} mm "
          f"| chamber Ø{2*CHAMBER_R:.0f} mm | blade X span {2*BLADE_R:.0f} mm")
    return parts


if __name__ == "__main__":
    main()

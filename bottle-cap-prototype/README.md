# Cross-blade powder cap: printable prototype v1.1 (PCO 1881 / Dasani)

A screw-on bottle cap that stores pre-workout powder above a foil seal. Pressing the
head drives an X-shaped blade through the foil. The blade's slanted edges puncture the
centre first and then cut outward, so the foil opens as four flaps that stay attached.

## Files

| File | What it is |
|---|---|
| `cap.py` | Parametric CadQuery model. All dimensions are settings at the top. |
| `out/body.stl` | Collar with internal threads, neck seal ring, funnel floor, powder chamber |
| `out/lid.stl` | Press-fit lid with a guide tube for the plunger |
| `out/plunger.stl` | Shaft, retention collar and X blade |
| `out/head.stl` | Push button, presses onto the plunger peg |
| `out/safety_clip.stl` | C-clip under the head that blocks accidental presses |
| `out/washer.stl` | Seal washer, 22.2 × 27 × 1 mm. Print in TPU, or buy a silicone one |
| `out/cap_assembly.step` | All parts in place, for CAD tools and closure manufacturers |
| `viewer.html` | 3D viewer of the STL files with cutaway and press animation |

## Before printing

1. **Check the neck.** The thread is set to the PCO 1881 standard used on Dasani: thread
   OD 27.40 mm, root 24.94 mm, bore 21.74 mm, one start, 2.70 mm lead, 650° of thread
   starting 1.70 mm below the rim. A sealed Dasani cap should come off in about 1¾ turns.
   The root diameter is provisional; check it with calipers if you can. For a different
   bottle, change `NECK_THREAD_OD`, `NECK_THREAD_ROOT`, `NECK_BORE`, `THREAD_STARTS` and
   `THREAD_LEAD`.
2. Set fits for your printer. Defaults are for resin:
   `CLEARANCE = 0.2`, `LID_FIT = 0.05`, `BLADE_T = 0.9`.
   For filament (FDM) try `0.35`, `0.15` and `1.2`.
3. Regenerate:

   ```bash
   pip install cadquery
   python cap.py
   ```

## Print orientation

- **body**: upside down, chamber opening on the bed. The threads and funnel then print without supports.
- **lid**: top face on the bed.
- **plunger**: peg end down, blade tip up.
- **head**: dimpled top on the bed.
- **safety_clip**: flat.
- **washer**: flat, in TPU. A food-safe silicone washer (22 × 27 × 1 mm) works too.

## Assembly

1. Stick a disc of aluminium foil tape, about 24 mm across, on the flat ring around the
   floor opening inside the chamber. Press the edges down firmly.
2. Fill the chamber with powder (about 34 mL of space).
3. Push the plunger up through the lid from underneath, blade end down, then press the lid
   into the chamber.
4. Press the head onto the peg. Add a drop of glue if it's loose.
5. Drop the washer into the pocket under the cap, snap the safety clip around the shaft,
   and screw the cap onto a filled bottle.

## Tests

- **Press force**: stand the bottle on a kitchen scale and press. Peak reading in kg × 10 ≈ newtons.
  Aim for under 2–3 kg.
- **Opening**: do all four flaps fold clear, and does all the powder fall through?
- **Leaks**: screw on, turn upside down, squeeze the bottle.

## Known limits of v1

- The cap is 74 mm tall before pressing, because 34 mL of powder space and a 14 mm stroke
  both add height. A smaller dose (`CHAMBER_H`) or a steeper blade (`BLADE_H`) shortens it.
- No tamper band. The safety clip stands in for it in prototypes.
- The thread profile is a simple trapezoid, fine for test prints but not a production thread.
- Foil tape stands in for an induction-sealed foil. Production foil is laminated and may
  need more force to cut.

## Fit check (v1.1)

`cap.py`'s thread was checked against a modelled PCO 1881 neck (one right-hand thread,
2.70 mm lead, 650°, starting 1.70 mm below the rim) with the cap seated on a washer
compressed 0.3 mm. The threads nest with zero overlap; the only contact is the seal ring,
which presses 0.05 mm into the neck bore by design. This checks the model against the
published standard, not against a physical bottle.

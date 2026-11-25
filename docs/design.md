# Mechanical design — revision A

## Scope and requirements

The instrument is a passive research concept for low-frequency vibration event retention. It must not rely on electronics for the proposed sensing or indication function. The laboratory reference instrumentation may be electronic.

| ID | Research requirement | Evidence gate |
|---|---|---|
| R01 | Tune a single-axis channel to 25 Hz | Measured natural frequency within ±2% |
| R02 | Distinguish frequency and amplitude | Measured transfer curve and cross-axis test |
| R03 | Accumulate repeated threshold crossings and decay without them | Measured input work, decay law and threshold |
| R04 | Retain flag state after excitation stops | Retention and manual reset test |
| R05 | No detached parts or exposed pinch points in the bench rig | Independent fixture, containment and inspection |
| R06 | Reproduce all nominal calculations | Automated tests and checked-in tables |

Only R06 is addressed by the numerical release. The remainder are untested design goals.

## Architecture

Stationary machine housing → rigid mount → clamped beam and captive mass → adjustable gap → compliant drive pawl → one-way input to return-spring accumulator → trip cam → independent bistable visual flag.

A plain ratchet that locks its wheel against reverse rotation cannot implement decay. The proposed accumulator therefore needs a disengaging input pawl and a return path; its ratchet or one-way clutch must not lock the return motion. Candidate arrangements are a spring-loaded rack with an over-running input linkage or a sector with disengagement and a separately damped return. The flag must be independent of accumulator decay. Neither geometry is final.

## Envelope

The first envelope is a 125 × 54 × 34 mm single-channel bench module. The beam lies in its long direction and bends through its 0.8 mm thickness; the sensitive axis is normal to the strip. A 12 mm-wide clamp captures the root. A captive tip-mass holder is adjusted to 40 g **including** hardware. The free length is measured from the clamp edge to the effective tip mass location. Final clamp geometry, fasteners, end stops, clearances and spring grade must be derived after material and fixture selection.

An upright or side-mounted installation changes gravity loading. The gap must be set in the installed orientation. The OpenSCAD file is a simplified interference envelope and intentionally omits the unresolved drive and memory geometry. Do not fabricate it as a complete instrument.

## Candidate comparison

| Approach | Merit | Main limitation |
|---|---|---|
| Tuned cantilever with direct bistable flag | Few parts | Short shock may trip it |
| Tuned cantilever with leaky mechanical accumulator | Duration discrimination hypothesis | Input work and wear unresolved |
| Electronic accelerometer/logger | Calibrated broadband reference | Requires electrical power |

The direct flag is the physical baseline; the leaky mechanism is the research candidate. Neither should be treated as a replacement for qualified monitoring or shutdown equipment.

## Energy and coupling

At each measured threshold crossing, record the available work under load, not just free displacement. The unloaded stored energy is not the energy harvested per cycle. At resonance the drive supplies the dissipated energy in the existing resonator; harvesting extra work changes damping and possibly frequency. A pawl, spring preload, friction and return damping may prevent actuation entirely. Start with a low-force threshold contact, then test one accumulator under controlled motion before attaching it to the reed. Check for frequency shift, changed Q and missed/double advances.

# Verification and experimental protocol

## Release gates

| Gate | Status at v0.1.0 |
|---|---|
| Reproducible analytical model | Software checks included |
| Independent numerical convergence | Software check included |
| Material certificate and actual beam dimensions | NOT VERIFIED |
| Current purchased component ratings | NOT VERIFIED |
| Frequency, Q and threshold calibration | NOT VERIFIED |
| Pawl/accumulator energy budget | NOT VERIFIED |
| Shock discrimination and retained indication | NOT VERIFIED |
| Mounting, containment, fatigue and field suitability | NOT VERIFIED |

## Bench method

Use a guarded vibration test fixture with an independently calibrated accelerometer, displacement sensor or high-speed optical observation, and an appropriate reference analyser. Begin with the resonator only; do not attach to operating machinery until a competent engineer approves the mounting and hazard controls.

1. Record material grade, measured dimensions, clamp torque procedure, tip mass including hardware, orientation, ambient temperature, instrumentation calibration and uncertainty.
2. Conduct low-amplitude frequency sweeps on both sides of 25 Hz. Record peak base acceleration and relative tip displacement; estimate natural frequency and Q. Repeat at multiple drive amplitudes.
3. Calibrate the gap under gravity in the intended orientation. Check repeatability and cross-axis sensitivity.
4. On a separate fixture, measure pawl input force versus travel and work per stroke, return time constant, friction, and latch trip/reset force. Reject any mechanism that cannot operate within the **measured loaded** resonator energy budget.
5. Compare a direct flag baseline and accumulator candidate. At matched input amplitude and frequency, test sustained sine, short bursts, ringdown, detuned input and controlled non-damaging disturbances. Randomize order; reset between independent trials. Begin with 10 repetitions per condition; report every trial and uncertainty.
6. Verify retained flag state without excitation and a deliberate manual reset. Inspect for wear, loose parts, calibration drift and jammed mechanisms before each next stage.

## Proposed research acceptance criteria

These are provisional targets, not certified limits: natural frequency within ±2%; measured Q between 4 and 8; 0.40 g peak at 25 Hz for 3 s trips in at least 9/10 trials; 0.10 s burst of the same amplitude does not trip in 10/10 trials; flag remains set for 24 h under specified bench conditions. Report exact binomial confidence intervals; a small sample cannot establish reliability. Set a safe fixture amplitude limit independently. Stop for looseness, contact with enclosure, abnormal noise, permanent deformation or instrumentation fault.

Use the raw data schema: specimen_id, revision, orientation, test_id, repetition, frequency_hz, base_peak_g, duration_s, temperature_c, measured_tip_peak_mm, event_count, trip_s, flag_retained, notes, uncertainty. Do not fill missing values with zero. Publish raw evidence and analysis only after review.

Add a 0.40 s burst to exercise the accumulator with multiple threshold crossings while retaining the intended no-trip outcome. Report whether the direct-flag comparator trips on this input.

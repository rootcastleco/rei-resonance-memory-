# Numerical model

For a prismatic cantilever of free length L, width b and thickness t, the second moment I = b t³/12 and tip stiffness k = 3 E I/L³. Use the static tip-load shape phi(s) = (3s² - s³)/2, with s = x/L and phi(1) = 1. Its squared integral over the normalized span is 33/140; its integral is 3/8.

The generalized mass is m_eff = M + (33/140) rho A L. Uniform base acceleration acts through m_force = M + (3/8) rho A L. The participation factor gamma = m_force/m_eff. Treat the tip mass as a point mass, neglect its rotational inertia and clamp compliance.

The equation of relative tip motion is:

    x'' + (omega_n/Q) x' + omega_n² x = -gamma a_base(t)
    omega_n = sqrt(k/m_eff)

For sinusoidal peak acceleration a at angular frequency omega, the predicted peak displacement is:

    X = gamma a / sqrt((omega_n² - omega²)² + (omega omega_n/Q)²)

At omega = omega_n, X = gamma a Q / omega_n². For continuity with the initial concept, the nominal gap is computed with gamma = 1 at 0.30 g. The transient model includes gamma; the actual threshold therefore differs slightly from 0.30 g and must be calibrated.

The elastic strain energy at maximum displacement is U = k X²/2. For the unloaded linear oscillator at omega_n, loss per cycle is 2 pi U/Q. These quantities are **not** guaranteed extractable work. The nominal root stress from the static deflection shape is 3 E t |X|/(2 L²). No yield, fatigue, impact or clamp concentration claim follows from this estimate.

## Abstract memory

A dimensionless accumulator z decays exponentially between positive-going gap crossings. Each crossing increments z by one. The flag is set when z reaches H and stays set until reset. For ideal equal events at f events/s with decay time tau, the post-event steady state is 1/(1 - exp(-1/(f tau))). We choose tau = 1 s and H = 0.7 of that value at the channel's nominal frequency. This is a **software hypothesis**, not a specified damper, gear ratio or physical trip force. The numerical integrator uses fixed-step classical RK4 with at least 40 steps per fastest cycle; the default is 240. Gap crossings are resolved to the time step. Abrupt excitation cutoff is a numerical scenario, not an impact qualification.

## Limits

Linear small-deflection beam, ideal rigid base, sinusoidal base acceleration, one axis, independent channels, prescribed Q, no contact force or harvesting feedback, no temperature variation, no fatigue, no rotational tip inertia. Results are predictions, not measured spectra or machinery alarm levels. A transient run at 0.40 g for 3 s and a 0.10 s burst of the same drive serve only as examples.

The additional 0.40 s burst tests memory discrimination even when the gap is crossed. The sensitivity table varies Q, drive frequency and acceleration. Because the current function recalculates the gap from the chosen Q, these are retuned model scenarios rather than fixed-gap manufacturing drift tests.

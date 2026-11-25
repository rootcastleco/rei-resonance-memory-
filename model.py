"""Idealised mechanical resonator and abstract exposure-memory research model."""
from dataclasses import dataclass
import argparse
import json
import math

G = 9.80665

def positive(name, value):
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")

@dataclass(frozen=True)
class Beam:
    width: float = 0.012
    thickness: float = 0.0008
    young: float = 200e9
    density: float = 7850.0
    tip_mass: float = 0.040
    q: float = 6.0

    def __post_init__(self):
        for name, val in vars(self).items():
            positive(name, val)

    @property
    def area(self):
        return self.width * self.thickness

    @property
    def inertia(self):
        return self.width * self.thickness**3 / 12

    def effective_mass(self, length):
        positive("length", length)
        return self.tip_mass + (33/140)*self.density*self.area*length

    def stiffness(self, length):
        positive("length", length)
        return 3*self.young*self.inertia/length**3

    def natural_frequency(self, length):
        return math.sqrt(self.stiffness(length)/self.effective_mass(length))/(2*math.pi)

    def participation(self, length):
        # Static-tip-deflection assumed shape: integral(phi)=3L/8.
        return (self.tip_mass + (3/8)*self.density*self.area*length)/self.effective_mass(length)

    def tune(self, target_hz):
        positive("target frequency", target_hz)
        lo, hi = 0.005, 0.2
        if not self.natural_frequency(hi) <= target_hz <= self.natural_frequency(lo):
            raise ValueError("target outside the stated 5–200 mm beam envelope")
        for _ in range(80):
            mid = (lo+hi)/2
            if self.natural_frequency(mid) > target_hz:
                lo = mid
            else:
                hi = mid
        return (lo+hi)/2

    def amplitude(self, length, drive_hz, acceleration_g, *, unit_participation=False):
        if not math.isfinite(drive_hz) or drive_hz < 0:
            raise ValueError("drive frequency must be finite and nonnegative")
        if not math.isfinite(acceleration_g) or acceleration_g < 0:
            raise ValueError("peak acceleration must be finite and nonnegative")
        w = 2*math.pi*self.natural_frequency(length)
        ratio = 2*math.pi*drive_hz/w
        gamma = 1 if unit_participation else self.participation(length)
        return gamma*G*acceleration_g/(w*w*math.hypot(1-ratio*ratio, ratio/self.q))

    def stress(self, length, deflection):
        positive("length", length)
        if not math.isfinite(deflection):
            raise ValueError("deflection must be finite")
        return 1.5*self.young*self.thickness*abs(deflection)/length**2

@dataclass
class Memory:
    """Dimensionless ideal leaky event counter, NOT a physical accumulator."""
    tau: float
    threshold: float
    value: float = 0.0
    latched: bool = False

    def __post_init__(self):
        positive("time constant", self.tau)
        positive("threshold", self.threshold)
        if not math.isfinite(self.value) or self.value < 0:
            raise ValueError("initial value must be finite and nonnegative")
        self.latched = self.latched or self.value >= self.threshold

    def advance(self, dt, event=False):
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("time step must be finite and nonnegative")
        self.value = self.value*math.exp(-dt/self.tau) + int(bool(event))
        self.latched = self.latched or self.value >= self.threshold
        return self.latched

    def reset(self):
        self.value, self.latched = 0.0, False

def channel(target_hz, beam=Beam()):
    length = beam.tune(target_hz)
    gap = beam.amplitude(length, target_hz, 0.30, unit_participation=True)
    x = beam.amplitude(length, target_hz, 0.30)
    return dict(frequency_hz=target_hz, free_length_mm=length*1000,
                effective_mass_g=beam.effective_mass(length)*1000,
                stiffness_n_per_m=beam.stiffness(length), participation=beam.participation(length),
                gap_mm=gap*1000, response_mm=x*1000,
                stored_energy_uj=0.5*beam.stiffness(length)*x*x*1e6,
                root_stress_mpa_at_05g=beam.stress(length, beam.amplitude(length,target_hz,0.5))/1e6,
                memory_threshold=0.7/(-math.expm1(-1/target_hz)))

def simulate(beam, target_hz, drive_hz, acceleration_g, duration, *, on_time=None, steps_per_cycle=240):
    """RK4 integration, positive-gap upward crossings; ideal event increment of 1."""
    for n, v in [("target",target_hz),("drive",drive_hz),("duration",duration)]:
        positive(n,v)
    if not math.isfinite(acceleration_g) or acceleration_g < 0:
        raise ValueError("invalid acceleration")
    if not isinstance(steps_per_cycle,int) or steps_per_cycle < 40:
        raise ValueError("use at least 40 steps per cycle")
    if on_time is None:
        on_time = duration
    if not math.isfinite(on_time) or not 0 <= on_time <= duration:
        raise ValueError("invalid excitation duration")
    length = beam.tune(target_hz)
    gap = channel(target_hz, beam)["gap_mm"]/1000
    w = 2*math.pi*target_hz
    gamma = beam.participation(length)
    threshold = channel(target_hz,beam)["memory_threshold"]
    mem = Memory(1.0, threshold)
    n = math.ceil(duration*max(drive_hz,target_hz)*steps_per_cycle)
    if n > 3_000_000:
        raise ValueError("simulation step budget exceeded")
    dt = duration/n
    x = v = peak = 0.0
    events = 0
    trip = None
    def deriv(t, x, v):
        a = acceleration_g*G*math.sin(2*math.pi*drive_hz*t) if t < on_time else 0.0
        return v, -w*w*x-w/beam.q*v-gamma*a
    for i in range(n):
        t=i*dt
        a,b=deriv(t,x,v)
        c,d=deriv(t+dt/2,x+dt*a/2,v+dt*b/2)
        e,f=deriv(t+dt/2,x+dt*c/2,v+dt*d/2)
        h,j=deriv(t+dt,x+dt*e,v+dt*f)
        xn=x+dt*(a+2*c+2*e+h)/6
        v=v+dt*(b+2*d+2*f+j)/6
        event=x<gap<=xn
        events+=int(event)
        if mem.advance(dt,event) and trip is None:
            trip=(i+1)*dt
        peak=max(peak,abs(xn))
        x=xn
    return dict(peak_mm=peak*1000,events=events,trip_s=trip,latched=mem.latched,
                final_accumulator=mem.value,steps=n)

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frequency",type=float,default=25)
    p.add_argument("--acceleration-g",type=float,default=0.30)
    p.add_argument("--duration",type=float,default=3)
    a=p.parse_args()
    print(json.dumps({"channel":channel(a.frequency),"transient":simulate(Beam(),a.frequency,a.frequency,a.acceleration_g,a.duration)},indent=2))

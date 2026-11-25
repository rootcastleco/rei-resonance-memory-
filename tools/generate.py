"""Generate original vector diagrams and numerical tables; standard library only."""
import csv, json, sys
from pathlib import Path
from math import pi
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model import Beam, channel, simulate
A=ROOT/"assets"; R=ROOT/"results"
A.mkdir(exist_ok=True);R.mkdir(exist_ok=True)
b=Beam(); freqs=[20,25,40,50]
rows=[channel(f,b) for f in freqs]
with (R/"channels.csv").open("w",newline="") as file:
    w=csv.DictWriter(file,fieldnames=rows[0].keys(),lineterminator="\n");w.writeheader()
    for row in rows:w.writerow({k:round(v,8) for k,v in row.items()})
scenarios={n:simulate(b,25,f,a,3,on_time=t) for n,f,a,t in [
    ("sustained",25,.4,3),("short_burst",25,.4,.1),
    ("crossing_burst",25,.4,.4), ("off_band",40,.4,3),("zero",25,0,3)]}
(R/"scenarios.json").write_text(json.dumps(scenarios,indent=2)+"\n")
header='<svg xmlns="http://www.w3.org/2000/svg" width="960" height="430" viewBox="0 0 960 430"><rect width="960" height="430" fill="#fff"/><g font-family="Arial, sans-serif" fill="#172029">'
out=[header,'<text x="32" y="38" font-size="24" font-weight="bold">Frequency-selective mechanical memory</text><text x="32" y="61" font-size="13" fill="#536271">Functional concept | no powered components | prototype not built</text>']
colors=["#0e3d8a","#526879","#526879","#526879"]
for i,(f,L) in enumerate(zip(freqs,[row["free_length_mm"] for row in rows])):
    y=105+i*67
    out.append(f'<rect x="32" y="{y-15}" width="90" height="43" rx="4" fill="#f3f5f7"/><text x="45" y="{y+5}" font-size="20" font-weight="bold">{f} Hz</text><text x="45" y="{y+20}" font-size="10">channel {i+1}</text>')
    end=163+L*1.8
    out.append(f'<rect x="146" y="{y-5}" width="17" height="26" fill="#445260"/><path d="M163 {y+8} H{end}" stroke="#0e3d8a" stroke-width="5"/><rect x="{end-9}" y="{y-4}" width="18" height="24" rx="2" fill="#c5a46e" stroke="#77664c"/><path d="M{end+13} {y+8} H355" stroke="#64748b" stroke-dasharray="4 4" fill="none"/>')
    for x,w,label in [(359,104,"Gap / pawl"),(490,157,"Leaky accumulator"),(676,116,"Trip / latch")]:
        out.append(f'<rect x="{x}" y="{y-10}" width="{w}" height="36" rx="4" fill="#eef2f6" stroke="#9eabb9"/><text x="{x+w/2}" y="{y+12}" text-anchor="middle" font-size="12">{label}</text>')
    for x in [463,647,792]:
        out.append(f'<path d="M{x} {y+8} H{x+21} l-5 -4 m5 4 l-5 4" fill="none" stroke="#0e3d8a" stroke-width="1.5"/>')
    out.append(f'<rect x="819" y="{y-10}" width="109" height="36" rx="4" fill="#e8f3eb" stroke="#228b55"/><text x="873" y="{y+12}" text-anchor="middle" font-size="12">Flag / reset</text>')
out.append('<path d="M146 95 V330" stroke="#445260" stroke-width="4"/><text x="32" y="393" font-size="13" fill="#536271">Rigid base input → tuned beam → threshold → ideal leaky accumulation → independent persistent flag</text></g></svg>')
(A/"architecture.svg").write_text("\n".join(out))
out=[header,'<text x="32" y="38" font-size="24" font-weight="bold">Unloaded response | 0.30 g peak</text><text x="32" y="61" font-size="13" fill="#536271">Linear assumed-shape model, Q = 6. Computed, not measured.</text>']
x0,y0,w,h=88,344,814,250
for j in range(5):
    v=j*.35;y=y0-h*v/1.4
    out.append(f'<path d="M{x0} {y} H{x0+w}" stroke="#e3e7ec"/><text x="75" y="{y+4}" text-anchor="end" font-size="11">{v:.2f}</text>')
for f in range(10,71,10):
    x=x0+(f-10)/60*w
    out.append(f'<text x="{x}" y="365" font-size="11" text-anchor="middle">{f}</text>')
out.append(f'<path d="M{x0} {y0-h} V{y0} H{x0+w}" fill="none" stroke="#536271"/><text x="495" y="388" text-anchor="middle" font-size="13">Excitation frequency (Hz)</text><text transform="translate(22 219) rotate(-90)" text-anchor="middle" font-size="13">Peak displacement (mm)</text>')
for i,f in enumerate(freqs):
    L=b.tune(f);c=["#0e3d8a","#228b55","#9b641e","#884e81"][i];pts=[]
    for k in range(601):
        fd=10+k/10;v=b.amplitude(L,fd,.3)*1000;pts.append(f"{x0+(fd-10)/60*w:.2f},{y0-v/1.4*h:.2f}")
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width="2.3"/>')
    xx=590+i*80
    out.append(f'<path d="M{xx} 76 h19" stroke="{c}" stroke-width="3"/><text x="{xx+23}" y="80" font-size="11">{f} Hz</text>')
out.append('</g></svg>')
(A/"response.svg").write_text("\n".join(out))
with (R/"sensitivity.csv").open("w",newline="") as file:
    w=csv.writer(file,lineterminator="\n");w.writerow(["q","drive_hz","peak_g","nominal_length_mm","peak_mm","events","trip_s","latched"])
    for q in (4,6,8):
        for f in (20,24,25,26,30):
            for acc in (.2,.3,.4):
                beam=Beam(q=q); r=simulate(beam,25,f,acc,3)
                w.writerow([q,f,acc,round(beam.tune(25)*1000,6),round(r["peak_mm"],6),r["events"],r["trip_s"],r["latched"]])
print("Generated vector diagrams, channel table, transient scenarios and 45 sensitivity cases.")

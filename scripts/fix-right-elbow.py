from pathlib import Path

path = Path("rig-labor.html")
html = path.read_text(encoding="utf-8")
old = "const sign=name.endsWith('_l')?1:-1;"
new = "const sign=1; // Right elbow calibrated to flex in the same anatomical direction"
if html.count(old) != 1:
    raise SystemExit(f"Expected one elbow direction expression, found {html.count(old)}")
path.write_text(html.replace(old, new, 1), encoding="utf-8")
print("Right elbow flexion direction corrected in published rig-labor.html")

from pathlib import Path

p = Path("rig-labor.html")
s = p.read_text(encoding="utf-8")
marker = '<label>Beide Ellenbogen: <strong id="angleText">0°</strong></label>'
assert s.count(marker) == 1, "Angle label not found"
s = s.replace(marker, '<label>Gemeinsamer anatomischer Beugewinkel: <strong id="angleText">0°</strong></label>', 1)
old = '<label>Rotationsachse (zum Kalibrieren)</label><select id="axis"><option value="z">Lokale Z-Achse</option><option value="x">Lokale X-Achse</option><option value="y">Lokale Y-Achse</option></select>'
assert s.count(old) == 1, "Original axis control not found"
new = '''<div class="row"><div><label>Linker Ellenbogen · lokale Achse</label><select id="axis_l"><option value="z">Z</option><option value="x">X</option><option value="y">Y</option></select><label>Drehrichtung links</label><select id="sign_l"><option value="1">Positiv (+)</option><option value="-1">Negativ (−)</option></select><label>Neutralstellung links (°)</label><input id="offset_l" type="number" value="0" min="-180" max="180" step="1" style="width:100%;padding:10px;background:#174b68;color:white;border:1px solid #40718d;border-radius:8px"></div><div><label>Rechter Ellenbogen · lokale Achse</label><select id="axis_r"><option value="z">Z</option><option value="x">X</option><option value="y">Y</option></select><label>Drehrichtung rechts</label><select id="sign_r"><option value="-1">Negativ (−)</option><option value="1">Positiv (+)</option></select><label>Neutralstellung rechts (°)</label><input id="offset_r" type="number" value="0" min="-180" max="180" step="1" style="width:100%;padding:10px;background:#174b68;color:white;border:1px solid #40718d;border-radius:8px"></div></div><p><small>Beide Seiten verwenden denselben anatomischen Winkel. Achse, Vorzeichen und Neutralstellung sind unabhängig kalibrierbar. Die Einstellung ist noch keine anatomische Validierung.</small></p>'''
s = s.replace(old, new, 1)
start = "function apply(){if(!model)return;"
end = "function load(){try{"
a = s.index(start)
b = s.index(end, a)
replacement = """function apply(){if(!model)return;const a=Math.max(0,Math.min(135,Number($('angle').value)||0));$('angleText').textContent=a+'°';for(const side of ['l','r']){const name='lowerarm_'+side,b=bones[name];if(!b)continue;const axis=$('axis_'+side).value;const sign=Number($('sign_'+side).value);const offset=Math.max(-180,Math.min(180,Number($('offset_'+side).value)||0));const v=new THREE.Vector3(axis==='x'?1:0,axis==='y'?1:0,axis==='z'?1:0);b.quaternion.copy(original[name]);b.quaternion.multiply(new THREE.Quaternion().setFromAxisAngle(v,(offset+sign*a)*Math.PI/180))}}"""
s = s[:a]+replacement+s[b:]
s = s.replace("$('axis').onchange=apply;", "for(const id of ['axis_l','axis_r','sign_l','sign_r','offset_l','offset_r']){$(id).addEventListener('input',apply);$(id).addEventListener('change',apply)}", 1)
s = s.replace('Anatomie Motion 3D · v2.7.1', 'Anatomie Motion 3D · v2.8 – Gelenkkalibrierung', 1)
p.write_text(s, encoding="utf-8")
print("Independent left/right elbow calibration controls installed.")

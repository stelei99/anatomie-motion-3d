from pathlib import Path
p=Path("rig-labor-v3.0.html")
s=p.read_text(encoding="utf-8")
assert "EXTRA_JOINTS" in s
s=s.replace("v3.0 – Gelenkanalyse (Beta)","v3.1 – Knie-Winkelmessung (Beta)")
needle='<label>Hüftbeugung (beidseitig):'
assert s.count(needle)==1
panel='''<div style="padding:10px;margin:10px 0;background:#092b43;border:1px solid #46748d;border-radius:8px"><strong>Gemessener Kniewinkel aus Knochenpositionen</strong><p style="font-size:13px;margin:6px 0">Links: <strong id="kneeMeasuredL">–</strong> · Rechts: <strong id="kneeMeasuredR">–</strong></p><p id="kneeDeviation" style="font-size:12px;margin:4px 0">Warte auf Messung …</p><p style="font-size:11px;opacity:.8">Messpunkte: Hüftgelenk (Oberschenkelknochen), Kniegelenk (Unterschenkelknochen), Fußknochen als Näherung für das Sprunggelenk. Ergebnis ist eine geometrische Messung am Rig, keine klinische Messung.</p></div>'''
s=s.replace(needle,panel+needle,1)
needle="function applyExtraJoints(){"
assert s.count(needle)==1
measurement="""function measureKnees(){
  if(!model)return;
  model.updateMatrixWorld(true);
  const target=Number(document.getElementById('kneeAngle').value)||0;
  const results={};
  for(const side of ['l','r']){
    const hip=bones['thigh_'+side],knee=bones['calf_'+side],ankle=bones['foot_'+side];
    const out=document.getElementById(side==='l'?'kneeMeasuredL':'kneeMeasuredR');
    if(!hip||!knee||!ankle){out.textContent='nicht messbar';continue}
    const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();
    hip.getWorldPosition(a);knee.getWorldPosition(b);ankle.getWorldPosition(c);
    const up=a.sub(b),down=c.sub(b);
    if(up.length()<1e-5||down.length()<1e-5){out.textContent='nicht messbar';continue}
    const interior=up.angleTo(down)*180/Math.PI;
    const flexion=Math.max(0,Math.min(180,180-interior));
    results[side]=flexion;
    out.textContent=flexion.toFixed(1)+'°';
  }
  const diag=document.getElementById('kneeDeviation');
  if(results.l!==undefined&&results.r!==undefined){
    const dl=results.l-target,dr=results.r-target;
    diag.textContent='Soll: '+target+'° · Abweichung links: '+(dl>=0?'+':'')+dl.toFixed(1)+'° · rechts: '+(dr>=0?'+':'')+dr.toFixed(1)+'°';
  }else diag.textContent='Messung nicht möglich: erforderliche Knochenpositionen fehlen.';
}
"""
s=s.replace(needle,measurement+needle,1)
needle="  applyExtraJoints();\n  model.updateMatrixWorld(true);"
assert s.count(needle)==1
s=s.replace(needle,"  applyExtraJoints();\n  model.updateMatrixWorld(true);\n  measureKnees();",1)
Path("rig-labor-v3.1.html").write_text(s,encoding="utf-8")
print("v3.1 knee angle measurements generated")

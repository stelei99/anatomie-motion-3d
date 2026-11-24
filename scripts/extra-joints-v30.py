from pathlib import Path
p=Path("rig-labor-v2.9.html")
s=p.read_text(encoding="utf-8")
assert "AUTO_JOINTS" in s, "v2.9 must be generated first"
s=s.replace("v2.9 – automatische Ellenbogenkalibrierung","v3.0 – Gelenkanalyse (Beta)")
# Inject a panel adjacent to existing auto status without changing elbow controls.
needle='<p id="autostatus"'
assert s.count(needle)==1
panel='''<section style="margin:12px 0;padding:12px;border:1px solid #46748d;border-radius:10px"><h3 style="margin:0 0 8px">Weitere Gelenke · automatische Analyse (Beta)</h3><p style="font-size:13px">Knie, Hüfte und Schulter: Achsen werden aus den Knochenpositionen abgeleitet. Dies ist eine technische Vorschau, keine anatomisch validierte Bewegung.</p><label>Kniebeugung (beidseitig): <strong id="kneeText">0°</strong></label><input type="range" id="kneeAngle" min="0" max="120" value="0" style="width:100%"><label>Hüftbeugung (beidseitig): <strong id="hipText">0°</strong></label><input type="range" id="hipAngle" min="0" max="90" value="0" style="width:100%"><label>Schultervorhebung (beidseitig): <strong id="shoulderText">0°</strong></label><input type="range" id="shoulderAngle" min="0" max="90" value="0" style="width:100%"><p id="jointDiagnostics" role="status" style="font-size:12px;white-space:pre-line">Warte auf Modell …</p></section>'''
s=s.replace(needle,panel+needle,1)
needle="function apply(){\n  if(!model)return;"
assert needle in s
# Inferred rotation: choose world flexion axis based on segment and model's anterior +Z.
# For knee the calf moves posterior (-Z); hip/shoulder move anterior (+Z).
extra="""const EXTRA_JOINTS={};
function inferExtraJoints(){
  model.updateMatrixWorld(true);
  const specs=[
    ['knee','calf','foot','thigh',-1],
    ['hip','thigh','calf','pelvis',1],
    ['shoulder','upperarm','lowerarm','spine_03',1]
  ];
  const report=[];
  for(const [kind,segment,child,anchor,dir] of specs){
    for(const side of ['l','r']){
      const bone=bones[segment+'_'+side],next=bones[child+'_'+side];
      const root=bones[anchor+'_'+side]||bones[anchor];
      const key=kind+'_'+side;
      if(!bone||!next||!root){EXTRA_JOINTS[key]={valid:false};report.push(key+': Knochen fehlen');continue}
      const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();
      root.getWorldPosition(a);bone.getWorldPosition(b);next.getWorldPosition(c);
      const segmentDir=c.clone().sub(b);
      if(segmentDir.length()<1e-5){EXTRA_JOINTS[key]={valid:false};report.push(key+': Segment zu kurz');continue}
      segmentDir.normalize();
      const front=new THREE.Vector3(0,0,dir);
      front.addScaledVector(segmentDir,-front.dot(segmentDir));
      if(front.length()<.1){EXTRA_JOINTS[key]={valid:false};report.push(key+': Bewegungsachse nicht eindeutig');continue}
      front.normalize();
      const worldAxis=new THREE.Vector3().crossVectors(segmentDir,front).normalize();
      const parentQ=new THREE.Quaternion();bone.parent.getWorldQuaternion(parentQ);
      const axis=worldAxis.applyQuaternion(parentQ.clone().invert());
      EXTRA_JOINTS[key]={valid:true,bone,base:original[bone.name].clone(),axis};
      report.push(key+': Achse erkannt (nicht validiert)');
    }
  }
  const status=document.getElementById('jointDiagnostics');
  if(status)status.textContent=report.join(' | ');
}
function applyExtraJoints(){
  for(const kind of ['knee','hip','shoulder']){
    const control=document.getElementById(kind+'Angle');
    if(!control)continue;
    const angle=Number(control.value)||0;
    document.getElementById(kind+'Text').textContent=angle+'°';
    for(const side of ['l','r']){
      const j=EXTRA_JOINTS[kind+'_'+side];
      if(!j?.valid)continue;
      j.bone.quaternion.copy(new THREE.Quaternion().setFromAxisAngle(j.axis,angle*Math.PI/180)).multiply(j.base);
    }
  }
}
"""
s=s.replace(needle,extra+needle,1)
# preserve the original elbow apply, add additional joint application before matrix update
needle="  model.updateMatrixWorld(true);\n}\nfunction load()"
assert needle in s
s=s.replace(needle,"  applyExtraJoints();\n  model.updateMatrixWorld(true);\n}\nfunction load()",1)
needle="model.updateMatrixWorld(true);autoCalibrate();"
assert needle in s
s=s.replace(needle,"model.updateMatrixWorld(true);autoCalibrate();inferExtraJoints();",1)
needle="window.addEventListener('resize',resize);"
assert needle in s
s=s.replace(needle,"for(const kind of ['knee','hip','shoulder']){document.getElementById(kind+'Angle').addEventListener('input',apply)}"+needle,1)
Path("rig-labor-v3.0.html").write_text(s,encoding="utf-8")
print("v3.0 experimental joint-analysis page built: knees, hips, shoulders.")

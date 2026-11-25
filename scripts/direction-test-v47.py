from pathlib import Path
s=Path("rig-labor-v4.6.html").read_text(encoding="utf-8")
assert "calibrateKneeAxes()" in s
s=s.replace("v4.6 – Winkelmessung und Achsenkorrektur (Beta)","v4.7 – Winkelreaktion prüfen (Beta)")
needle='<p id="kneeCalibrationStatus"'
assert s.count(needle)==1
panel='''<div style="padding:9px;margin:8px 0;border:1px solid #46748d;border-radius:8px"><strong>Bewegungsrichtung automatisch testen</strong><p style="font-size:12px">Testet Knie links/rechts bei 0° und 15° am Rig. Prüft die gemessene Winkeländerung; die anatomische Beugerichtung lässt sich aus einem ungerichteten Winkel allein nicht sicher bestimmen. Hüft-, Schulter- und Ellenbogenachsen werden zusätzlich auf numerische Plausibilität geprüft. Die Ausgangsstellung wird danach wiederhergestellt.</p><button type="button" id="directionTestButton">Winkelreaktion prüfen</button><p id="directionTestStatus" role="status" style="font-size:12px;white-space:pre-line">Noch nicht geprüft.</p></div>'''
s=s.replace(needle,panel+needle,1)
js="""function readKneeAngle(side){
 const hip=bones['thigh_'+side],knee=bones['calf_'+side],ankle=bones['foot_'+side];
 if(!hip||!knee||!ankle)return NaN;
 const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();
 hip.getWorldPosition(a);knee.getWorldPosition(b);ankle.getWorldPosition(c);
 const u=a.sub(b),v=c.sub(b);
 if(u.lengthSq()<1e-8||v.lengthSq()<1e-8)return NaN;
 return 180-u.angleTo(v)*180/Math.PI;
}
function testMotionDirections(){
 if(!model)return;
 const slider=document.getElementById('kneeAngle');
 const saved=slider.value;
 const messages=[];
 try{
  slider.value='0';apply();
  for(const side of ['l','r']){
   const joint=EXTRA_JOINTS['knee_'+side];
   if(!joint?.valid){messages.push('Knie '+side+': nicht verfügbar');continue}
   model.updateMatrixWorld(true);
   const neutral=readKneeAngle(side);
   slider.value='15';apply();model.updateMatrixWorld(true);
   const measured=readKneeAngle(side);
   if(!Number.isFinite(neutral)||!Number.isFinite(measured)){
    messages.push('Knie '+side+': Messung nicht möglich');slider.value='0';apply();continue;
   }
   const change=measured-neutral;
   if(change< -2){
    messages.push('Knie '+side+': Winkel nimmt ab ('+change.toFixed(1)+'°) – manuelle anatomische Prüfung nötig');
   }else if(change<2){
    messages.push('Knie '+side+': kaum Winkeländerung ('+change.toFixed(1)+'°), keine automatische Korrektur');
   }else messages.push('Knie '+side+': Winkel steigt um '+change.toFixed(1)+'° bei 15° Soll');
   slider.value='0';apply();
  }
  for(const side of ['l','r']){
   const e=AUTO_JOINTS[side];
   messages.push('Ellenbogen '+side+': '+(e?.valid&&e.axisLocal?.lengthSq()>.8?'Achse vorhanden':'nicht eindeutig'));
   for(const kind of ['hip','shoulder']){
    const j=EXTRA_JOINTS[kind+'_'+side];
    messages.push(kind+' '+side+': '+(j?.valid&&j.axis?.lengthSq()>.8?'Achse vorhanden, Richtung unbestätigt':'nicht eindeutig'));
   }
  }
 }finally{
  slider.value=saved;
  apply();
 }
 document.getElementById('directionTestStatus').textContent=messages.join(' · ');
 auditRigAxes();
}
document.getElementById('directionTestButton').addEventListener('click',testMotionDirections);
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,js+needle,1)
Path("rig-labor-v4.7.html").write_text(s,encoding="utf-8")
print("v4.7 direction test generated")

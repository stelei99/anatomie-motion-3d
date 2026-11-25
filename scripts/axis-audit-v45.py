from pathlib import Path
s=Path("rig-labor-v4.4.html").read_text(encoding="utf-8")
assert "configureForearmFingers()" in s
s=s.replace("v4.4 – Unterarm und Finger (Beta)","v4.5 – Achsenprüfung und Kalibrierdiagnose (Beta)")
needle='<p id="forearmFingerStatus"'
assert s.count(needle)==1
panel='''<section style="padding:10px;margin:10px 0;border:1px solid #ffcb05;border-radius:8px"><h3>Automatische Achsenprüfung · v4.5</h3><p style="font-size:12px">Prüft Gelenkachsen auf endliche Werte, Normierung, Segmentausrichtung und Modellverfügbarkeit. Dies ist eine technische Plausibilitätsprüfung, keine anatomische Validierung.</p><button type="button" id="axisAuditButton">Achsen erneut prüfen</button><p id="axisAuditSummary" role="status">Warte auf Modell …</p><div id="axisAuditRows" style="max-height:260px;overflow:auto"></div></section>'''
s=s.replace(needle,panel+needle,1)
js="""const AXIS_AUDIT={results:[]};
function auditAxis(key,bone,axis,reference,kind){
 let status='OK',reason='Achse numerisch plausibel';
 if(!bone||!axis){status='FEHLT';reason='Knochen oder Achse fehlt'}
 else if(![axis.x,axis.y,axis.z].every(Number.isFinite)||axis.lengthSq()<0.8||axis.lengthSq()>1.2){
  status='FEHLER';reason='Achse ungültig oder nicht normiert';
 }else if(reference&&reference.lengthSq()>1e-8){
  const parallel=Math.abs(axis.clone().normalize().dot(reference.clone().normalize()));
  if(kind==='hinge'&&parallel>0.4){status='WARNUNG';reason='Achse liegt zu nah an der Segmentlängsrichtung ('+parallel.toFixed(2)+')'}
  if(kind==='twist'&&parallel<0.7){status='WARNUNG';reason='Rotationsachse weicht von Segmentlängsrichtung ab ('+parallel.toFixed(2)+')'}
 }
 return {key,status,reason};
}
function auditRigAxes(){
 if(!model)return;
 model.updateMatrixWorld(true);
 const results=[];
 const segmentLocal=(bone,child)=>{
  if(!bone||!child||!bone.parent)return null;
  const a=new THREE.Vector3(),b=new THREE.Vector3(),q=new THREE.Quaternion();
  bone.getWorldPosition(a);child.getWorldPosition(b);
  bone.parent.getWorldQuaternion(q);
  return b.sub(a).applyQuaternion(q.invert());
 };
 for(const side of ['l','r']){
  const elbow=AUTO_JOINTS[side];
  results.push(auditAxis('Ellenbogen '+side,elbow?.lower,elbow?.axisLocal,segmentLocal(elbow?.lower,bones['hand_'+side]),'hinge'));
  for(const kind of ['knee','hip','shoulder']){
   const j=EXTRA_JOINTS[kind+'_'+side];
   const next=kind==='knee'?bones['foot_'+side]:kind==='hip'?bones['calf_'+side]:bones['lowerarm_'+side];
   results.push(auditAxis(kind+' '+side,j?.bone,j?.axis,segmentLocal(j?.bone,next),'hinge'));
  }
  const forearm=FOREARM_FINGER_RIG.forearms.find(j=>j.side===side);
  results.push(auditAxis('Unterarmrotation '+side,forearm?.bone,forearm?.axis,segmentLocal(forearm?.bone,bones['hand_'+side]),'twist'));
 }
 for(const [key,j] of Object.entries(ADDITIONAL_JOINTS)){
  results.push(auditAxis(key,j?.bone,j?.axis,null,'other'));
 }
 for(const j of FOREARM_FINGER_RIG.fingers){
  results.push(auditAxis('Finger '+j.bone.name,j.bone,j.axis,null,'other'));
 }
 AXIS_AUDIT.results=results;
 const rows=document.getElementById('axisAuditRows');rows.replaceChildren();
 for(const item of results){
  const el=document.createElement('div');el.style.cssText='font-size:12px;border-bottom:1px solid #31516a;padding:5px 0';
  el.textContent=item.status+' · '+item.key+' · '+item.reason;
  rows.appendChild(el);
 }
 const counts={};
 for(const item of results)counts[item.status]=(counts[item.status]||0)+1;
 document.getElementById('axisAuditSummary').textContent=results.length+' Achsen geprüft · '+(counts.OK||0)+' plausibel · '+(counts.WARNUNG||0)+' Warnungen · '+(counts.FEHLER||0)+' Fehler · '+(counts.FEHLT||0)+' nicht verfügbar';
}
document.getElementById('axisAuditButton').addEventListener('click',auditRigAxes);
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,js+needle,1)
needle="configureForearmFingers();"
assert s.count(needle)==1
s=s.replace(needle,"configureForearmFingers();auditRigAxes();",1)
Path("rig-labor-v4.5.html").write_text(s,encoding="utf-8")
print("v4.5 axis audit generated")

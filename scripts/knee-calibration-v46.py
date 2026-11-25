from pathlib import Path
s=Path("rig-labor-v4.5.html").read_text(encoding="utf-8")
assert "auditRigAxes()" in s
s=s.replace("v4.5 – Achsenprüfung und Kalibrierdiagnose (Beta)","v4.6 – Winkelmessung und Achsenkorrektur (Beta)")
needle='<p id="axisAuditSummary"'
assert s.count(needle)==1
panel='''<div style="margin:8px 0;padding:8px;border:1px solid #46748d;border-radius:7px"><strong>Knie: automatische Achsenkorrektur und Winkelprüfung</strong><p style="font-size:12px">Projiziert fehlerhafte Knie-Scharnierachsen senkrecht zur Unterschenkellängsachse. Vergleicht anschließend gemessenen und eingestellten Winkel. Keine automatische Änderung bei mehrdeutiger Achse.</p><button type="button" id="calibrateKneesButton">Knieachsen prüfen und korrigieren</button><p id="kneeCalibrationStatus" role="status" style="font-size:12px;white-space:pre-line">Noch nicht geprüft.</p></div>'''
s=s.replace(needle,panel+needle,1)
js="""function calibrateKneeAxes(){
 if(!model)return;
 const messages=[];
 // Use the current pose for numerical checks, but derive the axis in each bone's parent coordinates.
 model.updateMatrixWorld(true);
 for(const side of ['l','r']){
  const j=EXTRA_JOINTS['knee_'+side];
  const bone=j?.bone,foot=bones['foot_'+side];
  if(!j?.valid||!bone||!foot){messages.push('Knie '+side+': Knochen fehlen');continue}
  const p=new THREE.Vector3(),c=new THREE.Vector3(),q=new THREE.Quaternion();
  bone.getWorldPosition(p);foot.getWorldPosition(c);
  bone.parent.getWorldQuaternion(q);
  const direction=c.sub(p).applyQuaternion(q.invert());
  if(direction.lengthSq()<1e-8||!j.axis||!Number.isFinite(j.axis.lengthSq())){
   messages.push('Knie '+side+': Achse nicht eindeutig');continue;
  }
  direction.normalize();
  const axis=j.axis.clone();
  const projected=axis.addScaledVector(direction,-axis.dot(direction));
  if(projected.lengthSq()<0.05){
   messages.push('Knie '+side+': Achse nahezu parallel zum Knochen – keine sichere Korrektur');continue;
  }
  projected.normalize();
  const deviation=Math.acos(THREE.MathUtils.clamp(j.axis.clone().normalize().dot(projected),-1,1))*180/Math.PI;
  if(deviation>1){
   j.axis.copy(projected);
   messages.push('Knie '+side+': Achse um '+deviation.toFixed(1)+'° orthogonalisiert');
  }else messages.push('Knie '+side+': Achse bereits orthogonal');
 }
 // Reapply existing slider targets, then measure actual knee angles.
 apply();
 const target=Number(document.getElementById('kneeAngle')?.value)||0;
 for(const side of ['l','r']){
  const measured=Number.parseFloat(document.getElementById(side==='l'?'kneeMeasuredL':'kneeMeasuredR')?.textContent||'');
  if(Number.isFinite(measured)){
   const delta=Math.abs(measured-target);
   messages.push('Knie '+side+': Soll '+target.toFixed(1)+'°, gemessen '+measured.toFixed(1)+'° ('+(delta<=10?'innerhalb':'außerhalb')+' ±10°)');
  }else messages.push('Knie '+side+': Winkelmessung nicht verfügbar');
 }
 document.getElementById('kneeCalibrationStatus').textContent=messages.join(' · ');
 auditRigAxes();
}
document.getElementById('calibrateKneesButton').addEventListener('click',calibrateKneeAxes);
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,js+needle,1)
Path("rig-labor-v4.6.html").write_text(s,encoding="utf-8")
print("v4.6 knee axis correction and measured angle check generated")

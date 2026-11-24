from pathlib import Path
s=Path("rig-labor-v4.3.html").read_text(encoding="utf-8")
assert "applyAdditionalJoints();" in s
s=s.replace("v4.3 – Zusätzliche Gelenksteuerung (Beta)","v4.4 – Unterarm und Finger (Beta)")
needle='<p id="newJointsStatus"'
assert s.count(needle)==1
panel='''<div style="padding:10px;margin:10px 0;border:1px solid #46748d;border-radius:8px"><strong>Unterarm und Finger · Teststeuerung</strong><p style="font-size:12px">Unterarmdrehung ist eine vereinfachte Rig-Rotation und bildet Radius/Ulna nicht einzeln ab. Finger werden nur bewegt, wenn eigene Rig-Knochen existieren.</p><label>Unterarmrotation links: <strong id="forearmLText">0°</strong></label><input type="range" id="forearmL" min="-75" max="75" value="0" style="width:100%"><label>Unterarmrotation rechts: <strong id="forearmRText">0°</strong></label><input type="range" id="forearmR" min="-75" max="75" value="0" style="width:100%"><label>Fingerbeugung (beide Hände): <strong id="fingerCurlText">0°</strong></label><input type="range" id="fingerCurl" min="0" max="70" value="0" style="width:100%"><button id="forearmFingerReset" type="button">Unterarm und Finger zurücksetzen</button><p id="forearmFingerStatus" role="status" style="font-size:12px;white-space:pre-line">Prüfe Rig …</p></div>'''
s=s.replace(needle,panel+needle,1)
js="""const FOREARM_FINGER_RIG={forearms:[],fingers:[]};
function configureForearmFingers(){
 FOREARM_FINGER_RIG.forearms=[];FOREARM_FINGER_RIG.fingers=[];
 const notes=[];
 model.updateMatrixWorld(true);
 for(const side of ['l','r']){
  const forearm=bones['lowerarm_'+side],hand=bones['hand_'+side];
  if(!forearm||!hand){notes.push('Unterarm '+side+': nicht verfügbar');continue}
  const a=new THREE.Vector3(),b=new THREE.Vector3();
  forearm.getWorldPosition(a);hand.getWorldPosition(b);
  const world=b.sub(a);
  if(world.lengthSq()<1e-8){notes.push('Unterarm '+side+': Achse unbestimmt');continue}
  const parentQ=new THREE.Quaternion();forearm.parent.getWorldQuaternion(parentQ);
  const axis=world.normalize().applyQuaternion(parentQ.invert()).normalize();
  FOREARM_FINGER_RIG.forearms.push({side,bone:forearm,axis});
 }
 model.traverse(bone=>{
  if(!bone.isBone||!/(finger|thumb|index|middle|ring|pinky|little)/i.test(bone.name))return;
  if(!original[bone.name])return;
  const children=bone.children.filter(c=>c.isBone);
  if(children.length!==1)return;
  const a=new THREE.Vector3(),b=new THREE.Vector3();
  bone.getWorldPosition(a);children[0].getWorldPosition(b);
  const direction=b.sub(a);
  if(direction.lengthSq()<1e-8)return;
  // Approximate bending axis: perpendicular to segment and rig forward (+Z).
  const forward=new THREE.Vector3(0,0,1);
  const axisWorld=new THREE.Vector3().crossVectors(direction.normalize(),forward);
  if(axisWorld.lengthSq()<1e-5)return;
  const parentQ=new THREE.Quaternion();bone.parent.getWorldQuaternion(parentQ);
  const axis=axisWorld.normalize().applyQuaternion(parentQ.invert()).normalize();
  FOREARM_FINGER_RIG.fingers.push({bone,axis,base:original[bone.name].clone()});
 });
 notes.push(FOREARM_FINGER_RIG.forearms.length+' Unterarme für vereinfachte Rotation');
 notes.push(FOREARM_FINGER_RIG.fingers.length+' Fingerknochen mit eindeutiger Segmentachse');
 document.getElementById('forearmFingerStatus').textContent=notes.join(' · ');
}
function applyForearmFingers(){
 const left=Number(document.getElementById('forearmL').value)||0;
 const right=Number(document.getElementById('forearmR').value)||0;
 const curl=Number(document.getElementById('fingerCurl').value)||0;
 document.getElementById('forearmLText').textContent=left+'°';
 document.getElementById('forearmRText').textContent=right+'°';
 document.getElementById('fingerCurlText').textContent=curl+'°';
 for(const j of FOREARM_FINGER_RIG.forearms){
  const angle=(j.side==='l'?left:right)*Math.PI/180;
  // Compose with elbow flexion rather than overwriting it.
  j.bone.quaternion.multiply(new THREE.Quaternion().setFromAxisAngle(j.axis,angle));
 }
 for(const j of FOREARM_FINGER_RIG.fingers){
  j.bone.quaternion.copy(new THREE.Quaternion().setFromAxisAngle(j.axis,curl*Math.PI/180)).multiply(j.base);
 }
}
for(const id of ['forearmL','forearmR','fingerCurl'])document.getElementById(id).addEventListener('input',apply);
document.getElementById('forearmFingerReset').addEventListener('click',()=>{
 for(const id of ['forearmL','forearmR','fingerCurl'])document.getElementById(id).value='0';
 apply();
});
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,js+needle,1)
needle="buildJointAtlas();configureAdditionalJoints();"
assert s.count(needle)==1
s=s.replace(needle,"buildJointAtlas();configureAdditionalJoints();configureForearmFingers();",1)
needle="  applyAdditionalJoints();"
assert s.count(needle)==1
s=s.replace(needle,"  applyAdditionalJoints();\n  applyForearmFingers();",1)
Path("rig-labor-v4.4.html").write_text(s,encoding="utf-8")
print("v4.4 built")

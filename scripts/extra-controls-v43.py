from pathlib import Path
s=Path("rig-labor-v4.2.html").read_text(encoding="utf-8")
assert "mapJointCandidates()" in s
s=s.replace("v4.2 – Gelenkzuordnung (Beta)","v4.3 – Zusätzliche Gelenksteuerung (Beta)")
needle='<p id="candidateSummary"'
assert s.count(needle)==1
panel='''<div style="padding:10px;margin:10px 0;border:1px solid #46748d;border-radius:8px"><strong>Neue Bewegungen · experimentell</strong><p style="font-size:12px">Bewegung nur bei vorhandenen Rig-Knochen. Neutralstellung entspricht der geladenen Modellpose; Achsen sind Näherungen, nicht klinisch validiert.</p><label>Halsrotation: <strong id="neckRotationText">0°</strong></label><input id="neckRotation" type="range" min="-60" max="60" value="0" style="width:100%"><label>Handgelenke beugen/strecken: <strong id="wristFlexText">0°</strong></label><input id="wristFlex" type="range" min="-60" max="60" value="0" style="width:100%"><label>Sprunggelenke bewegen: <strong id="ankleFlexText">0°</strong></label><input id="ankleFlex" type="range" min="-30" max="45" value="0" style="width:100%"><button type="button" id="newJointsReset">Neue Gelenke auf 0°</button><p id="newJointsStatus" role="status" style="font-size:12px;white-space:pre-line">Warte auf Rig …</p></div>'''
s=s.replace(needle,panel+needle,1)
js="""const ADDITIONAL_JOINTS={};
function findNamedBone(pattern){
 const all=JOINT_ATLAS.entries.filter(e=>pattern.test(e.name));
 return all.length===1?bones[all[0].name]:null;
}
function configureAdditionalJoints(){
 const specs=[
  ['neck','neck',/^(neck|neck_01|cervical)$/i,new THREE.Vector3(0,1,0)],
  ['wrist_l','wrist',/^(hand|wrist)_l$/i,new THREE.Vector3(1,0,0)],
  ['wrist_r','wrist',/^(hand|wrist)_r$/i,new THREE.Vector3(1,0,0)],
  ['ankle_l','ankle',/^(foot|ankle)_l$/i,new THREE.Vector3(1,0,0)],
  ['ankle_r','ankle',/^(foot|ankle)_r$/i,new THREE.Vector3(1,0,0)]
 ];
 const report=[];
 for(const [key,kind,pattern,worldAxis] of specs){
  const bone=findNamedBone(pattern);
  if(!bone||!bone.parent||!original[bone.name]){
   ADDITIONAL_JOINTS[key]={valid:false};report.push(key+': nicht eindeutig verfügbar');continue;
  }
  const q=new THREE.Quaternion();bone.parent.getWorldQuaternion(q);
  const axis=worldAxis.clone().applyQuaternion(q.invert()).normalize();
  ADDITIONAL_JOINTS[key]={valid:true,bone,base:original[bone.name].clone(),axis,kind};
  report.push(key+': Achse geschätzt');
 }
 document.getElementById('newJointsStatus').textContent=report.join(' · ');
}
function applyAdditionalJoints(){
 const values={
  neck:Number(document.getElementById('neckRotation').value)||0,
  wrist:Number(document.getElementById('wristFlex').value)||0,
  ankle:Number(document.getElementById('ankleFlex').value)||0
 };
 for(const [kind,id] of [['neck','neckRotationText'],['wrist','wristFlexText'],['ankle','ankleFlexText']]){
  document.getElementById(id).textContent=values[kind]+'°';
 }
 for(const joint of Object.values(ADDITIONAL_JOINTS)){
  if(!joint.valid)continue;
  const angle=values[joint.kind]*Math.PI/180;
  joint.bone.quaternion.copy(new THREE.Quaternion().setFromAxisAngle(joint.axis,angle)).multiply(joint.base);
 }
}
for(const id of ['neckRotation','wristFlex','ankleFlex']){
 document.getElementById(id).addEventListener('input',apply);
}
document.getElementById('newJointsReset').addEventListener('click',()=>{
 for(const id of ['neckRotation','wristFlex','ankleFlex'])document.getElementById(id).value='0';
 apply();
});
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,js+needle,1)
needle="buildJointAtlas();"
assert s.count(needle)==1
s=s.replace(needle,"buildJointAtlas();configureAdditionalJoints();",1)
needle="  applyExtraJoints();"
assert s.count(needle)==1
s=s.replace(needle,"  applyExtraJoints();\n  applyAdditionalJoints();",1)
Path("rig-labor-v4.3.html").write_text(s,encoding="utf-8")
print("v4.3 built: experimental neck wrist ankle controls")

from pathlib import Path

p = Path("rig-labor.html")
s = p.read_text(encoding="utf-8")
s = s.replace("Anatomie Motion 3D · v2.7.1", "Anatomie Motion 3D · v2.9 – automatische Ellenbogenkalibrierung", 1)
a = s.index("function apply(){if(!model)return;")
b = s.index("function load(){try{", a)
replacement = """const AUTO_JOINTS={};const ELBOW_MAX=135;
function autoCalibrate(){
  model.updateMatrixWorld(true);
  const front=new THREE.Vector3(0,0,1); // Model front: +Z, checked against initial front camera
  const rad=Math.PI/180;
  for(const side of ['l','r']){
    const upper=bones['upperarm_'+side],lower=bones['lowerarm_'+side],hand=bones['hand_'+side];
    if(!upper||!lower||!hand){AUTO_JOINTS[side]={valid:false,reason:'Knochen fehlen'};continue}
    const shoulder=new THREE.Vector3(),elbow=new THREE.Vector3(),wrist=new THREE.Vector3();
    upper.getWorldPosition(shoulder);lower.getWorldPosition(elbow);hand.getWorldPosition(wrist);
    const upperDir=elbow.clone().sub(shoulder),lowerDir=wrist.clone().sub(elbow);
    if(upperDir.length()<1e-5||lowerDir.length()<1e-5){AUTO_JOINTS[side]={valid:false,reason:'Knochenabstand zu klein'};continue}
    upperDir.normalize();lowerDir.normalize();
    const anterior=front.clone().addScaledVector(upperDir,-front.dot(upperDir));
    if(anterior.length()<.15){AUTO_JOINTS[side]={valid:false,reason:'Vorderachse nicht eindeutig'};continue}
    anterior.normalize();
    const axisWorld=new THREE.Vector3().crossVectors(upperDir,anterior).normalize();
    const parentWorld=new THREE.Quaternion();lower.parent.getWorldQuaternion(parentWorld);
    const inv=parentWorld.clone().invert();
    const alignWorld=new THREE.Quaternion().setFromUnitVectors(lowerDir,upperDir);
    const neutral=inv.clone().multiply(alignWorld).multiply(parentWorld).multiply(original['lowerarm_'+side]);
    const axisLocal=axisWorld.clone().applyQuaternion(inv);
    AUTO_JOINTS[side]={valid:true,neutral,axisLocal,upperDir:upperDir.clone(),anterior:anterior.clone(),hand,lower};
  }
  const good=['l','r'].every(side=>AUTO_JOINTS[side]?.valid);
  const el=document.getElementById('autostatus');
  if(el)el.textContent=good?'Automatische Kalibrierung aktiv: beide Ellenbogen, Neutralstellung 0°, Beugung 0–135°. Anatomische Richtung wird am Modell geprüft.':'Automatische Kalibrierung nicht eindeutig: '+['l','r'].filter(x=>!AUTO_JOINTS[x]?.valid).map(x=>x+': '+AUTO_JOINTS[x]?.reason).join('; ');
  return good;
}
function apply(){
  if(!model)return;
  const angle=Math.max(0,Math.min(ELBOW_MAX,Number($('angle').value)||0));
  $('angleText').textContent=angle+'°';
  for(const side of ['l','r']){
    const j=AUTO_JOINTS[side],bone=bones['lowerarm_'+side];
    if(!bone||!j?.valid)continue;
    bone.quaternion.copy(new THREE.Quaternion().setFromAxisAngle(j.axisLocal,angle*Math.PI/180)).multiply(j.neutral);
  }
  model.updateMatrixWorld(true);
}
"""
s=s[:a]+replacement+s[b:]
# call auto calibration once after model bones are collected and matrices updated
needle="model.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(model);"
assert s.count(needle)==1
s=s.replace(needle,"model.updateMatrixWorld(true);autoCalibrate();const box=new THREE.Box3().setFromObject(model);",1)
# old manual controls remain in source for backward compatibility, but are hidden for v2.9
needle="<label>Gemeinsamer anatomischer Beugewinkel:"
assert needle in s
s=s.replace(needle,'<p id="autostatus" role="status" style="color:#ffcb05">Analysiere Knochenachsen automatisch …</p><label>Gemeinsamer anatomischer Beugewinkel:',1)
# remove calibration UI (do not remove event handlers for backwards compatibility)
start=s.index('<div class="row"><div><label>Linker Ellenbogen · lokale Achse')
end=s.index('</small></p>',start)+len('</small></p>')
s=s[:start]+'<div style="display:none" aria-hidden="true">'+s[start:end]+'</div>'+s[end:]
# Set status explicitly to distinguish model loaded vs verified
s=s.replace("Modell geladen – Ellenbogenregler bereit.","Modell geladen – automatische Gelenkkalibrierung bereit.",1)
Path("rig-labor-v2.9.html").write_text(s,encoding="utf-8")
print("v2.9 auto-calibration page built; left/right neutral and flexion axis computed from rig.")

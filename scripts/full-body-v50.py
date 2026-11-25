from pathlib import Path
s=Path("rig-labor-v4.7.html").read_text(encoding="utf-8")
assert "JOINT_ATLAS" in s and "testMotionDirections" in s
s=s.replace("v4.7 – Winkelreaktion prüfen (Beta)","v5.0 – Ganzkörper-Gelenklabor (Beta)")
needle='<p id="candidateSummary"'
assert s.count(needle)==1
panel='''<section style="padding:10px;margin:10px 0;border:2px solid #08a9ef;border-radius:10px"><h3>Ganzkörper-Gelenklabor v5.0</h3><p style="font-size:12px">Zentrale Übersicht der verfügbaren Gelenke. Die App zeigt nur Bewegungen an, für die im geladenen Modell passende Knochen erkannt wurden. Vorhandene Regler bleiben in den jeweiligen Abschnitten darunter.</p><div id="fullBodyOverview" role="status">Analysiere Gelenke …</div><div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0"><button type="button" id="fullBodyNeutral">Alle Gelenke neutral (0°)</button><button type="button" id="fullBodyRefresh">Gelenkstatus aktualisieren</button></div><p style="font-size:12px">Nicht vorhanden: echte Radius-/Ulna-Rotation, zusätzliche Fingersegmente oder andere anatomische Freiheitsgrade, die das Rig nicht enthält. Keine medizinische Validierung.</p></section>'''
s=s.replace(needle,panel+needle,1)
js="""const FULL_BODY_CONTROLS=[
 ['Ellenbogen links/rechts','angle',()=>['l','r'].filter(x=>AUTO_JOINTS[x]?.valid).length],
 ['Knie links/rechts','kneeAngle',()=>['l','r'].filter(x=>EXTRA_JOINTS['knee_'+x]?.valid).length],
 ['Hüfte links/rechts','hipAngle',()=>['l','r'].filter(x=>EXTRA_JOINTS['hip_'+x]?.valid).length],
 ['Schulter links/rechts','shoulderAngle',()=>['l','r'].filter(x=>EXTRA_JOINTS['shoulder_'+x]?.valid).length],
 ['Halsrotation','neckRotation',()=>ADDITIONAL_JOINTS.neck?.valid?1:0],
 ['Handgelenke','wristFlex',()=>['l','r'].filter(x=>ADDITIONAL_JOINTS['wrist_'+x]?.valid).length],
 ['Sprunggelenke','ankleFlex',()=>['l','r'].filter(x=>ADDITIONAL_JOINTS['ankle_'+x]?.valid).length],
 ['Unterarm links','forearmL',()=>FOREARM_FINGER_RIG.forearms.some(x=>x.side==='l')?1:0],
 ['Unterarm rechts','forearmR',()=>FOREARM_FINGER_RIG.forearms.some(x=>x.side==='r')?1:0],
 ['Finger','fingerCurl',()=>FOREARM_FINGER_RIG.fingers.length]
];
function renderFullBodyOverview(){
 const root=document.getElementById('fullBodyOverview');if(!root)return;
 root.replaceChildren();
 for(const [label,id,countFn] of FULL_BODY_CONTROLS){
  const input=document.getElementById(id),count=countFn();
  const row=document.createElement('div');row.style.cssText='border-bottom:1px solid #31516a;padding:6px 0;font-size:13px;display:flex;justify-content:space-between;gap:8px';
  const name=document.createElement('span');name.textContent=label;
  const status=document.createElement('strong');status.textContent=count?(count+' Knochen · experimentell'):'Nicht verfügbar';
  status.style.color=count?'#8bd8ff':'#ffcb05';
  row.append(name,status);root.appendChild(row);
  if(input){input.disabled=!count;input.title=count?'Experimentelle Bewegung':'Passende Rig-Knochen fehlen';}
 }
}
document.getElementById('fullBodyRefresh').addEventListener('click',()=>{
 renderFullBodyOverview();auditRigAxes();
});
document.getElementById('fullBodyNeutral').addEventListener('click',()=>{
 for(const [,id] of FULL_BODY_CONTROLS){
  const input=document.getElementById(id);if(input)input.value='0';
 }
 apply();
 renderFullBodyOverview();
});
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,js+needle,1)
needle="configureForearmFingers();auditRigAxes();"
assert s.count(needle)==1
s=s.replace(needle,"configureForearmFingers();auditRigAxes();renderFullBodyOverview();",1)
Path("rig-labor-v5.0.html").write_text(s,encoding="utf-8")
print("v5.0 full-body beta overview generated")

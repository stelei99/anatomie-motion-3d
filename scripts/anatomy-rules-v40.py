from pathlib import Path
s=Path("rig-labor-v3.1.html").read_text(encoding="utf-8")
assert "measureKnees()" in s
s=s.replace("v3.1 – Knie-Winkelmessung (Beta)","v4.0 – Anatomische Bewegungsregeln (Beta)")
rules="""// Anatomical motion definitions: reference ranges, not personal clinical limits.
// Model axes and neutral poses must be validated against anatomical landmarks.
const ANATOMY_RULES=Object.freeze({
 elbow:{label:'Ellenbogen',min:0,max:135,plane:'sagittal',degreesOfFreedom:['flexion'],status:'experimental'},
 knee:{label:'Knie',min:0,max:120,plane:'sagittal',degreesOfFreedom:['flexion'],status:'experimental'},
 hip:{label:'Hüfte',min:0,max:90,plane:'sagittal',degreesOfFreedom:['flexion'],status:'experimental'},
 shoulder:{label:'Schulter',min:0,max:90,plane:'sagittal',degreesOfFreedom:['flexion'],status:'experimental'}
});
function validateAnatomicalTargets(){
 const checks=[];
 for(const [kind,rule] of Object.entries(ANATOMY_RULES)){
  const input=document.getElementById(kind==='elbow'?'angle':kind+'Angle');
  if(!input){checks.push(rule.label+': Regler fehlt');continue}
  input.min=rule.min;input.max=rule.max;
  const raw=Number(input.value);
  if(!Number.isFinite(raw)){input.value=rule.min;checks.push(rule.label+': ungültiger Winkel korrigiert')}
  else if(raw<rule.min||raw>rule.max){input.value=Math.max(rule.min,Math.min(rule.max,raw));checks.push(rule.label+': auf Bewegungsbereich begrenzt')}
 }
 return checks;
}
function checkKneeAgreement(){
 const target=Number(document.getElementById('kneeAngle')?.value)||0;
 const out=document.getElementById('ruleStatus');
 if(!out)return;
 const messages=validateAnatomicalTargets();
 for(const side of ['l','r']){
  const node=document.getElementById(side==='l'?'kneeMeasuredL':'kneeMeasuredR');
  const measured=Number.parseFloat(node?.textContent||'');
  if(!Number.isFinite(measured)){messages.push('Knie '+side.toUpperCase()+': keine Messung');continue}
  const diff=Math.abs(measured-target);
  if(diff>10)messages.push('Knie '+side.toUpperCase()+': Abweichung '+diff.toFixed(1)+'° – Kalibrierung erforderlich');
 }
 out.textContent=messages.length?messages.join(' · '):'Beide Knie innerhalb ±10° des Sollwerts (Rig-Messung; keine klinische Validierung).';
}
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,rules+needle,1)
needle="  measureKnees();"
assert s.count(needle)==1
s=s.replace(needle,"  measureKnees();\n  checkKneeAgreement();",1)
needle='<p id="jointDiagnostics"'
assert s.count(needle)==1
s=s.replace(needle,'<div style="padding:10px;border:1px solid #ffcb05;border-radius:8px;margin:8px 0"><strong>Anatomische Regelprüfung (Beta)</strong><p id="ruleStatus" role="status" style="font-size:12px">Warte auf Winkelmessung …</p><small>Regelgrenzen sind Referenzwerte. Die Achsenkalibrierung ist noch nicht anatomisch validiert. Bei Abweichungen wird gewarnt, nicht automatisch eine falsche Korrektur erzwungen.</small></div>'+needle,1)
Path("rig-labor-v4.0.html").write_text(s,encoding="utf-8")
print("v4.0 anatomical rule checks generated")

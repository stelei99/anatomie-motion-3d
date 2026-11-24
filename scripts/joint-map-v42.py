from pathlib import Path
s=Path("rig-labor-v4.1.html").read_text(encoding="utf-8")
assert "JOINT_ATLAS" in s
s=s.replace("v4.1 – Automatischer Gelenkatlas (Beta)","v4.2 – Gelenkzuordnung (Beta)")
needle='<p id="atlasSummary"'
assert s.count(needle)==1
s=s.replace(needle,'''<p style="font-size:12px">Automatische Kandidatenerkennung für Hals, Unterarmdrehung, Handgelenk, Sprunggelenk und Finger. Nur vorhandene Knochen werden berücksichtigt. Kandidaten sind noch nicht anatomisch validiert.</p><p id="candidateSummary" role="status">Analysiere mögliche Gelenke …</p><div id="candidateRows" style="margin:8px 0;max-height:280px;overflow:auto"></div>'''+needle,1)
code="""const JOINT_CANDIDATES=[];
const CANDIDATE_DEFINITIONS=[
 {id:'neck',label:'Halswirbelsäule',pattern:/^(neck|neck_\d+|cervical(?:_\d+)?)$/i,motions:['Beugung/Streckung','Rotation','Seitneigung'],region:'head'},
 {id:'forearm',label:'Unterarmrotation',pattern:/^(lowerarm|forearm)_[lr]$/i,motions:['Pronation/Supination'],region:'arm'},
 {id:'wrist',label:'Handgelenk',pattern:/^(hand|wrist)_[lr]$/i,motions:['Palmar-/Dorsalflexion','Radial-/Ulnarduktion'],region:'hand'},
 {id:'ankle',label:'Sprunggelenk',pattern:/^(foot|ankle)_[lr]$/i,motions:['Dorsal-/Plantarflexion'],region:'foot'},
 {id:'fingers',label:'Finger und Daumen',pattern:/(finger|thumb|index|middle|ring|pinky|little)/i,motions:['Fingerbeugung/Streckung (je nach Rig)'],region:'hand'}
];
function mapJointCandidates(){
 JOINT_CANDIDATES.length=0;
 const entries=JOINT_ATLAS.entries;
 for(const definition of CANDIDATE_DEFINITIONS){
  const matches=entries.filter(e=>definition.pattern.test(e.name));
  JOINT_CANDIDATES.push({id:definition.id,label:definition.label,region:definition.region,
    bones:matches.map(e=>e.name),motions:definition.motions,
    state:matches.length?'Kandidaten gefunden – Achsen nicht validiert':'Keine passenden Rig-Knochen erkannt'});
 }
 const container=document.getElementById('candidateRows');container.replaceChildren();
 for(const candidate of JOINT_CANDIDATES){
  const el=document.createElement('div');el.style.cssText='padding:8px 0;border-bottom:1px solid #31516a;font-size:12px';
  const name=document.createElement('strong');name.textContent=candidate.label;
  const detail=document.createElement('div');
  detail.textContent=candidate.state+' · '+(candidate.bones.join(', ')||'–')+' · Bewegungen: '+candidate.motions.join(', ');
  el.append(name,detail);container.appendChild(el);
 }
 const found=JOINT_CANDIDATES.filter(x=>x.bones.length).length;
 document.getElementById('candidateSummary').textContent=found+'/'+JOINT_CANDIDATES.length+' Gelenkgruppen mit passenden Knochen erkannt. Noch keine neuen Bewegungen aktiviert.';
}
"""
needle="function buildJointAtlas(){"
assert s.count(needle)==1
s=s.replace(needle,code+needle,1)
needle=" JOINT_ATLAS.generatedAt=new Date().toISOString();\n renderJointAtlas();"
assert s.count(needle)==1
s=s.replace(needle," JOINT_ATLAS.generatedAt=new Date().toISOString();\n mapJointCandidates();\n renderJointAtlas();",1)
needle="JSON.stringify({version:'4.1',...JOINT_ATLAS},null,2)"
assert s.count(needle)==1
s=s.replace(needle,"JSON.stringify({version:'4.2',...JOINT_ATLAS,jointCandidates:JOINT_CANDIDATES},null,2)",1)
Path("rig-labor-v4.2.html").write_text(s,encoding="utf-8")
print("v4.2 anatomical joint candidate map generated")

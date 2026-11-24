from pathlib import Path
s=Path("rig-labor-v4.0.html").read_text(encoding="utf-8")
assert "ANATOMY_RULES" in s
s=s.replace("v4.0 – Anatomische Bewegungsregeln (Beta)","v4.1 – Automatischer Gelenkatlas (Beta)")
atlas_panel='''<section style="padding:12px;margin:12px 0;border:1px solid #39708b;border-radius:10px;background:#092b43"><h3>Automatischer Gelenkatlas · Rig-Inventar</h3><p style="font-size:13px">Erkennt alle Knochen des geladenen Modells, ordnet sie Körperregionen zu und zeigt an, welche Bewegungen bereits gesteuert werden. Knochen sind nicht gleich anatomische Gelenke.</p><p id="atlasSummary" role="status">Modell wird analysiert …</p><label for="atlasFilter">Körperregion</label><select id="atlasFilter" style="width:100%"><option value="all">Alle Regionen</option><option value="head">Kopf und Hals</option><option value="spine">Rumpf und Becken</option><option value="arm">Schultern und Arme</option><option value="hand">Hände und Finger</option><option value="leg">Hüfte und Beine</option><option value="foot">Füße und Zehen</option><option value="other">Nicht zugeordnet</option></select><div id="atlasRows" style="max-height:340px;overflow:auto;margin-top:10px"></div><button type="button" id="atlasExport" style="margin-top:8px">Rig-Inventar als JSON exportieren</button><p style="font-size:11px">Die Inventarisierung ist automatisch; die Zuordnung basiert auf Knochennamen. Anatomische Achsen und Bewegungsgrenzen bleiben gesondert zu validieren.</p></section>'''
needle='<p id="autostatus"'
assert s.count(needle)==1
s=s.replace(needle,atlas_panel+needle,1)
code="""const JOINT_ATLAS={entries:[],modelName:'',generatedAt:''};
function classifyRigBone(name){
 const n=name.toLowerCase();
 if(/finger|thumb|index|middle|ring|pinky|metacarp|hand/.test(n))return 'hand';
 if(/toe|foot|heel|ball/.test(n))return 'foot';
 if(/thigh|calf|shin|knee|leg/.test(n))return 'leg';
 if(/upperarm|lowerarm|forearm|clavicle|shoulder|scapula|arm/.test(n))return 'arm';
 if(/head|neck|jaw|eye/.test(n))return 'head';
 if(/spine|pelvis|hip|root|chest|abdomen/.test(n))return 'spine';
 return 'other';
}
function rigMovementStatus(name){
 const n=name.toLowerCase();
 if(/^lowerarm_[lr]$/.test(n))return 'Ellenbogenbeugung · experimentell';
 if(/^calf_[lr]$/.test(n))return 'Kniebeugung · experimentell';
 if(/^thigh_[lr]$/.test(n))return 'Hüftbeugung · experimentell';
 if(/^upperarm_[lr]$/.test(n))return 'Schultervorhebung · experimentell';
 return 'Bewegung noch nicht eingerichtet';
}
function buildJointAtlas(){
 if(!model)return;
 const entries=[];
 model.updateMatrixWorld(true);
 model.traverse(o=>{
  if(!o.isBone)return;
  const pos=new THREE.Vector3();o.getWorldPosition(pos);
  entries.push({name:o.name||'(unbenannt)',parent:o.parent?.name||null,region:classifyRigBone(o.name||''),position:pos.toArray().map(v=>Number(v.toFixed(5))),movement:rigMovementStatus(o.name||'')});
 });
 entries.sort((a,b)=>a.region.localeCompare(b.region)||a.name.localeCompare(b.name));
 JOINT_ATLAS.entries=entries;
 JOINT_ATLAS.modelName=model.name||'GLB-Rig';
 JOINT_ATLAS.generatedAt=new Date().toISOString();
 renderJointAtlas();
}
function renderJointAtlas(){
 const entries=JOINT_ATLAS.entries,region=document.getElementById('atlasFilter')?.value||'all';
 const visible=entries.filter(e=>region==='all'||e.region===region);
 const mapped=entries.filter(e=>e.region!=='other').length;
 const active=entries.filter(e=>!e.movement.startsWith('Bewegung noch')).length;
 document.getElementById('atlasSummary').textContent=entries.length+' Rig-Knochen gefunden · '+mapped+' Körperregion zugeordnet · '+active+' experimentell gesteuerte Knochen. Keine automatische anatomische Validierung.';
 const root=document.getElementById('atlasRows');root.replaceChildren();
 for(const entry of visible){
  const row=document.createElement('div');
  row.style.cssText='border-bottom:1px solid #31516a;padding:7px 0;font-size:12px';
  const title=document.createElement('strong');title.textContent=entry.name;
  const desc=document.createElement('div');desc.textContent='Elternknochen: '+(entry.parent||'–')+' · '+entry.movement;
  row.append(title,desc);root.appendChild(row);
 }
 if(!visible.length)root.textContent='Keine Knochen in dieser Region gefunden.';
}
function exportJointAtlas(){
 const blob=new Blob([JSON.stringify({version:'4.1',...JOINT_ATLAS},null,2)],{type:'application/json'});
 const url=URL.createObjectURL(blob),a=document.createElement('a');
 a.href=url;a.download='anatomie-motion-rig-inventar.json';a.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
}
document.getElementById('atlasFilter').addEventListener('change',renderJointAtlas);
document.getElementById('atlasExport').addEventListener('click',exportJointAtlas);
"""
needle="function measureKnees(){"
assert s.count(needle)==1
s=s.replace(needle,code+needle,1)
needle="autoCalibrate();inferExtraJoints();"
assert s.count(needle)==1
s=s.replace(needle,"autoCalibrate();inferExtraJoints();buildJointAtlas();",1)
Path("rig-labor-v4.1.html").write_text(s,encoding="utf-8")
print("v4.1 full rig atlas created")

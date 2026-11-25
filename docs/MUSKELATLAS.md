# Anatomie Motion 3D – Anatomischer Muskelatlas (Variante A)

Stand: 2026-11-25 · Status: **Phase 1 als separater statischer Atlas-Prototyp umgesetzt**; noch keine Kopplung der Muskelmeshes an das bewegliche 53-Knochen-Rig.

## Ziel
Die bestehende animierte Figur mit 53 Rig-Knochen bleibt als Bewegungsgrundlage. Darüber werden echte, individuell segmentierte 3D-Muskeloberflächen gelegt, die bei der Kniebeuge mit dem Skelett deformiert werden. Das Muskelmodell ist eine **eigene anatomische Ebene**, nicht bloß eine Farbmarkierung auf der Haut.

## Verbindliche Anforderungen
- Separate schaltbare Ebenen: Haut / Muskulatur / Skelett.
- Jeder Muskel mit eindeutiger ID, deutscher und lateinischer Bezeichnung, Körperseite, 3D-Mesh und eigener Materialinstanz.
- Alle Muskelmeshes müssen zum vorhandenen 53-Knochen-Rig registriert und geskinnt werden. Haut und Muskelmeshes dürfen sich bei Bewegungen nicht sichtbar ablösen.
- Farben: Hauptbeteiligung dunkelrot (#A72A34), unterstützend/stabilisierend hellrot (#ED9298), sonst grau (#A9B1BA).
- Beteiligung ist **qualitativ und übungsphasenabhängig**; keine behaupteten EMG-Prozentwerte oder exakten Muskelkräfte.
- Links und rechts separat auswählbar. Ein Muskel kann durch Antippen hervorgehoben und mit Funktion und Bewegung erklärt werden.
- Mobil nutzbar (Android) und Windows im Browser; Performance-Budget und LOD vorsehen.
- Bei fehlendem oder inkompatiblem Anatomie-Asset einen deutlichen Hinweis zeigen, nicht eine falsche Darstellung als realistisch ausgeben.

## Datenstruktur pro Muskel
```json
{
  "id": "vastus_lateralis_l",
  "latin": "Musculus vastus lateralis",
  "de": "Äußerer breiter Oberschenkelmuskel",
  "side": "left",
  "meshNode": "muscle_vastus_lateralis_l",
  "skinJoints": ["thigh_l", "calf_l"],
  "actions": ["knee_extension"],
  "squat": {"down": "support", "up": "primary", "hold": "primary"}
}
```

## Gesamtumfang: vollständiger Muskelatlas des Körpers

Das Zielmodell umfasst alle größeren oberflächlichen und relevanten tiefen Skelettmuskeln, jeweils links/rechts getrennt, soweit anatomisch vorhanden. Keine Beschränkung auf Kniebeugenmuskeln.

| Region | Erforderliche Bereiche (Auswahl, nicht abschließend) |
|---|---|
| Kopf und Hals | Mimische Muskulatur, Kaumuskeln, Sternocleidomastoideus, Skalenusgruppe, tiefe Halsmuskulatur |
| Schultergürtel | Trapezius, Deltoideus, Rotatorenmanschette, Serratus anterior, Rhomboiden, Levator scapulae |
| Brust und Rücken | Pectoralis major/minor, Latissimus dorsi, Erector spinae, Multifidi, tiefe Rückenmuskulatur |
| Bauch und Becken | Rectus abdominis, Obliquus externus/internus, Transversus abdominis, Iliopsoas, Beckenboden (separate Tiefenschicht) |
| Oberarm, Unterarm, Hand | Bizeps, Brachialis, Trizeps, Pronatoren/Supinatoren, Flexoren/Extensoren, intrinsische Handmuskeln |
| Gesäß und Hüfte | Gluteus maximus/medius/minimus, tiefe Außenrotatoren, Tensor fasciae latae |
| Oberschenkel | Quadrizepsköpfe, Hamstrings, Adduktoren, Sartorius, Gracilis |
| Unterschenkel und Fuß | Gastrocnemius, Soleus, Tibialis anterior/posterior, Fibularisgruppe, Zehenflexoren/-extensoren, intrinsische Fußmuskeln |

**Anatomische Genauigkeit:** Mehrschichtige Ansicht (oberflächlich/mittel/tief) mit Ausblenden einzelner Muskeln; Sehnen und Faszien als separat gekennzeichnete Strukturen, nicht als Muskeln behandeln. Links/rechts spiegeln nur, wo die Anatomie es rechtfertigt. Ursprung, Ansatz und Funktion sind Metadaten, nicht automatisch aus einem 53-Knochen-Rig ableitbar.

**Rig-Grenze:** 53 Knochen reichen nicht für die eigenständige, anatomisch präzise Bewegung aller kleinen Muskeln und knöchernen Strukturen (z. B. Schulterblatt, Finger, Hals). Für diese Regionen ist eine erweiterte Rig-Hierarchie oder zusätzliche Deformationssteuerung erforderlich. Der bestehende Kniebeugen-Prototyp darf dadurch nicht beschädigt werden.

**Lieferphasen:** (1) lizenzgeprüftes segmentiertes Ganzkörper-Asset, (2) Ganzkörper-Atlas mit Auswahl/Schichten in Ruhepose, (3) Registrierung an bestehendes Rig und Animation der großen Muskeln, (4) erweiterte Gelenke/Deformation für Hände, Hals, Schultergürtel und tiefe Muskeln, (5) weitere Übungen und Validierung auf Android/Windows. Vollständige anatomische Abdeckung ist das Ziel der Architektur, nicht der aktuelle Implementierungsstand.

## Erste Muskelgruppen für die Kniebeuge
| Muskeln | Funktion bei Kniebeuge | Anzeige |
|---|---|---|
| Vastus lateralis/medialis/intermedius, rectus femoris | Kniestreckung, exzentrische Kontrolle beim Absenken | Hauptbeteiligung |
| Gluteus maximus | Hüftstreckung, exzentrische Kontrolle beim Absenken | Hauptbeteiligung |
| Adductor magnus (hinterer Anteil) | Hüftstreckung, besonders aus tiefer Hüftbeugung | Hauptbeteiligung/unterstützend je nach Phase |
| Soleus, gastrocnemius | Kontrolle des Sprunggelenks und Stabilisierung | Unterstützend |
| Hamstrings | Hüftstreckung und Stabilisierung; keine pauschale Einstufung als stärkster Kniestrecker | Unterstützend |
| Erector spinae, Bauchwand | Rumpfstabilisierung | Stabilisierend |
| Gluteus medius/minimus | Becken- und Hüftstabilisierung | Stabilisierend |

Hinweis: „Hauptbeteiligung“ ist eine didaktische, qualitative Kategorie, keine Muskelaktivitätsmessung. Muskelaktivität variiert mit Technik, Tiefe, Last, Person und Phase.

## Implementierungsstand 25.11.2026
- `muskelatlas.html` angelegt: 3D-Ganzkörper-Atlas mit getrennt auswählbaren Muskelmeshes, Suche, Regionenauswahl und didaktischer Kniebeugen-Farbgebung.
- Quelle: `organui/muscles-3d`, `public/models/muscles.glb` (BodyParts3D, CC BY-SA 2.1 Japan); derzeit per jsDelivr geladen, nicht als eigene Assetkopie abgelegt.
- **v3.1 (experimentell):** `muskelatlas.html` hat nun einen Kniebeugen-Regler, Play/Pause, Aufrichten und umkehrbare Beugerichtung. Die einzelnen anatomischen Meshes werden im GPU-Vertexshader durch ein vereinfachtes, gemeinsames Hüft-/Knie-/Sprunggelenkmodell verformt. **Das ist eine optische Demonstration, noch keine anatomisch korrekte individuelle Muskelskinning-Lösung.** Insbesondere ist das Modell nicht an das 53-Knochen-Rig gekoppelt; Gelenkachsen und Knieposition sind nur aus dem Modell-Bounding-Box angenähert. Deformationen, Durchdringungen, Muskelursprünge/-ansätze und mobile Performance müssen visuell geprüft werden.
- **Noch offen:** Browser-Funktionstest und zuverlässiger CDN-Abruf, Anatomie-Qualitätsprüfung, deutsch-lateinische Muskelnamen, Rig-Registrierung, Skinning, Bewegungsphasen, vollständige Schichten Haut/Skelett und Fersenkontakt.
- Die Auswahl umfasst Muskeln und Sehnen; diese müssen bei späterer fachlicher Katalogisierung getrennt werden.

## Technischer Integrationsplan
1. **Asset-Auswahl und Lizenzprüfung:** ein anatomisch detailliertes Muskelmodell mit klar benannten separaten Muskeln und erlaubter Nutzung finden/erstellen. GLB/glTF bevorzugt. Keine unklare Lizenz oder Meshes ohne Herkunft.
2. **Rig-Registrierung:** Maßstab, Achsen, Bindpose, Gelenkzentren und Haut-/Muskelgeometrie auf das vorhandene 53-Knochen-Rig abstimmen.
3. **Skinning und Validierung:** je Muskel Gewichte, Gelenkdeformationen und Durchdringungen bei 0°, 90°, 120°, 135° Kniebeugung prüfen.
4. **Atlas-Oberfläche:** Ebenenumschalter, Muskelwahl, Legende, Seitenfilter, Übungsphase.
5. **Ansteuerung:** Übungsmetadaten auf Muskelmaterialien abbilden; keine erfundenen Kräfte oder „KI-gemessene“ Aktivität.
6. **Erweiterbarkeit:** RDL, Ausfallschritt, Wadenheben, Liegestütz mit demselben Muskelregister.

## Abnahmekriterien
- Alle sichtbaren Muskeln sind individuell identifizierbar und anatomisch plausibel positioniert.
- Keine Ablösung der Muskeln bei Kniebeuge und keine auffälligen Haut-/Muskel-Durchdringungen.
- Die Haut lässt sich ausblenden, ohne die Bewegung anzuhalten.
- Links und rechts getrennte Muskelwahl und identische Muskel-IDs.
- Keine Muskelaktivität wird als direkt gemessen ausgegeben.
- Windows und Android visuell geprüft.

## Aktuelle Einschränkung
Das im Repository verwendete Original-GLB stellt eine geriggte **Körperoberfläche**, kein separat segmentiertes Muskelmodell bereit. Für Variante A ist deshalb ein zusätzliches geeignetes Anatomie-Asset mit einzeln modellierten Muskeln erforderlich. Ein reines Einfärben der bisherigen Haut oder schematische Zylinder wäre **nicht** die vereinbarte Variante A.

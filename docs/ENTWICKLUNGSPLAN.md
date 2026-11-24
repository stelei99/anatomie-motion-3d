# Entwicklungsplan – Anatomie Motion 3D

## Ziel
Kostenlose Web-App für Windows und Android zur interaktiven Darstellung menschlicher Anatomie und von Kraftübungen. Geplant sind die Ebenen Haut, Muskulatur, Skelett und kombinierte Ansicht sowie auswählbare anatomische Strukturen.

## Bisheriger Stand (lokaler Prototyp 2.7.1)
- Anatomischer Muskelatlas als HTML-Prototyp vorhanden.
- Schematische Liegestütz-Demo auf Android getestet; die Bewegung wurde vom Nutzer als korrekt bestätigt.
- Ganzkörper-GLB mit 53 Rig-Knochen und einer verformbaren Körperoberfläche lokal erfolgreich angezeigt.
- Ellenbogensteuerung im Rig-Labor experimentell, Achsen und Ausgangsstellungen noch nicht kalibriert.
- Einzelne realistische Muskeln noch nicht mit dem Rig verbunden.

**Wichtig:** Die genannten lokalen Prototyp-Dateien sind noch nicht Teil dieses GitHub-Repositories. Dieses Dokument ist kein Nachweis einer bereits veröffentlichten Web-App.

## Technische Schritte
1. Quellcode und Assets des getesteten lokalen Stands in nachvollziehbare Dateien überführen.
2. Browserstart über GitHub Pages testen; relative Asset-Pfade und Ladefehler behandeln.
3. Rig-Bindepose und lokale Knochenachsen aus den tatsächlichen GLB-Daten bestimmen.
4. Gelenkgrenzen einführen (Ellenbogen als Standardmodell 0–145° Flexion; individuelle Anatomie kann abweichen).
5. Validierte Bewegungssteuerung der schematischen Liegestütze auf das Rig übertragen.
6. Anatomische Muskelmeshes mit geprüfter Lizenz und korrekten Zuordnungen integrieren.
7. Haut, Muskulatur und Skelett an ein gemeinsames Rig binden.
8. Automatisierte Prüfungen für Gelenkgrenzen, Mesh-Namen und Modellladen ergänzen.

## Qualitätsregeln
- Keine biomechanische Validierung behaupten, solange sie nicht nachgewiesen ist.
- Einzelne Meshes nicht automatisch mit einzelnen anatomischen Muskeln gleichsetzen.
- Herkunft, Lizenz und Attribution jedes externen Assets dokumentieren.
- Android und Windows bei jeder größeren Änderung testen.

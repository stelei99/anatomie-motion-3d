# Automatische Gelenkkalibrierung – Version 2.9

## Ziel
Anatomische Winkel und Modellrotationen strikt trennen. Gleiche anatomische Winkel gelten links/rechts; lokale Achsen, Neutralrotationen und Vorzeichen werden pro Gelenk aus dem Rig ermittelt und validiert.

## Auswertung
1. GLB-Bones, Hierarchie, lokale Bind-Quaternions und Welttransformationen auslesen.
2. Für jeden Ellenbogen die Richtungen Oberarm→Ellenbogen und Ellenbogen→Handgelenk in der Bind-Pose bestimmen. Bei fehlenden Landmarken den Knochenachsen aus Bind-Matrizen folgen und die Zuverlässigkeit kennzeichnen.
3. Neutralstellung als anatomischen Winkel zwischen Ober- und Unterarmsegment bestimmen; Modell-Bind-Pose nicht mit anatomischen 0° gleichsetzen.
4. Kandidatenachsen im lokalen Unterarm-Koordinatensystem aus der Ebene von Oberarm und Unterarm ableiten; links und rechts unabhängig berechnen. Spiegelung anhand der Körpermittellinie erkennen.
5. Kandidaten bei 0°, 45°, 90° und 135° simulieren. Prüfen, ob die Beugung monoton ist, der Unterarm zum Oberarm führt und keine Rückwärtsbeugung entsteht.
6. Bei unklarer Anatomie keine scheinbar sichere Autokalibrierung: Fehlerdiagnose und optional einmalige manuelle Korrektur; kalibrierte Werte dauerhaft speichern.

## Anatomische Regeln
- Ellenbogen: Flexion 0–135° als konservativer Testbereich; klinischer Bewegungsumfang ist individuell und oft größer.
- 0°: nahezu gestreckter Ellenbogen; 90°: rechtwinklige Beugung.
- Kein negatives Flexionsziel; keine unkontrollierte Hyperextension.
- Anatomische Winkel sind für beide Seiten gleich; technische Transformationswerte können verschieden sein.
- Schulterposition und Ellenbogenflexion unabhängig behandeln.

## Akzeptanztests
- Linker und rechter Ellenbogen bei 0° ohne sichtbare Restbeugung.
- Beide Seiten bei 90° in anatomisch richtiger Beugerichtung.
- Vorder-, Seiten- und Rückansicht.
- Rückkehr zu 0° ohne Drift; Animation bleibt im erlaubten Bereich.
- Falls automatische Kalibrierung nicht verlässlich: explizite Warnung statt stillschweigend falscher Bewegung.

## Umsetzungsreihenfolge
1. Diagnosemodul (Knochenhierarchie, Bind-Pose, Achsen, Winkel, Konfidenz) ohne Veränderung der funktionierenden v2.8.
2. Automatische Achsen-/Nullstellungserkennung.
3. Anatomische Tests, links/rechts.
4. Freigabe der automatischen Steuerung erst nach bestandenen Tests.

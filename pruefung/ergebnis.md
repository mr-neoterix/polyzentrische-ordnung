# Ergebnis der Friedensprüfung

**Durchgeführt am 15.08.2026** nach der Vorregistrierung in `praeregistrierung.md`, die vor der ersten Schätzung angelegt und seither nicht geändert wurde. Skript: `analyse.py`. Rohausgabe: `ausgabe.txt`. Koeffiziententabelle: `ergebnisse.csv`.

---

## Das Ergebnis in einem Satz

Nach der vorher festgelegten Regel ist die These **nicht gestützt** – und der Grund dafür ist nicht, dass das Vorzeichen falsch wäre, sondern dass es sich in keiner Rechnung von der Null trennen lässt.

## Grundgesamtheit

Panel 1946 bis 2010: 8.843 Staat-Jahre in 180 Staaten. Davon führt V-Dem 3.141 Staat-Jahre in 111 Staaten als Wahldemokratie oder liberale Demokratie; das ist die Gruppe, innerhalb derer gemessen wird. Die Verteilungsgröße `v2pepwrses` liegt in dieser Gruppe bei einem Mittel von 1,181 und einer Standardabweichung von 0,756. Die abhängige Variable – Initiierung einer militarisierten Auseinandersetzung im Folgejahr – tritt in 299 der 3.029 auswertbaren Staat-Jahre ein, also in knapp zehn Prozent.

## Die Schätzungen

Angegeben ist der Koeffizient der standardisierten Verteilungsgröße, der Standardfehler nach Staat geclustert, der p-Wert und die relative Änderung der mittleren vorhergesagten Wahrscheinlichkeit bei einer Erhöhung um eine Standardabweichung.

| Modell | N | Ereignisse | b | SE | p | Effekt |
|---|---:|---:|---:|---:|---:|---:|
| **Hauptmodell** – Initiierung (GML), t+1 | 3.029 | 299 | −0,347 | 0,219 | 0,113 | −23,7 % |
| R1 – andere Gruppenabgrenzung (Polyarchie ≥ 0,5) | 3.036 | 300 | −0,346 | 0,218 | 0,113 | −23,6 % |
| R2a – jede Beteiligung statt Initiierung | 3.045 | 708 | −0,279 | 0,169 | 0,099 | −15,4 % |
| R2b – nur Gewaltanwendung oder Krieg | 3.008 | 200 | −0,362 | 0,247 | 0,143 | −26,0 % |
| R3 – COW MID statt GML | 3.122 | 359 | −0,293 | 0,231 | 0,205 | −19,6 % |
| R4 – Machtanteil statt Großmachtstatus | 3.029 | 299 | −0,345 | 0,205 | 0,093 | −23,0 % |
| *Z1 – Jahrestrend statt Jahres-Fixeffekte* | 3.138 | 299 | −0,341 | 0,201 | 0,090 | −24,2 % |
| *Z2 – ohne Kontrollen* | 3.029 | 299 | −0,308 | 0,129 | **0,017** | −23,9 % |

Die beiden kursiven Zeilen waren nicht vorregistriert und dienen nur der Einordnung; sie zählen für die Entscheidung nicht.

## Die vorregistrierte Entscheidung

| Bedingung | erfüllt |
|---|---|
| (1) Hauptmodell negativ und p < 0,05 | **nein** (b = −0,347, p = 0,113) |
| (2) mindestens drei von vier Robustheitsvarianten desgleichen | **nein** (null von fünf gerechneten) |
| (3) Effekt mindestens −10 Prozent relativ | ja (−23,7 %) |

Damit greift die Regel für **nicht gestützt**: Die erste Bedingung ist verfehlt.

## Was das heißt, und was es nicht heißt

*Es heißt nicht, dass die These falsch ist.* Der Koeffizient ist in acht von acht Rechnungen negativ, also in der von der These vorhergesagten Richtung, und er ist substanziell groß – eine Standardabweichung gleicherer Machtverteilung geht mit einer um ein Fünftel bis ein Viertel niedrigeren vorhergesagten Initiierungswahrscheinlichkeit einher. Verfehlt wird nicht das Vorzeichen, sondern die Genauigkeit. Ein Nichtergebnis dieser Bauart ist keine Widerlegung; es ist ein Befund über die Grenzen dessen, was 111 Staaten und 299 Ereignisse hergeben.

*Es heißt aber auch nicht, dass die These halb gestützt wäre.* Drei Beobachtungen sprechen dagegen, und sie gehören genannt, weil sonst aus einem Nichtergebnis ein Achtungserfolg würde.

Erstens gibt es **kein Gefälle**. Teilt man die Gruppe in Viertel nach der Machtverteilung, liegen die Initiierungsraten bei 12,6 – 8,9 – 12,7 – 3,8 Prozent. Das dritte Viertel liegt so hoch wie das erste; abgesetzt ist allein das gleichste Viertel. Die These sagt einen Gradienten voraus und findet eine Stufe an einem Ende, und ein solches Muster erzeugt auch, wer eine Handvoll besonderer Länder in eine Kategorie sortiert.

Zweitens **verschwindet die Genauigkeit dort, wo der Wohlstand steht**. Die Verteilungsgröße korreliert zu 0,42 mit dem logarithmierten Bruttoinlandsprodukt je Kopf. Ohne Kontrollen ist der Zusammenhang bei p = 0,017 von null zu trennen, mit ihnen nicht mehr, während der Koeffizient fast gleich bleibt. Der gemessene Zusammenhang lässt sich also nicht davon unterscheiden, dass reiche Länder gleicher verteilt sind – und der kapitalistische Frieden ist genau die konkurrierende Erklärung, die dieses Buch bereits kennt.

Drittens ist **die erste Robustheitsvariante schwächer, als sie aussieht**. Die Abgrenzung über den Polyarchie-Index wählt fast dieselben Staat-Jahre wie die über die Regimeeinordnung (3.036 gegen 3.029); sie prüft die Ergebnisse also kaum gegen eine andere Entscheidung.

## Die Grenzen, die vorher genannt wurden, gelten unverändert

Der Test misst Zusammenhang und nicht Ursache. Er misst nur den sichtbaren Teil des Gegenstands: Militarisierte Auseinandersetzungen werden aus öffentlichen Quellen kodiert, und verdeckte Eingriffe – der Kanal, den das zweiundzwanzigste Kapitel als Ausweichroute der Rechenschaftspflicht benennt – sind darin kaum erfasst. Der Störfaktor Bündniszugehörigkeit ist nur grob aufgefangen. Und es ist eine erste Durchführung, kein Forschungsprogramm.

Diese Vorbehalte standen vor der Schätzung fest. Sie werden hier wiederholt und nicht verstärkt – ein Vorbehalt, der nach einem unerwünschten Ergebnis wächst, ist kein Vorbehalt, sondern eine Ausrede.

## Folge für das Buch

Nach der vorregistrierten Regel bleibt der Eintrag in der dritten Klasse des Ledgers – Fragen, über die niemand etwas weiß – und bekommt das Ergebnis dazu. Die Frage ist damit einmal gestellt worden, statt nur stellbar zu sein, und die Antwort lautet: Das Vorzeichen stimmt in jeder Rechnung, und in keiner trägt es.

Was ein nächster Anlauf bräuchte, ist damit auch bestimmt: mehr Ereignisse als 299, eine Trennung von Wohlstand und Verteilung, die dieses Panel nicht leistet, und eine abhängige Variable, die den verdeckten Teil erfasst. Wer das hat, prüft weiter. Wer es nicht hat, schreibt das Ergebnis auf und lässt den Eintrag stehen.

# Vorregistrierung: Prüfung der Friedensvermutung

**Angelegt am 15.08.2026, vor der ersten Modellschätzung.** Diese Datei wird nach der Auswertung nicht mehr geändert. Wer prüfen will, ob hier nachträglich zurechtgelegt wurde, vergleiche ihren Commit mit dem der Ergebnisdatei.

---

## Warum es diese Datei gibt

Das zweiundzwanzigste Kapitel prüft die Vermutung, eine Ordnung mit verteilter Macht trete nach außen friedlicher auf, und kommt zu dem Ergebnis, dass sie in dieser Form nicht hält – aber auch nicht widerlegt ist, weil sie sich gegen jeden Einzelfall retten lässt, indem man den kriegführenden Staat nachträglich als konzentriert einstuft. Das fünfundzwanzigste Kapitel führt sie deshalb als offene Frage der dritten Klasse und nennt ein Verfahren: die Verteilung wirtschaftlicher Macht unabhängig messen, innerhalb der Gruppe gewählter Regierungen gegen die Konfliktdaten halten und *vorher* sagen, welches Ergebnis die These widerlegt.

Der letzte Halbsatz ist der Grund für diese Datei. Nach der Hausregel dieses Projekts falsifiziert eine Kennzahl ohne Schwelle nichts, und das Buch hat diese Regel an fremden Bauteilen oft genug angewandt. Hier gilt sie gegen eine These, von deren Zutreffen das Projekt profitieren würde – und deshalb wird die Schwelle vorher aufgeschrieben.

## Frage

Sind Staat-Jahre mit gewählter Regierung, in denen politische Macht nach sozioökonomischer Stellung gleicher verteilt ist, seltener Ausgangspunkt zwischenstaatlicher militarisierter Auseinandersetzungen?

## Daten

*V-Dem, Version 16* (`vdemdata`, Datei `data/vdem.RData`), Staat-Jahr, 1789–2025. Daraus die Verteilungsgröße, die Regimeeinordnung und zwei Kontrollen.

*Gibler-Miller-Little MID* in der Aufbereitung des R-Pakets `peacesciencer` (`gml_mid_ddydisps`, gerichtete Dyaden-Jahr-Daten, 1816–2010). Ersatzweise *COW MID 5.0* (`cow_mid_dirdisps`, 1816–2014).

*Correlates of War* für Großmachtstatus (`cow_majors`) und Machtanteil (`cow_nmc`, CINC).

Zusammengeführt über den COW-Ländercode, den V-Dem als `COWcode` mitführt.

## Einheit und Zeitraum

Staat-Jahr, 1946 bis 2010. Der Beginn ist die Nachkriegsordnung, in der die Frage dieses Buches spielt; das Ende ist die Reichweite der GML-Daten.

## Grundgesamtheit

Staat-Jahre, die V-Dem nach *Regimes of the World* als Wahldemokratie oder liberale Demokratie führt, also `v2x_regime` in {2, 3}. Das ist die Gruppe, innerhalb derer die These überhaupt prüfbar wird: Der Vergleich zwischen Regimetypen misst das Regimeetikett, der Vergleich innerhalb der Gruppe misst die Machtverteilung.

## Variablen

*Unabhängig:* `v2pepwrses` im Jahr t – Verteilung politischer Macht nach sozioökonomischer Stellung. Höhere Werte bedeuten gleichere Verteilung. Standardisiert für die Berichterstattung der Effektgröße.

*Abhängig (Hauptmodell):* Initiierung im Jahr t+1. Gleich eins, wenn der Staat in einer im Jahr t+1 beginnenden militarisierten Auseinandersetzung Originator auf Seite A ist (`gmlmidonset` = 1, `orig` = 1, `sidea` = 1), sonst null. Gemessen wird also, wer anfängt, nicht wer beteiligt ist.

*Kontrollen:* logarithmiertes Bruttoinlandsprodukt je Kopf, logarithmierte Bevölkerung, Großmachtstatus, Jahres-Fixeffekte.

*Modell:* Logit, Standardfehler geclustert nach Staat.

## Robustheitsvarianten

1. *Andere Abgrenzung der Gruppe:* `v2x_polyarchy` ≥ 0,5 statt der Regimeeinordnung.
2. *Andere abhängige Variable:* jede Beteiligung an einer beginnenden Auseinandersetzung statt nur Initiierung; zusätzlich nur Auseinandersetzungen mit Gewaltanwendung oder Krieg (`hostlev` ≥ 4).
3. *Andere Konfliktquelle:* COW MID 5.0 statt GML.
4. *Andere Kontrolle:* Machtanteil (CINC) statt Großmachtstatus.

## Entscheidungsregel – vor der Schätzung festgelegt

Die These sagt ein **negatives** Vorzeichen voraus: mehr Gleichverteilung, weniger Initiierung.

**Gestützt** heißt sie nur, wenn alle drei Bedingungen zutreffen:
der Koeffizient ist im Hauptmodell negativ und bei p < 0,05 von null unterscheidbar;
er ist in mindestens drei der vier Robustheitsvarianten negativ und bei p < 0,05 von null unterscheidbar;
und der Effekt ist substanziell – eine Erhöhung um eine Standardabweichung senkt die vorhergesagte Initiierungswahrscheinlichkeit um mindestens zehn Prozent ihres Ausgangswerts.

**Nicht gestützt** heißt sie, wenn der Koeffizient im Hauptmodell nicht negativ ist oder bei p ≥ 0,05 nicht von null zu unterscheiden ist.

**Unentschieden** heißt sie, wenn das Hauptmodell die Bedingung erfüllt, die Robustheit aber durchfällt.

Das Ergebnis wird in allen drei Fällen veröffentlicht, und der Ledger-Eintrag im fünfundzwanzigsten Kapitel wird entsprechend geändert: bei *gestützt* wandert er aus der dritten Klasse heraus; bei *nicht gestützt* bleibt er dort und bekommt das Ergebnis; bei *unentschieden* bleibt er dort und bekommt beides.

## Was dieser Test nicht kann, ebenfalls vorher gesagt

*Er misst Zusammenhang, nicht Ursache.* Es gibt keine Identifikationsstrategie, kein Instrument, kein natürliches Experiment. Ein negativer Koeffizient wäre ein Anlass zum Weitersuchen und kein Nachweis.

*Er misst nur den sichtbaren Teil.* Militarisierte Auseinandersetzungen werden aus öffentlichen Quellen kodiert. Verdeckte Eingriffe sind darin kaum erfasst – und das ist genau der Kanal, den das zweiundzwanzigste Kapitel als Ausweichroute der Rechenschaftspflicht benennt. Ein Nullbefund kann deshalb auch bedeuten, dass die Wirkung dort steckt, wo diese Daten nicht hinsehen. Diese Lesart ist zulässig; sie darf aber nicht erst nach einem unerwünschten Ergebnis eingeführt werden, und deshalb steht sie hier.

*Er hat einen bekannten Störfaktor, den er nicht auflöst.* Wer an einem Einsatz teilnimmt, hängt stark an Bündniszugehörigkeit und Gelegenheit. Beides ist mit der Machtverteilung korreliert und wird hier nur über Großmachtstatus, Wirtschaftskraft und Größe grob aufgefangen.

*Er ist eine erste Durchführung und keine Untersuchung.* Ein Nachmittag, ein Auswerter, zwei öffentliche Datensätze. Das Ergebnis ist ein Anfang für die Frage und nicht ihr Abschluss.

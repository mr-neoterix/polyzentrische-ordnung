# Satz

Hier liegt, was aus den Kapiteldateien in `manuskript/` ein Buch-PDF macht.
Der Satz läuft bei jeder Änderung am Manuskript automatisch
(`.github/workflows/manuskript-pdf.yml`).

Das Ergebnis geht zwei Wege. Jeder Lauf hängt es als Artefakt
`manuskript-pdf` unter *Actions* an – auch für Zweige und Pull Requests,
aber nur mit Anmeldung erreichbar und nach neunzig Tagen verfallen. Läuft
der Satz auf dem Hauptzweig, wandert es zusätzlich an die Veröffentlichung
unter der Marke `manuskript-aktuell`, und die ist ohne Anmeldung offen. Ihr
Verweis bleibt derselbe, während sich der Anhang ändert:

```
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest/download/polyzentrische-ordnung-manuskript.pdf
```

Die Marke bleibt dabei stehen, wo sie angelegt wurde; aus welchem Stand das
PDF gesetzt wurde, sagt der Text der Veröffentlichung.

| Datei | Aufgabe |
|---|---|
| `build.py` | setzt die Kapitel zusammen und ruft Pandoc |
| `vorlage.tex` | die Buchgestaltung: Schrift, Satzspiegel, Kapitelköpfe, Belegapparat |

## Örtlich bauen

```
sudo apt-get install pandoc texlive-luatex texlive-latex-recommended \
                     texlive-lang-german texlive-fonts-recommended fonts-texgyre
python3 satz/build.py
```

Das PDF landet in `build/`. Der Ordner ist von der Versionsverwaltung
ausgenommen: Das PDF ist ein Erzeugnis, keine Quelle.

Nützlich beim Suchen von Fehlern:

```
python3 satz/build.py --nur-quelltext   # zeigt den zusammengesetzten Markdown-Stand
python3 satz/build.py --ausgabe /tmp/probe.pdf
```

## Was das Skript voraussetzt

Der Satz liest die Struktur aus den Quellen, statt sie zu verdoppeln. Drei
Annahmen macht er dabei, und wer sie bricht, bricht den Satz:

*Jede Kapiteldatei beginnt mit zwei Überschriften* – der ausgeschriebenen
Kapitelbezeichnung (`# Neuntes Kapitel`) und darunter dem Kapiteltitel
(`## Fehlertoleranz`). Beide zusammen ergeben den Kapitelanfang. Alle
weiteren Überschriften der Datei, ob mit zwei oder drei Rauten gesetzt,
werden als Abschnitte des Kapitels behandelt.

*Der Belegapparat steht am Schluss* unter einer Überschrift `Belege`. Er
wird kleiner und mit Abstand statt Einzug gesetzt, damit er als Apparat und
nicht als Fließtext gelesen wird. Ein Kapitel ohne Belege wird gesetzt, aber
im Lauf angemerkt.

*Die Einteilung in Teile steht in `manuskript/00_inhalt.md`*, im Abschnitt
*Aufbau*: fette Zeilen der Form `**Teil I – Die Frage**`, darunter kursive
Kapitelzeilen der Form `*1. Eine Frage, die weiterführte.*`. Daraus entstehen
die Teilseiten. Ein Kapitel, das dort nicht auftaucht, wird trotzdem gesetzt
– nur ohne Teilzuordnung, und der Lauf sagt es.

Die Reihenfolge der Kapitel ist die Reihenfolge der Dateinamen. Wer ein
Kapitel einschiebt, nummeriert die Dateien um.

*Die Titelei steht im Kopf von `00_inhalt.md`*, also vor dem ersten
Abschnitt: der Titel als `#`, der Untertitel als `###`, der Verfasser als
einzige fett gesetzte Zeile, der Stand als kursive Zeile `*Manuskript.
Stand: …*`. Titel, Untertitel und Verfasser wandern auch in die
PDF-Metadaten. Fehlt eine der Zeilen, entfällt sie schlicht auf der
Titelseite; nur ohne Titel bricht der Satz ab.

## Was das Skript am Text ändert

Nichts am Inhalt, zweierlei an der Form. Die Quellen setzen das öffnende
Anführungszeichen typografisch und das schließende als geraden Zoll
(`„Zitat"`); für den Satz wird daraus das deutsche Paar. Und hoch- oder
tiefgestellte Ziffern (`CO₂`) werden aus der Brotschrift gesetzt, weil
Pagella diese Zeichen nicht mitführt und LuaTeX sie sonst stillschweigend
weglässt.

Beides geschieht nur auf dem Weg ins PDF. Die Dateien in `manuskript/`
bleiben, wie sie sind.

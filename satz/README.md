# Satz

Hier liegt, was aus den Kapiteldateien in `manuskript/` ein Buch-PDF macht.
Der Satz läuft bei jeder Änderung am Manuskript automatisch
(`.github/workflows/manuskript-pdf.yml`).

Das Ergebnis geht zwei Wege. Jeder Lauf hängt es als Artefakt unter
*Actions* an – auch für Zweige und Pull Requests, aber nur mit Anmeldung
erreichbar und nach neunzig Tagen verfallen. Läuft der Satz auf dem
Hauptzweig, bekommt er zusätzlich eine Veröffentlichung, und die ist ohne
Anmeldung offen.

## Die Ausgabenummer

Jeder Satz des Hauptzweigs zählt eine Nummer der Form `1.x` hoch: `1.0`,
`1.1`, `1.2`. Sie steht an drei Stellen, damit sich zwei heruntergeladene
Dateien unterscheiden lassen, ohne sie zu öffnen – im Dateinamen
(`polyzentrische-ordnung-manuskript-1.3.pdf`), in der Marke (`v1.3`) und im
Titel der Veröffentlichung (`Manuskript 1.3 (Stand: …)`).

Gezählt wird nicht in einer Datei des Verzeichnisses, sondern an den
vorhandenen Marken: Der Lauf sucht die höchste Marke der Form `v1.x` und
nimmt die nächste. Das erspart einen Schritt, der in den Baum
zurückschreibt, und eine gelöschte Veröffentlichung gibt ihre Nummer nicht
wieder frei, solange ihre Marke steht. Wer eine Nummer überspringen will,
legt von Hand eine Marke an; wer sie zurücksetzen will, muss die höheren
Marken löschen.

Was nicht auf dem Hauptzweig läuft – Zweige und Pull Requests –, bekommt
keine Nummer, sondern den Quellstand: `…-entwurf-a1b2c3d.pdf`. Nur
Veröffentlichtes wird gezählt.

Der Verweis auf die jeweils letzte Ausgabe bleibt trotzdem derselbe, denn
jede neue Veröffentlichung wird zur „latest":

```
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest
```

Dazu liegt jeder Veröffentlichung derselbe Satz ein zweites Mal unter dem
festen Namen `polyzentrische-ordnung-manuskript.pdf` bei, damit auch der
Verweis unmittelbar auf die Datei gültig bleibt:

```
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest/download/polyzentrische-ordnung-manuskript.pdf
```

Wer die Nummer lesen will, nimmt die andere der beiden Dateien.

| Datei | Aufgabe |
|---|---|
| `build.py` | setzt die Kapitel zusammen und ruft Pandoc |
| `vorlage.tex` | die Buchgestaltung: Schrift, Satzspiegel, Kapitelköpfe, Belegapparat |

Gesetzt wird auf 14,8 × 21,0 cm, dem üblichen Buchformat, nicht auf A4.
Papierformat und Satzspiegel stehen im Kopf von `vorlage.tex` beieinander;
wer das eine ändert, muss das andere mitziehen, sonst steht der Text
verloren auf der Seite oder läuft aus ihr heraus.

## Linke und rechte Seiten

Gesetzt wird zweiseitig. Die erste Seite ist eine rechte; danach wechseln
sich linke und rechte ab, und was am Rand steht, wechselt mit. Die
Seitenzahl steht außen, also auf der linken Seite links und auf der rechten
Seite rechts; der Kolumnentitel steht innen, zum Bund hin. Nur die Zahl auf
den Kapitelanfängen bleibt, wo sie ist: Sie steht unten in der Mitte und
kennt deshalb keine Seite.

Der Kolumnentitel sagt links und rechts Verschiedenes – links das Kapitel,
rechts der Abschnitt. Das ist der eigentliche Gewinn des zweiseitigen
Satzes: Vorher stand auf jeder Seite dasselbe, nämlich der Abschnitt.

Die Ränder sind nicht mehr gleich. Innen stehen 22 mm, außen 18 mm, weil
der Bund einen Teil des inneren Randes verschluckt; zusammen bleiben es
dieselben 40 mm wie vorher, die Zeile also gleich lang.

Teile und Kapitel fangen auf einer rechten Seite an. Trifft es sich nicht,
bleibt die linke Seite davor frei – ganz frei, ohne Kolumnentitel und ohne
Zahl. Das kostet Papier: Aus 346 Seiten werden 369, dreiundzwanzig davon
leer. Wer das nicht will, tauscht in `vorlage.tex` die Klassenoption
`open=right` gegen `open=any` und in den Befehlen `\kapitel`, `\teil` und
`\vorspann` das `\cleardoublepage` gegen `\clearpage` – dann fangen Kapitel
an, wo das vorige aufhört, und die Zählung der Seiten bleibt trotzdem
zweiseitig.

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

Gezählt wird im PDF mit Ziffern: Über dem Titel steht „9. Kapitel“, im
Inhaltsverzeichnis „9. Kapitel – Fehlertoleranz“. Die Zahl nimmt der Satz
aus dem Dateinamen, nicht aus der Überschrift – der Dateiname bestimmt
ohnehin die Reihenfolge, und der Aufbau in `00_inhalt.md` zählt genauso.
Die ausgeschriebene Bezeichnung erscheint damit nicht mehr im PDF, wird
aber gegen die Dateinummer geprüft: Wer Dateien umnummeriert und die
Überschriften stehen lässt, liest es im Lauf als Hinweis.

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

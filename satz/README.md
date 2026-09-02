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

Jeder Satz des Hauptzweigs zählt eine Nummer der Form `2.x` hoch: `2.0`,
`2.1`, `2.2`. Sie steht an drei Stellen, damit sich zwei heruntergeladene
Dateien unterscheiden lassen, ohne sie zu öffnen – im Dateinamen
(`polyzentrische-ordnung-manuskript-2.3.pdf`), in der Marke (`v2.3`) und im
Titel der Veröffentlichung (`Manuskript 2.3 (Stand: …)`).

Die Nummer hat zwei Teile, und nur einer wird gezählt. Die Zahl nach dem
Punkt zählt der Lauf an den vorhandenen Marken und in keiner Datei des
Verzeichnisses: Er sucht die höchste Marke der laufenden Reihe (`v2.x`)
und nimmt die nächste. Das erspart einen Schritt, der in den Baum
zurückschreibt, und eine gelöschte Veröffentlichung gibt ihre Nummer nicht
wieder frei, solange ihre Marke steht. Wer eine Nummer überspringen will,
legt von Hand eine Marke an.

Die Zahl vor dem Punkt, die Hauptnummer, ist gesetzt statt gezählt. Sie
steht an genau einer Stelle, als `HAUPTNUMMER` im Kopf des Workflows, und
wer sie erhöht, setzt damit den Zähler zurück, ohne eine Marke anzufassen:
Die erste Ausgabe der neuen Reihe ist die `.0`, weil noch keine Marke mit
dieser Hauptnummer existiert, und die Marken der alten Reihe bleiben samt
ihren Veröffentlichungen stehen. Am 02.09.2026 ist die Hauptnummer von 1
auf 2 gestiegen; die erste Reihe lief von `1.0` bis `1.31`, und ihre
Ausgaben sind unter ihren Marken weiter erreichbar. Innerhalb einer Reihe
lässt sich der Zähler nur durch Löschen der höheren Marken zurücksetzen –
und genau das erspart die Hauptnummer.

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
| `schriften/` | die Schriftschnitte selbst, samt Lizenz |

Gesetzt wird auf 14,8 × 21,0 cm, dem üblichen Buchformat, nicht auf A4.
Papierformat und Satzspiegel stehen im Kopf von `vorlage.tex` beieinander;
wer das eine ändert, muss das andere mitziehen, sonst steht der Text
verloren auf der Seite oder läuft aus ihr heraus.

## Die Schriften liegen im Verzeichnis

Die Brotschrift ist **Alegreya** von Huerta Tipográfica, die Serifenlose ihre
Schwesterfamilie **Alegreya Sans**, dazu von beiden der Kapitälchenschnitt –
gebraucht wird er für die Kapitelmarken und die Belege-Köpfe. Alle liegen als
OTF-Dateien in `schriften/`: zehn Schnitte, 3,3 MB.

Das hat zwei Gründe. Der Bauläufer müsste die Schnitte sonst aus einem
Schriftpaket von 630 MB ziehen, und jeder Rechner setzt so mit denselben
Dateien, ohne dass eine Schriftverwaltung mitspielen muss. Den Pfad reicht
`build.py` als Pandoc-Variable an die Vorlage; fehlt sie, sucht LuaTeX wie
sonst im TeX-Baum.

Die Serifenlose kommt im Buchkörper praktisch nicht vor – die Überschriften
stehen ausdrücklich auf `\normalfont`, weil KOMA sie sonst serifenlos setzte.
Sie steht trotzdem auf der Schwesterfamilie und nicht mehr auf TeX Gyre
Heros: Ein zweites Schriftbild danebenzustellen, das mit dem ersten nichts zu
tun hat, ist eine Mischung ohne Grund. Aus demselben Grund fehlt ihr das
`Scale = MatchLowercase` der übrigen: Heros brauchte es, weil seine x-Höhe
neben Alegreya nicht stimmte; die beiden Alegreya sind aufeinander
gezeichnet, und Skalieren zerstörte gerade die Passung, um derentwillen sie
gewählt ist.

Nicht im Verzeichnis steht allein die Schreibmaschinenschrift. **Latin Modern
Mono** kommt weiter aus dem TeX-Baum, wo `fonts-texgyre` mit Heros
weggefallen ist und `fonts-lmodern` als Abhängigkeit ohnehin mitkommt. Sie
trägt im ganzen Buch acht Stellen, sämtlich in den Belegapparaten. Weil sie
als einzige an einem Paket hängt, prüft der Lauf sie eigens mit; fällt die
Abhängigkeit einmal weg, soll das dort auffallen und nicht erst in LuaTeX.

Alegreya steht unter der **SIL Open Font License**. Der Lizenztext liegt als
`schriften/OFL.txt` daneben, deckt beide Familien und gehört bei jeder
Weitergabe dazu – auch dann, wenn nur das PDF weitergereicht wird.

Wer die Schrift wechselt, ändert den Block im Kopf von `vorlage.tex` und legt
die neuen Schnitte daneben. Zu prüfen ist dabei dreierlei: ob die Schrift
echte Kapitälchen mitbringt (sonst bekommt `\scshape` stillschweigend
Gemeine), ob sie hoch- und tiefgestellte Ziffern führt, und wie viele Zeichen
danach in eine Zeile gehen. Für die Namen der Dateien gilt: Der Lauf bricht
ab, bevor LuaTeX es tut, und nennt den fehlenden Schnitt.

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

*Dieser eine Abschnitt wird gelesen und nicht gesetzt.* Alle übrigen
`##`-Abschnitte des Vorspanns wandern in der Reihenfolge der Datei ins PDF,
der Aufbau seit dem 01.09.2026 nicht mehr: Aus denselben Teilen und
Kapiteln erzeugt der Satz sein Inhaltsverzeichnis selbst, und zwar mit
Seitenzahlen – der Abschnitt stand wenige Seiten dahinter als zweites
Verzeichnis ohne. Im Verzeichnis bleibt er, weil es dort keinen Satzlauf
gibt, der eines erzeugt: Wer die Kapitel auf GitHub überblicken will, hat
nur ihn, und `README.md` verweist als „Übersicht und Leseplan" auf ihn. Der
Lauf sagt die Ausnahme mit („… Vorspannabschnitte gesetzt, Aufbau nur
gelesen"), damit die kleinere Zahl niemanden einen Fehler suchen lässt.

Die Reihenfolge der Kapitel ist die Reihenfolge der Dateinamen. Wer ein
Kapitel einschiebt, nummeriert die Dateien um.

*Die Titelei steht im Kopf von `00_inhalt.md`*, also vor dem ersten
Abschnitt: der Titel als `#`, der Untertitel als `###`, der Verfasser als
einzige fett gesetzte Zeile, der Stand als kursive Zeile `*Manuskript.
Stand: …*`. Titel, Untertitel und Verfasser wandern auch in die
PDF-Metadaten. Fehlt eine der Zeilen, entfällt sie schlicht auf der
Titelseite; nur ohne Titel bricht der Satz ab.

*Das Impressum steht auf der Rückseite des Titelblatts*, in `vorlage.tex`.
Zwei seiner Angaben werden dort nicht gepflegt: Der Rechteinhaber ist der
Verfasser aus der Titelei, und die Jahreszahl kommt aus dem Datum des
Quellstands – nicht aus der Uhr des Bauläufers, damit ein späterer Satz
derselben Fassung dieselbe Zahl trägt. Verlag und Druckerei stehen fest in
der Vorlage; wer sie ändert, ändert sie dort.

## Was das Skript am Text ändert

Nichts am Inhalt, zweierlei an der Form. Die Quellen setzen das öffnende
Anführungszeichen typografisch und das schließende als geraden Zoll
(`„Zitat"`); für den Satz wird daraus das deutsche Paar. Und hoch- oder
tiefgestellte Ziffern (`CO₂`) werden aus der Brotschrift gesetzt, weil
Brotschriften diese Zeichen selten mitführen und LuaTeX sie sonst
stillschweigend weglässt.

Beides geschieht nur auf dem Weg ins PDF. Die Dateien in `manuskript/`
bleiben, wie sie sind.

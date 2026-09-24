# Satz

Hier liegt, was aus den Kapiteldateien in `manuskript/` die Bücher macht.
Das Manuskript erscheint in zwei Bänden, und jeder liegt in seinem eigenen
Verzeichnis: das Argument in `manuskript/band1/`, die Bauanleitung in
`manuskript/band2/`. Jeder Band hat seine eigene Inhaltsdatei, seine eigene
Titelei und seine eigene Kapitelzählung, die bei eins beginnt. Der Satz
läuft bei jeder Änderung am Manuskript automatisch
(`.github/workflows/manuskript-pdf.yml`) und setzt dann beide Bände.

Aus jedem Band entstehen fünf Dateien, in drei Gruppen:

| Datei | Wozu |
|---|---|
| `polyzentrische-ordnung-band-1.pdf` | die **Leseausgabe** für den Bildschirm: mit Lesezeichen, anklickbarem Inhaltsverzeichnis und der Akzentfarbe der Überschriften |
| `polyzentrische-ordnung-band-1-kdp-innenteil.pdf` | der **Innenteil des Taschenbuchs** zum Hochladen bei KDP: seitengleich mit der Leseausgabe, in Graustufen, ohne Lesezeichen und Verweise |
| `polyzentrische-ordnung-band-1-kdp-umschlag.pdf` | der **Umschlag des Taschenbuchs** für KDP: Rückseite, Rücken und Vorderseite auf einem Bogen, mit Beschnitt; der Rücken folgt aus der Seitenzahl |
| `polyzentrische-ordnung-band-1.epub` | das **E-Book** (EPUB 3) für KDP und jedes andere Lesegerät |
| `polyzentrische-ordnung-band-1-ebook-titelbild.jpg` | das **Titelbild des E-Books** für KDP, 1600 × 2560 Pixel |

Für den zweiten Band dasselbe mit `band-2`. Das Ergebnis geht zwei Wege.
Jeder Lauf hängt alle Dateien als Artefakt unter *Actions* an – auch für
Zweige und Pull Requests, aber nur mit Anmeldung erreichbar und nach
neunzig Tagen verfallen. Läuft der Satz auf dem Hauptzweig, bekommt er
zusätzlich eine Veröffentlichung, und die ist ohne Anmeldung offen. Was der
Lauf gesetzt hat – Seitenzahlen, Rückenbreiten, Warnungen –, steht danach
in `build/ausgabe.json`, in der Zusammenfassung des Laufs und im Text der
Veröffentlichung.

| Datei | Aufgabe |
|---|---|
| `build.py` | setzt die Kapitel eines Bandes zusammen und erzeugt daraus alle fünf Dateien, ohne Angabe für beide Bände |
| `vorlage.tex` | die Buchgestaltung: Schrift, Satzspiegel, Kapitelköpfe, Belegapparat, Impressum; aus ihr entstehen Leseausgabe und Innenteil |
| `umschlag.tex` | der Umschlag und das Titelbild des E-Books |
| `epub-vorlage.xhtml`, `epub.css` | Titelseite, Impressum und Gestaltung des E-Books |
| `veroeffentlichung.toml` | was nicht im Manuskript steht: Format, Papier, Verlag, Anschrift, Lizenz, ISBN |
| `umschlag/band1.md`, `umschlag/band2.md` | der Text der Umschlagrückseite, zugleich die Beschreibung des E-Books |
| `schriften/` | die Schriftschnitte selbst, samt Lizenz |

## Die Ausgabenummer

Jeder Satz des Hauptzweigs zählt eine Nummer der Form `3.x` hoch: `3.0`,
`3.1`, `3.2`. Alle Dateien beider Bände eines Laufs tragen dieselbe Nummer
und erscheinen in derselben Veröffentlichung. Die Nummer steht an vier
Stellen, damit sich heruntergeladene Dateien unterscheiden lassen, ohne sie
zu öffnen – im Dateinamen (`polyzentrische-ordnung-band-1-3.3.pdf`,
`polyzentrische-ordnung-band-1-kdp-umschlag-3.3.pdf`), in der Marke
(`v3.3`), im Titel der Veröffentlichung (`Manuskript 3.3 (Stand: …)`) und
im Impressum jedes Bandes („Ausgabe 3.3“). Das Satzskript bekommt sie mit
`--kennung`.

Die Nummer hat zwei Teile, und nur einer wird gezählt. Die Zahl nach dem
Punkt zählt der Lauf an den vorhandenen Marken und in keiner Datei des
Verzeichnisses: Er sucht die höchste Marke der laufenden Reihe (`v3.x`)
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
Ausgaben sind unter ihren Marken weiter erreichbar. Am 23.09.2026 ist sie
von 2 auf 3 gestiegen, mit der Teilung des Manuskripts in zwei Bände; die
zweite Reihe lief von `2.0` bis `2.2` und bestand aus je einem PDF. Jede
Ausgabe der dritten Reihe bestand zunächst aus zwei PDFs im Format A5; seit
dem 24.09.2026 besteht sie aus fünf Dateien je Band im Format für KDP.
Innerhalb einer Reihe lässt sich der Zähler nur durch Löschen der höheren
Marken zurücksetzen – und genau das erspart die Hauptnummer.

Was nicht auf dem Hauptzweig läuft – Zweige und Pull Requests –, bekommt
keine Nummer, sondern den Quellstand: `…-entwurf-a1b2c3d.pdf`. Nur
Veröffentlichtes wird gezählt, und nur eine gezählte Ausgabe nennt im
Impressum eine Ausgabenummer.

Der Verweis auf die jeweils letzte Ausgabe bleibt trotzdem derselbe, denn
jede neue Veröffentlichung wird zur „latest":

```
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest
```

Dazu liegen jeder Veröffentlichung die Leseausgabe und das E-Book jedes
Bandes ein zweites Mal unter einem festen Namen bei, damit auch die
Verweise unmittelbar auf die Dateien gültig bleiben:

```
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest/download/polyzentrische-ordnung-band-1.pdf
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest/download/polyzentrische-ordnung-band-2.pdf
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest/download/polyzentrische-ordnung-band-1.epub
https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest/download/polyzentrische-ordnung-band-2.epub
```

Die Dateien für KDP bekommen keinen festen Namen: Wer sie hochlädt, soll
wissen, welche Ausgabe es ist. Der feste Name der zweiten Reihe,
`polyzentrische-ordnung-manuskript.pdf`, liegt nur den Veröffentlichungen
bis `v2.2` bei; der Verweis auf ihn unter `latest` führt seit der ersten
Ausgabe der dritten Reihe ins Leere.

## Das Format

Gesetzt wird auf 5,5 × 8,5 Zoll, also 13,97 × 21,59 cm. Das ist ein
Standardformat von KDP, und unter diesen liegt es dem deutschen
Sachbuchformat von 13,5 × 21,5 cm am nächsten; bis zum 24.09.2026 stand
hier A5, das KDP nur als Sonderformat annimmt. Das Format steht in
`veroeffentlichung.toml`, die Ränder in `vorlage.tex`. Wer das eine
ändert, prüft das andere mit, sonst steht der Text verloren auf der Seite
oder läuft aus ihr heraus. Ein Format, das KDP nicht als Standard führt,
setzt der Lauf trotzdem, meldet es aber.

Der Satzspiegel ist beim Formatwechsel nur so weit nachgezogen, wie das
schmalere und etwas höhere Blatt verlangt: Die Zeile ist 102,7 statt
108 mm breit, die Kolumne sechs Millimeter höher, und beide Bände behalten
ihren Umfang – 190 und 240 Seiten wie auf A5, gemessen am 24.09.2026. Oben
stehen 18 mm Rand, unten 22, außen 17 und innen der Bund.

**Der Bund folgt der Seitenzahl.** KDP verlangt innen mindestens 9,6 mm
bis 150 Seiten, 12,7 mm bis 300, 15,9 mm bis 500, 19,1 mm bis 700 und
22,3 mm bis 828 Seiten; außen, oben und unten 6,4 mm. Die Vorlage hält
innen 20 mm, mehr als KDP bis 700 Seiten verlangt. Welchen Bund ein Band
braucht, weiß erst der fertige Satz; wird ein Band so dick, dass die 20 mm
nicht mehr reichen, setzt der Lauf ihn mit dem verlangten Bund neu.

## Leseausgabe und Innenteil

Beide entstehen aus derselben Vorlage und sind seitengleich: Eine
Seitenangabe gilt in beiden, und der Lauf warnt, wenn ihre Seitenzahlen je
auseinanderlaufen. Die Variable `druck` schaltet drei Dinge um, und nur
diese.

*Graustufen:* Der Innenteil wird schwarzweiß gedruckt. xcolor rechnet
deshalb jede Farbe schon im Satz in einen Grauwert um, statt die
Umrechnung der Druckerei zu überlassen; die Akzentfarbe der Überschriften
wird ein dunkles Grau.

*Keine Lesezeichen, keine Verweise:* KDP lehnt Innenteile mit
Lesezeichen, Anmerkungen oder Verweisflächen ab. hyperref läuft im
Innenteil deshalb im Entwurfsmodus und ohne Lesezeichen, und die
Klassenoption `bookmarkpackage=false` hält scrbook davon ab, das Paket
`bookmark` nachzuladen, das Lesezeichen an hyperref vorbei anlegt.

*Druckort:* Nur das Impressum des Innenteils nennt ihn.

Der Lauf prüft den Innenteil danach selbst gegen die Vorgaben von KDP, so
weit die Datei es zeigt: das Seitenmaß jeder Seite, keine Lesezeichen und
keine Anmerkungen, die Seitenzahl zwischen 24 und 828 und den Bund. Dafür
schreibt die Vorlage den Innenteil ohne Objektströme; Seitenmaß und
Anmerkungen stehen dann im Klartext in der Datei.

Beide PDFs enden auf einer geraden Seite. KDP füllt eine ungerade
Seitenzahl ohnehin auf; so stimmt die Seitenzahl der Datei mit der
gedruckten überein, und aus ihr rechnet der Umschlag seinen Rücken. Der
Trennstrich über dem Belegapparat ist 0,75 pt stark, weil KDP dünnere
Linien nicht sicher druckt.

## Der Umschlag

Der Umschlag ist ein einziger Bogen aus Rückseite, Rücken und Vorderseite,
rundum mit 0,125 Zoll (3,2 mm) Beschnitt, so wie KDP ihn verlangt. Seine
Breite rechnet der Lauf aus der Seitenzahl des fertigen Innenteils:

```
Rücken = Seiten × 0,002252 Zoll (weißes Papier) bzw. × 0,0025 Zoll (creme)
Breite = 0,125 + 5,5 + Rücken + 5,5 + 0,125 Zoll
Höhe   = 0,125 + 8,5 + 0,125 Zoll
```

Wird ein Band dicker, wird sein Rücken breiter, ohne dass jemand etwas
einstellt. Welches Papier gilt, steht in `veroeffentlichung.toml`; es muss
dasselbe sein, das bei KDP gewählt wird. Der Lauf misst den fertigen Bogen
nach und bricht ab, wenn er nicht das Maß hat, das KDP erwartet.

Was KDP sonst vorschreibt, hält die Vorlage ein. Text steht überall mehr
als 0,125 Zoll innerhalb der Schnittkante. Rückentext gibt es erst ab 80
Seiten und mit 0,0625 Zoll Luft zu beiden Falzen; der Lauf rechnet die
Schriftgröße des Rückens daraus und lässt ihn leer, wo sie unter sechs
Punkt fiele. Unten an der Rückseite, 0,25 Zoll vom Rücken und von der
Schnittkante, bleibt ein weißes Feld von 2 × 1,2 Zoll frei: Dort druckt
KDP den Barcode hinein, und ein Umschlag mit Text oder Bild in diesem Feld
wird abgelehnt. Die Farben stehen als CMYK, der Grund bleibt unter 240
Prozent Farbmenge, Transparenz gibt es keine und keine Linie unter 0,75 pt.

Gestaltet ist der Umschlag typografisch: der Titel groß oben, darunter der
Untertitel, in der Mitte als Zeichen eine Gruppe von Kreisen mit je einem
Mittelpunkt – viele Zentren, keines in der Mitte –, unten Band und
Verfasser. Der erste Band steht auf gedecktem Schieferblau, der zweite auf
dunklem Ziegelrot. Der Rücken liest sich von unten nach oben, wie in
deutschen Büchern üblich: Verfasser, Titel, Band.

**Der Text der Rückseite steht in `umschlag/band1.md` und
`umschlag/band2.md`.** Er ist zugleich die Beschreibung in den Metadaten
des E-Books und passt in das Feld „Beschreibung“ bei KDP. Übernommen ist
er wörtlich aus dem Abschnitt „Über dieses Buch“ des jeweiligen Bandes;
wer einen eigenen Klappentext will, ersetzt ihn dort. Die Rückseite trägt
etwa 230 Wörter. Wird der Text länger, als der Platz über der Werkangabe
reicht, meldet der Lauf, um wie viele Millimeter.

## Das E-Book

Das E-Book ist ein EPUB 3, gebaut von Pandoc nach `epub-vorlage.xhtml` und
`epub.css`. Die Gliederung ist die des Buches: Vorspann und Teile auf der
ersten Ebene, die Kapitel darunter, jedes in einer eigenen Datei. Das
Inhaltsverzeichnis steht am Anfang und führt, wie im PDF, Teile und
Kapitel („9. Kapitel – Fehlertoleranz“). Die Titelseite trägt Titel,
Untertitel, Bandzeile, Verfasser und Stand, die Seite dahinter das
Impressum. Eine Schrift schreibt das Stylesheet nicht vor; die wählt der
Leser.

Nach dem Lauf von Pandoc bessert das Satzskript an drei Stellen nach, weil
KDP es so verlangt. *Die Titelbildseite fällt:* Pandoc legt zum Titelbild
eine eigene Seite an, und die Kindle-Richtlinien verbieten genau das – das
Titelbild erschiene doppelt oder die Umwandlung scheiterte. Das Bild bleibt,
als `cover-image` und zusätzlich mit der älteren Angabe
`<meta name="cover">`. *Der Lesebeginn wird gesetzt:* Das Buch geht beim
ersten Öffnen auf „Über dieses Buch“ auf, nicht auf der Titelseite. *Die
Kapitelmarken bekommen den Gedankenstrich:* Im Inhaltsverzeichnis stehen
Marke und Titel hintereinander wie im PDF, ohne dass dafür Text versteckt
werden müsste – versteckter Text im Inhaltsverzeichnis bricht die
Umwandlung bei Kindle ab.

Danach prüft EPUBCheck, der Prüfer des W3C, das fertige E-Book, sobald er
greifbar ist: über die Umgebungsvariable `EPUBCHECK` (Pfad zur
`epubcheck.jar`) oder als Programm im Suchpfad. Der Workflow lädt ihn in
einer festen Version mit Prüfsumme; ein E-Book mit Fehlern bricht den Lauf
ab. Örtlich ohne EPUBCheck bleibt das E-Book ungeprüft, und der Lauf sagt
es.

Das Titelbild zeichnet dieselbe Vorlage wie den Umschlag, nur die
Vorderseite, im Seitenverhältnis 1 : 1,6 und in RGB, weil Kindle kein CMYK
kennt. Die RGB-Werte stehen neben den CMYK-Werten in `umschlag.tex`: Sie
sind die, als die ein gewöhnliches Farbprofil die Druckfarben wiedergibt,
damit das Titelbild aussieht wie das gedruckte Buch. Gerastert wird mit
`pdftoppm` aus Poppler, sonst mit Ghostscript; fehlt beides, entsteht das
E-Book ohne Titelbild, und der Lauf warnt.

## Angaben zur Veröffentlichung

Was im Impressum, auf dem Umschlag und in den Metadaten des E-Books steht,
aber nicht im Manuskript, steht in `veroeffentlichung.toml`: Format und
Papier, Lizenz und die Adresse des offenen Verzeichnisses, Verlag,
Anschrift und Druckort, der Hinweis auf die Deutsche Nationalbibliothek
und die ISBN je Band und Ausgabe.

**Die Anschrift ist Pflicht.** Die Landespressegesetze verlangen auf jedem
Druckwerk, das in Deutschland erscheint, Namen und Anschrift des
Verlegers, beim Selbstverlag also des Verfassers; ein Postfach genügt
nicht, die Anschrift eines Impressumsdienstes schon. Sie erscheint in
allen Dateien, also öffentlich. Wird das Feld geleert, steht die
Verlagszeile ohne Anschrift, und jeder Lauf warnt, dass Innenteil und
E-Book so nicht einreichbar sind.

Den Druckort nennt das Impressum nicht mit Namen: KDP druckt je nach
Bestellort an verschiedenen Orten und druckt den tatsächlichen auf die
letzte Seite jedes Exemplars. Der Hinweis auf die Deutsche
Nationalbibliothek bleibt aus, bis die Pflichtexemplare abgeliefert und
verzeichnet sind. Eine ISBN ist für das Taschenbuch bei KDP kostenlos zu
haben, das E-Book braucht keine; wer eine einträgt, muss dieselbe bei KDP
angeben.

## Bei KDP einreichen

Beim Anlegen des Taschenbuchs: Format 5,5 × 8,5 Zoll (13,97 × 21,59 cm),
Innenteil schwarzweiß auf dem Papier, das in `veroeffentlichung.toml`
steht, **ohne Beschnitt** („No bleed“); Innenteil
`…-kdp-innenteil-3.x.pdf`, Umschlag `…-kdp-umschlag-3.x.pdf` als eigene
PDF-Datei. Beim E-Book: Manuskript `…-3.x.epub`, Umschlag
`…-ebook-titelbild-3.x.jpg`. Dazu drei Dinge, die keine Datei erledigen
kann.

*KI-Angabe:* KDP verlangt, dass Text, der von einer künstlichen Intelligenz
erzeugt wurde, beim Einreichen als solcher angegeben wird – auch wenn er
danach bearbeitet wurde. Das Buch sagt im Abschnitt „Wie dieses Buch
entstanden ist“ selbst, dass seine Prosa so entstanden ist.

*Frei verfügbarer Inhalt:* Leseausgabe und E-Book liegen frei im Netz. KDP
nimmt solche Inhalte nur vom Rechteinhaber an und kann danach fragen.

*KDP Select:* Das Programm verlangt, dass das E-Book ausschließlich bei
Amazon erhältlich ist, auch kostenlos nirgends sonst. Solange das EPUB und
das PDF hier veröffentlicht werden, ist das E-Book deshalb nicht in KDP
Select einzuschreiben.

## Die Schriften liegen im Verzeichnis

Die Brotschrift ist **Alegreya** von Huerta Tipográfica, die Serifenlose ihre
Schwesterfamilie **Alegreya Sans**, dazu von beiden der Kapitälchenschnitt –
gebraucht wird er für die Kapitelmarken, die Belege-Köpfe und den Umschlag.
Alle liegen als OTF-Dateien in `schriften/`: zehn Schnitte, 3,3 MB. Das
E-Book bettet keine Schrift ein; dort wählt der Leser.

Das hat zwei Gründe. Der Bauläufer müsste die Schnitte sonst aus einem
Schriftpaket von 630 MB ziehen, und jeder Rechner setzt so mit denselben
Dateien, ohne dass eine Schriftverwaltung mitspielen muss. Den Pfad reicht
`build.py` an die Vorlagen weiter; fehlt er, sucht LuaTeX wie sonst im
TeX-Baum.

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
trägt im ganzen Buch acht Stellen, sämtlich in den Belegapparaten, dazu die
Pfadangabe im Impressum. Weil sie als einzige an einem Paket hängt, prüft
der Lauf sie eigens mit; fällt die Abhängigkeit einmal weg, soll das dort
auffallen und nicht erst in LuaTeX.

Alegreya steht unter der **SIL Open Font License**. Der Lizenztext liegt als
`schriften/OFL.txt` daneben, deckt beide Familien und gehört bei jeder
Weitergabe dazu – auch dann, wenn nur das PDF weitergereicht wird.

Wer die Schrift wechselt, ändert den Block im Kopf von `vorlage.tex` und von
`umschlag.tex` und legt die neuen Schnitte daneben. Zu prüfen ist dabei
dreierlei: ob die Schrift echte Kapitälchen mitbringt (sonst bekommt
`\scshape` stillschweigend Gemeine), ob sie hoch- und tiefgestellte Ziffern
führt, und wie viele Zeichen danach in eine Zeile gehen. Für die Namen der
Dateien gilt: Der Lauf bricht ab, bevor LuaTeX es tut, und nennt den
fehlenden Schnitt.

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

Die Ränder sind nicht gleich. Innen stehen 20 mm, außen 17 mm, weil der
Bund einen Teil des inneren Randes verschluckt.

Teile und Kapitel fangen auf einer rechten Seite an. Trifft es sich nicht,
bleibt die linke Seite davor frei – ganz frei, ohne Kolumnentitel und ohne
Zahl. Das kostet Papier, im Taschenbuch auch Geld, denn KDP rechnet den
Druck nach Seiten ab. Wer das nicht will, tauscht in `vorlage.tex` die
Klassenoption `open=right` gegen `open=any` und in den Befehlen `\kapitel`,
`\teil` und `\vorspann` das `\cleardoublepage` gegen `\clearpage` – dann
fangen Kapitel an, wo das vorige aufhört, und die Zählung der Seiten bleibt
trotzdem zweiseitig. Mehr als vier leere Seiten hintereinander lässt KDP
am Anfang und im Inneren nicht zu, am Ende nicht mehr als zehn; die
Vorlage erzeugt höchstens eine.

## Örtlich bauen

```
sudo apt-get install pandoc texlive-luatex texlive-latex-recommended \
                     texlive-lang-german texlive-fonts-recommended \
                     texlive-pictures poppler-utils
python3 satz/build.py                          # alles, beide Bände
python3 satz/build.py --band 1                 # nur einen
python3 satz/build.py --nur lesen              # nur die Leseausgaben
python3 satz/build.py --nur druck --nur ebook  # Innenteil, Umschlag, E-Book
```

Die Dateien landen in `build/`, ohne Ausgabenummer im Namen; mit
`--kennung 3.4` bekommen sie eine, und das Impressum nennt sie. Der Ordner
ist von der Versionsverwaltung ausgenommen: Ein PDF ist ein Erzeugnis,
keine Quelle. Unter `build/zwischenstand/` liegt je Band und Erzeugnis, was
der Lauf dafür zusammengesetzt hat – Quelltext, LaTeX-Datei und Protokoll.

Wer die E-Books örtlich prüfen will, lädt EPUBCheck von
`github.com/w3c/epubcheck` und nennt dem Lauf die Datei:

```
EPUBCHECK=/pfad/zu/epubcheck.jar python3 satz/build.py --nur ebook
```

Nützlich beim Suchen von Fehlern:

```
python3 satz/build.py --band 2 --nur-quelltext            # der Markdown-Stand des PDFs
python3 satz/build.py --band 2 --nur ebook --nur-quelltext # der des E-Books
python3 satz/build.py --band 1 --ziel /tmp/probe
```

## Was das Skript voraussetzt

Der Satz liest die Struktur aus den Quellen, statt sie zu verdoppeln. Drei
Annahmen macht er dabei, und wer sie bricht, bricht den Satz:

*Jede Kapiteldatei beginnt mit zwei Überschriften* – der ausgeschriebenen
Kapitelbezeichnung (`# Neuntes Kapitel`) und darunter dem Kapiteltitel
(`## Fehlertoleranz`). Beide zusammen ergeben den Kapitelanfang. Alle
weiteren Überschriften der Datei, ob mit zwei oder drei Rauten gesetzt,
werden als Abschnitte des Kapitels behandelt.

Gezählt wird im PDF und im E-Book mit Ziffern: Über dem Titel steht
„9. Kapitel“, im Inhaltsverzeichnis „9. Kapitel – Fehlertoleranz“. Die Zahl
nimmt der Satz aus dem Dateinamen, nicht aus der Überschrift – der
Dateiname bestimmt ohnehin die Reihenfolge, und der Aufbau in
`00_inhalt.md` zählt genauso. Jeder Band zählt für sich und beginnt bei
eins; ein Kapitel des zweiten Bandes kann deshalb dieselbe Nummer tragen
wie eines des ersten. Die ausgeschriebene Bezeichnung erscheint damit
nicht mehr im Satz, wird aber gegen die Dateinummer geprüft: Wer Dateien
umnummeriert und die Überschriften stehen lässt, liest es im Lauf als
Hinweis.

*Der Belegapparat steht am Schluss* unter einer Überschrift `Belege`. Er
wird kleiner und mit Abstand statt Einzug gesetzt, damit er als Apparat und
nicht als Fließtext gelesen wird. Ein Kapitel ohne Belege wird gesetzt, aber
im Lauf angemerkt.

*Die Einteilung in Teile steht in der `00_inhalt.md` jedes Bandes*, im Abschnitt
*Aufbau*: fette Zeilen der Form `**Teil I – Die Frage**`, darunter kursive
Kapitelzeilen der Form `*1. Eine Frage, die weiterführte.*`. Daraus entstehen
die Teilseiten. Ein Kapitel, das dort nicht auftaucht, wird trotzdem gesetzt
– nur ohne Teilzuordnung, und der Lauf sagt es.

*Dieser eine Abschnitt wird gelesen und nicht gesetzt.* Alle übrigen
`##`-Abschnitte des Vorspanns wandern in der Reihenfolge der Datei in die
Bücher, der Aufbau seit dem 01.09.2026 nicht mehr: Aus denselben Teilen und
Kapiteln erzeugt der Satz sein Inhaltsverzeichnis selbst, im PDF mit
Seitenzahlen – der Abschnitt stand wenige Seiten dahinter als zweites
Verzeichnis ohne. Im Verzeichnis bleibt er, weil es dort keinen Satzlauf
gibt, der eines erzeugt: Wer die Kapitel auf GitHub überblicken will, hat
nur ihn, und `README.md` verweist als „Übersicht und Leseplan" auf ihn. Der
Lauf sagt die Ausnahme mit („… Vorspannabschnitte gesetzt, Aufbau nur
gelesen"), damit die kleinere Zahl niemanden einen Fehler suchen lässt.

Die Reihenfolge der Kapitel ist die Reihenfolge der Dateinamen. Wer ein
Kapitel einschiebt, nummeriert die Dateien um.

*Die Titelei steht im Kopf von `00_inhalt.md`*, also vor dem ersten
Abschnitt: der Titel als `#`, der Untertitel als `###`, die Bandzeile als
`####` („Erster Band: Das Argument“), der Verfasser als einzige fett gesetzte
Zeile, der Stand als kursive Zeile `*Manuskript. Stand: …*`. Titel,
Bandzeile, Untertitel und Verfasser wandern auch in die Metadaten der PDFs
und des E-Books und auf den Umschlag; die Bandzeile steht auf der
Titelseite unter dem Untertitel und wird auf dem Umschlag am Doppelpunkt
geteilt („Erster Band“ über „Das Argument“). Die Standzeilen beider Bände
werden getrennt gepflegt; stimmen sie überein, nennt der Titel der
Veröffentlichung den Stand einmal, sonst beide. Fehlt eine der Zeilen,
entfällt sie schlicht auf der Titelseite; nur ohne Titel bricht der Satz
ab.

*Das Impressum steht auf der Rückseite des Titelblatts*, im E-Book auf der
Seite hinter der Titelseite. Gepflegt wird es nicht in einer Vorlage: Das
Satzskript setzt es aus der Titelei, dem Quellstand und
`veroeffentlichung.toml` zusammen – Rechteangabe und Lizenz, Verlag mit
Anschrift, im Innenteil der Druckort, die ISBN, wo es eine gibt, und die
Herkunft aus dem offenen Verzeichnis samt Quellstand. Die Jahreszahl kommt
aus dem Datum des Quellstands und nicht aus der Uhr des Bauläufers, damit
ein späterer Satz derselben Fassung dieselbe Zahl trägt.

## Was das Skript am Text ändert

Nichts am Inhalt, zweierlei an der Form. Die Quellen setzen das öffnende
Anführungszeichen typografisch und das schließende als geraden Zoll
(`„Zitat"`); für den Satz wird daraus das deutsche Paar. Und hoch- oder
tiefgestellte Ziffern (`CO₂`) werden im PDF aus der Brotschrift gesetzt,
weil Brotschriften diese Zeichen selten mitführen und LuaTeX sie sonst
stillschweigend weglässt; im E-Book werden sie als Hoch- und Tiefstellung
ausgezeichnet, weil niemand weiß, welche Schrift ein Lesegerät nimmt.

Beides geschieht nur auf dem Weg in die Erzeugnisse. Die Dateien in
`manuskript/band1/` und `manuskript/band2/` bleiben, wie sie sind.

# KDP-Einstellungen für beide Bände

Alles, was beim Einreichen der beiden Bände bei Kindle Direct Publishing (KDP) in die Formulare gehört, für das Taschenbuch und für das E-Book. Geordnet ist es nach den drei Seiten, die KDP für jedes Buch zeigt: *Details*, *Inhalt* und *Preisgestaltung*. Stand: 24.09.2026, Ausgabe 3.4.

Die Dateien kommen aus der jeweils jüngsten [Veröffentlichung](https://github.com/mr-neoterix/polyzentrische-ordnung/releases/latest); ihre Namen tragen die Ausgabenummer. Seitenzahl und Rückenbreite nennt der Text jeder Veröffentlichung. Ändert sich der Umfang eines Bandes, müssen Innenteil **und** Umschlag neu hochgeladen werden, denn der Rücken wächst mit.

Maßgeblich für die Klappentexte sind `satz/umschlag/band1.md` und `satz/umschlag/band2.md`; hier stehen sie nur zum Kopieren. Wer sie dort ändert, zieht sie hier nach.

## Auf einen Blick

| | Band 1 – Das Argument | Band 2 – Die Bauanleitung |
|---|---|---|
| Seiten | 190 | 240 |
| Rücken (weißes Papier) | 10,9 mm | 13,7 mm |
| Druckkosten bei Amazon.de | 3,03 € | 3,63 € |
| Innenteil | `…-band-1-kdp-innenteil-3.4.pdf` | `…-band-2-kdp-innenteil-3.4.pdf` |
| Umschlag | `…-band-1-kdp-umschlag-3.4.pdf` | `…-band-2-kdp-umschlag-3.4.pdf` |
| E-Book | `…-band-1-3.4.epub` | `…-band-2-3.4.epub` |
| Titelbild des E-Books | `…-band-1-ebook-titelbild-3.4.jpg` | `…-band-2-ebook-titelbild-3.4.jpg` |

Alle Dateinamen beginnen mit `polyzentrische-ordnung`.

## Details

Diese Seite ist für Taschenbuch und E-Book dieselbe. Wer zuerst das Taschenbuch anlegt, kann die Angaben für das E-Book übernehmen lassen.

| Feld | Band 1 | Band 2 |
|---|---|---|
| Sprache | Deutsch | Deutsch |
| Buchtitel | Die polyzentrische Ordnung | Die polyzentrische Ordnung |
| Untertitel | Das Argument – Warum Eigentum verteilt werden muss, damit Freiheit Bestand hat | Die Bauanleitung – Warum Eigentum verteilt werden muss, damit Freiheit Bestand hat |
| Reihe | Die polyzentrische Ordnung, Nummer 1 | Die polyzentrische Ordnung, Nummer 2 |
| Ausgabennummer | leer lassen | leer lassen |
| Autor | Marcel Richtsteiger | Marcel Richtsteiger |
| Mitwirkende | keine | keine |
| Beschreibung | siehe unten | siehe unten |
| Veröffentlichungsrechte | Ich besitze das Urheberrecht und die erforderlichen Veröffentlichungsrechte | ebenso |
| Hauptzielgruppe | keine sexuell expliziten Inhalte; Lesealter leer lassen | ebenso |
| Hauptmarktplatz | Amazon.de | Amazon.de |
| Kategorien | siehe unten | siehe unten |
| Schlüsselwörter | siehe unten | siehe unten |
| Veröffentlichungsdatum | leer lassen | leer lassen |
| Erscheinungstermin (E-Book) | jetzt veröffentlichen, keine Vorbestellung | ebenso |

*Titel und Untertitel:* KDP verlangt, dass der Titel auf dem Umschlag steht und mit den Angaben übereinstimmt; Titel und Untertitel zusammen müssen unter 200 Zeichen bleiben. Bandnummern gehören in die Reihenangabe und nicht in den Titel. Der Bandtitel („Das Argument“, „Die Bauanleitung“) steht auf der Vorderseite und deshalb auch im Untertitel. So unterscheiden sich die beiden Bände bei Amazon schon im Namen.

*Reihe:* Sind beide Bände angelegt, werden sie in KDP unter „Reihe“ zu einer Reihe verbunden. Taschenbuch und E-Book desselben Bandes verknüpft Amazon selbst.

*Ausgabennummer:* Die Ausgabenummer des Repositoriums („Ausgabe 3.4“) zählt Quellstände und keine Auflagen. Bei KDP bleibt das Feld leer.

## Beschreibung

KDP nimmt bis zu 4.000 Zeichen; die beiden Texte haben rund 1.400 und 1.500. Im Feld mit Formatleiste wird die erste Zeile fett gesetzt. Wer lieber HTML einfügt, nimmt die Fassung darunter; KDP versteht dort unter anderem `<p>`, `<b>`, `<i>` und `<br>`.

### Band 1 – Das Argument

> **Der Staatssozialismus ist an konzentrierter Macht gescheitert. Ist die Marktwirtschaft davor sicher?**
>
> Dieses Buch misst beide Systeme mit demselben Maß – an zwölf Ländern, sechs mit Plan und sechs mit Markt. Für die Planwirtschaften gilt: Am Plan lag es nicht; es lag daran, wer plante und wofür. Und die Marktwirtschaft hat Macht nur dort gebändigt, wo Konkurrenz, Insolvenzrecht, Rechtsstaat, freie Presse und Gegenmacht sie begleiteten. Wo diese fehlen, bändigt der Markt nichts. Wo sie bestehen, müssen ihre Regeln gegen genau die verteidigt werden, die sie einhegen sollen – und sie rosten.
>
> Die entscheidende Frage ist deshalb, ob Macht in einem Zentrum zusammenläuft oder auf viele Träger verteilt ist, die einander Konkurrenz machen und scheitern dürfen. Daraus entsteht eine Ordnung aus drei Eigentumssektoren: Betriebe, die ihren Belegschaften gehören, Netze, Wasser und Wohnungen in gemeinwirtschaftlicher Hand und ein privater Sektor, in dem Vermögen entstehen darf, ohne dynastisch zu werden. Wo immer es geht, ersetzt sie Regeln durch Eigentum, denn Eigentum hat einen Träger, der es verteidigt.
>
> Jede These muss sich dem stärksten marxistischen und dem stärksten liberalen Einwand stellen. Eine Utopie verspricht dieses Buch nicht, auch keine gerechtere Welt. Es behauptet, dass diese Ordnung ihre Fehler eher überlebt.
>
> **Scheitert ein Modell, stirbt das Modell – nicht das Land.**

```html
<p><b>Der Staatssozialismus ist an konzentrierter Macht gescheitert. Ist die Marktwirtschaft davor sicher?</b></p>
<p>Dieses Buch misst beide Systeme mit demselben Maß – an zwölf Ländern, sechs mit Plan und sechs mit Markt. Für die Planwirtschaften gilt: Am Plan lag es nicht; es lag daran, wer plante und wofür. Und die Marktwirtschaft hat Macht nur dort gebändigt, wo Konkurrenz, Insolvenzrecht, Rechtsstaat, freie Presse und Gegenmacht sie begleiteten. Wo diese fehlen, bändigt der Markt nichts. Wo sie bestehen, müssen ihre Regeln gegen genau die verteidigt werden, die sie einhegen sollen – und sie rosten.</p>
<p>Die entscheidende Frage ist deshalb, ob Macht in einem Zentrum zusammenläuft oder auf viele Träger verteilt ist, die einander Konkurrenz machen und scheitern dürfen. Daraus entsteht eine Ordnung aus drei Eigentumssektoren: Betriebe, die ihren Belegschaften gehören, Netze, Wasser und Wohnungen in gemeinwirtschaftlicher Hand und ein privater Sektor, in dem Vermögen entstehen darf, ohne dynastisch zu werden. Wo immer es geht, ersetzt sie Regeln durch Eigentum, denn Eigentum hat einen Träger, der es verteidigt.</p>
<p>Jede These muss sich dem stärksten marxistischen und dem stärksten liberalen Einwand stellen. Eine Utopie verspricht dieses Buch nicht, auch keine gerechtere Welt. Es behauptet, dass diese Ordnung ihre Fehler eher überlebt.</p>
<p><b>Scheitert ein Modell, stirbt das Modell – nicht das Land.</b></p>
```

### Band 2 – Die Bauanleitung

> **Eine andere Wirtschaftsordnung ist schnell gefordert. Dieser Band zeigt, wie man sie baut – bis auf den Paragraphen.**
>
> Der erste Band hat gezeigt, dass Planwirtschaft und Marktwirtschaft an derselben Stelle verwundbar sind: an Macht, die in einem Zentrum zusammenläuft. Dieser Band baut die Ordnung, die daraus folgt, Stück für Stück: Betriebe, die ihren Belegschaften gehören, mit individuellen Kapitalkonten und echtem Insolvenzrisiko; Netze, Wasser und Wohnungen in gemeinwirtschaftlicher Hand, mit einem Sterberecht für schlechte Betreiber; ein privater Sektor, in dem Vermögen entstehen darf, ohne dynastisch zu werden; dazu die politische Architektur und der Sozialstaat, auf dem alles ruht.
>
> Der Weg dorthin beginnt im geltenden Recht, mit gewöhnlichen Mehrheiten und vorhandenem Geld: bei Mittelständlern ohne Nachfolger, die ihren Betrieb an die Belegschaft verkaufen können, und bei einer Erbschaftsteuer, die sich in Unternehmensanteilen zahlen lässt, damit kein Euro den Betrieb verlässt. Jedes Bauteil wird geprüft, bis es an eine Wand stößt – was es kostet, wer es bekämpfen wird, was von ihm übrig bliebe, wenn eine Regierung es nicht mehr will –, und für den ganzen Weg steht vorher fest, woran man erkennt, dass er gescheitert ist.
>
> Geschrieben für alle, die prüfen wollen, ob ein Bauteil hält: in Genossenschaft und Kommune, in Steuerberatung, Verwaltung und Rechtswissenschaft. Das erste Kapitel fasst das Argument des ersten Bandes zusammen; der Band ist für sich lesbar.

```html
<p><b>Eine andere Wirtschaftsordnung ist schnell gefordert. Dieser Band zeigt, wie man sie baut – bis auf den Paragraphen.</b></p>
<p>Der erste Band hat gezeigt, dass Planwirtschaft und Marktwirtschaft an derselben Stelle verwundbar sind: an Macht, die in einem Zentrum zusammenläuft. Dieser Band baut die Ordnung, die daraus folgt, Stück für Stück: Betriebe, die ihren Belegschaften gehören, mit individuellen Kapitalkonten und echtem Insolvenzrisiko; Netze, Wasser und Wohnungen in gemeinwirtschaftlicher Hand, mit einem Sterberecht für schlechte Betreiber; ein privater Sektor, in dem Vermögen entstehen darf, ohne dynastisch zu werden; dazu die politische Architektur und der Sozialstaat, auf dem alles ruht.</p>
<p>Der Weg dorthin beginnt im geltenden Recht, mit gewöhnlichen Mehrheiten und vorhandenem Geld: bei Mittelständlern ohne Nachfolger, die ihren Betrieb an die Belegschaft verkaufen können, und bei einer Erbschaftsteuer, die sich in Unternehmensanteilen zahlen lässt, damit kein Euro den Betrieb verlässt. Jedes Bauteil wird geprüft, bis es an eine Wand stößt – was es kostet, wer es bekämpfen wird, was von ihm übrig bliebe, wenn eine Regierung es nicht mehr will –, und für den ganzen Weg steht vorher fest, woran man erkennt, dass er gescheitert ist.</p>
<p>Geschrieben für alle, die prüfen wollen, ob ein Bauteil hält: in Genossenschaft und Kommune, in Steuerberatung, Verwaltung und Rechtswissenschaft. Das erste Kapitel fasst das Argument des ersten Bandes zusammen; der Band ist für sich lesbar.</p>
```

## Kategorien

KDP lässt je Buch drei Kategorien wählen. Sie hängen vom Marktplatz und vom Format ab: Das Taschenbuch steht im Bereich „Bücher“, das E-Book im „Kindle-Shop“. Die Namen hier sind die des Kategoriebaums von Amazon.de, Stand 24.09.2026. Beschriftet KDP eine davon anders, gilt die nächstliegende.

### Band 1 – Das Argument

*Taschenbuch:*

1. Bücher › Politik & Geschichte › Politikwissenschaft
2. Bücher › Politik & Geschichte › Politik nach Bereichen › Wirtschaftspolitik
3. Bücher › Fachbücher › Sozialwissenschaft › Politikwissenschaft › Politische Ideologien

*E-Book:*

1. Kindle-Shop › eBooks › Politik & Geschichte › Politikwissenschaft
2. Kindle-Shop › eBooks › Politik & Geschichte › Politik nach Bereichen › Wirtschaftspolitik
3. Kindle-Shop › eBooks › Fachbücher › Wirtschaft › Wirtschaftstheorie

### Band 2 – Die Bauanleitung

*Taschenbuch:*

1. Bücher › Politik & Geschichte › Politik nach Bereichen › Wirtschaftspolitik
2. Bücher › Business & Karriere › Wirtschaft › Gesellschaftsformen & -recht
3. Bücher › Politik & Geschichte › Politik nach Bereichen › Sozialpolitik

*E-Book:*

1. Kindle-Shop › eBooks › Politik & Geschichte › Politik nach Bereichen › Wirtschaftspolitik
2. Kindle-Shop › eBooks › Politik & Geschichte › Politik nach Bereichen › Sozialpolitik
3. Kindle-Shop › eBooks › Fachbücher › Wirtschaft › Wirtschaftswissenschaft

*Ausweichkategorien,* falls eine der obigen nicht angeboten wird: Politik & Geschichte › Geschichte nach Themen › Wirtschaftsgeschichte (passt zur Fallreihe des ersten Bandes), Business & Karriere › Wirtschaft › Wirtschaftsethik, Politik & Geschichte › Gesellschaft › Gesellschaftskritik.

## Schlüsselwörter

Sieben je Buch, für Taschenbuch und E-Book dieselben. KDP rät von Wörtern ab, die schon in Titel oder Untertitel stehen, und lässt keine Namen von Autoren zu, die mit dem Buch nichts zu tun haben, keine Anführungszeichen und keine Programmnamen wie „KDP Select“. Deshalb fehlen hier „polyzentrisch“, „Eigentum“, „Freiheit“ und Namen wie Marx, Hayek oder Ostrom. Jedes Schlüsselwort hat weniger als 50 Zeichen.

| | Band 1 – Das Argument | Band 2 – Die Bauanleitung |
|---|---|---|
| 1 | Kapitalismus Sozialismus Systemvergleich | Belegschaftseigentum Mitarbeiterbeteiligung |
| 2 | Planwirtschaft Marktwirtschaft Scheitern | Unternehmensnachfolge Mittelstand Belegschaft |
| 3 | Machtkonzentration Wirtschaft Demokratie | Erbschaftsteuer Reform Betriebsvermögen |
| 4 | Alternative Wirtschaftsordnung | Verantwortungseigentum Stiftung Vermögensbindung |
| 5 | Politische Ökonomie Gesellschaftsordnung | Genossenschaft Gemeinwirtschaft Wohnen |
| 6 | DDR Wirtschaft Reform Untergang | Sozialstaat Reform Rentenversicherung |
| 7 | Marxismus Liberalismus Kritik | Wirtschaftsdemokratie Gemeinwohl Kommune |

## Inhalt: Taschenbuch

| Feld | Einstellung |
|---|---|
| ISBN | kostenlose ISBN von KDP oder eigene, siehe unten |
| Druckoptionen: Tinte und Papier | Schwarzweiß auf weißem Papier |
| Druckoptionen: Format | 13,97 × 21,59 cm (5,5 × 8,5 Zoll) |
| Druckoptionen: Anschnitt | kein Anschnitt („No bleed“) |
| Druckoptionen: Einband | matt; wer Abrieb auf dem dunklen Grund scheut, nimmt glänzend |
| Manuskript | `…-kdp-innenteil-3.4.pdf` |
| Buchcover | „Einen bereits vorhandenen Umschlag hochladen“, Datei `…-kdp-umschlag-3.4.pdf` |
| Umschlag enthält Barcode | **nicht** anhaken: KDP druckt den Barcode selbst in das weiße Feld der Rückseite |
| KI-generierte Inhalte | Ja, siehe unten |
| Vorschau | Druckvorschau von KDP durchsehen, vor der Veröffentlichung ein Probeexemplar bestellen |

*Papier:* Es muss dasselbe sein wie `papier` in `satz/veroeffentlichung.toml`, derzeit „weiss“, sonst stimmt der Rücken nicht. Wer bei KDP „creme“ wählt, stellt die Datei vorher um und wartet die nächste Ausgabe ab.

*ISBN:* Die kostenlose ISBN von KDP führt als Verlag „Independently published“ und gilt nur für KDP. Eine eigene ISBN (in Deutschland über die MVB) nennt den Verfasser als Verlag, taugt auch für andere Vertriebswege und gehört dann in `satz/veroeffentlichung.toml`, damit sie im Impressum steht. In beiden Fällen druckt KDP den Barcode.

*Fest nach dem Veröffentlichen* sind Format, Druckfarbe und ISBN; das Papier eines Schwarzweißbuchs lässt sich nur eingeschränkt wechseln. Wer eines davon ändern will, legt eine neue Ausgabe an.

### KI-generierte Inhalte

KDP fragt, ob für Texte, Bilder oder Übersetzungen KI-Werkzeuge verwendet wurden, und verlangt die Angabe auch dann, wenn der erzeugte Inhalt danach umfangreich bearbeitet wurde. Für beide Bände und beide Formate:

| Frage | Antwort |
|---|---|
| KI-Werkzeuge verwendet? | Ja |
| Texte | Gesamtes Werk, mit umfangreicher Bearbeitung („Entire work, with extensive editing“) |
| Bilder | Ein oder wenige Bilder, mit minimaler oder keiner Bearbeitung („One or a few AI-generated images, with minimal or no editing“); gemeint ist der Umschlag, den eine KI als Satzcode entworfen hat |
| Übersetzungen | Keine |

Das Buch sagt im Abschnitt „Wie dieses Buch entstanden ist“ selbst, dass seine Prosa von einer KI stammt und in vielen Durchgängen überarbeitet wurde. Die Einstufung bei den Bildern ist eine Einschätzung; wer den Umschlag für umfangreich bearbeitet hält, wählt die Variante mit umfangreicher Bearbeitung.

## Inhalt: E-Book

| Feld | Einstellung |
|---|---|
| Digitale Rechteverwaltung (DRM) | Nein |
| Manuskript | `…-3.4.epub` |
| Buchcover | eigenes Titelbild hochladen, Datei `…-ebook-titelbild-3.4.jpg` (1600 × 2560 Pixel) |
| KI-generierte Inhalte | wie beim Taschenbuch |
| ISBN | leer lassen; KDP vergibt eine eigene Kennung |
| Vorschau | Online-Vorschau von KDP durchsehen |

*DRM:* Das Buch steht unter CC BY 4.0, ein Kopierschutz passt dazu nicht. Seit dem 20.01.2026 können Käufer eines Buches ohne DRM EPUB und PDF herunterladen, und die Einstellung lässt sich später ändern.

## Preisgestaltung: Taschenbuch

| Feld | Einstellung |
|---|---|
| Territorien | weltweite Rechte |
| Hauptmarktplatz | Amazon.de |
| Listenpreis | wird **ohne** Mehrwertsteuer eingegeben; Amazon.de schlägt 7 % auf |
| Tantieme | 60 % des Listenpreises ab 9,99 €, darunter 50 %, jeweils abzüglich Druckkosten |
| Druckkosten bei Amazon.de | 0,75 € je Buch plus 0,012 € je Seite |
| Erweiterter Vertrieb | optional: Großhändler in den USA und Großbritannien, 40 % abzüglich Druckkosten; für den deutschen Markt entbehrlich |

*Rechenbeispiel,* die Preise sind frei wählbar:

| | Band 1 | Band 2 |
|---|---|---|
| Ladenpreis mit 7 % MwSt. | 12,99 € | 14,99 € |
| Listenpreis ohne MwSt. (bei KDP einzugeben) | 12,14 € | 14,01 € |
| Druckkosten | 3,03 € | 3,63 € |
| Tantieme je Exemplar (60 %) | 4,25 € | 4,78 € |

Die 60 % gibt es ab 9,99 € ohne MwSt., also ab 10,69 € Ladenpreis. Darunter gelten 50 %, und der Listenpreis muss mindestens die doppelten Druckkosten decken: 6,06 € bei Band 1 und 7,26 € bei Band 2.

## Preisgestaltung: E-Book

| Feld | Einstellung |
|---|---|
| KDP Select | nein; es verlangt, dass das E-Book nur bei Amazon erhältlich ist, auch kostenlos nirgends sonst |
| Territorien | weltweite Rechte |
| Hauptmarktplatz | Amazon.de |
| Listenpreis | wird **mit** Mehrwertsteuer eingegeben |
| Tantieme 70 % | bei einem Listenpreis zwischen 2,69 € und 12,99 €, mindestens 20 % unter dem Preis des Taschenbuchs, abzüglich Zustellkosten von 0,10 € je MB |
| Tantieme 35 % | sonst |

*Rechenbeispiel:* Band 1 zu 5,99 € ergibt bei 70 % rund 3,90 € je Verkauf, Band 2 zu 6,99 € rund 4,55 € (70 % des Preises ohne MwSt., abzüglich weniger Cent Zustellkosten).

**Preisangleichung:** Ist ein E-Book anderswo kostenlos erhältlich, darf Amazon es ebenfalls kostenlos anbieten, und die Tantieme ist dann null. Das EPUB liegt frei im Netz; das Kindle-E-Book kann also jederzeit kostenlos werden. Wer das nicht will, kann nur auf das E-Book bei Amazon verzichten.

## Vor dem Veröffentlichen

1. Die Anschrift im Impressum steht (`satz/veroeffentlichung.toml`); der Satzlauf meldet keine Warnung.
2. Druckvorschau und Online-Vorschau von KDP ohne Beanstandung durchgesehen.
3. Probeexemplar beider Taschenbücher bestellt und geprüft: Rücken, Farben, Barcodefeld, Satzspiegel.
4. KI-Angabe gesetzt, KDP Select abgewählt.
5. Für in Deutschland verkaufte Bücher gilt die Buchpreisbindung, seit 2016 auch für E-Books. Ob ein kostenpflichtiges E-Book neben dem kostenlosen EPUB mit ihr vereinbar ist, vor dem Veröffentlichen klären.

## Nach dem Veröffentlichen

- Beide Bände in KDP zur Reihe „Die polyzentrische Ordnung“ verbinden (Nummer 1 und 2).
- Pflichtexemplare an die Deutsche Nationalbibliothek und an die zuständige Landesbibliothek liefern. Ist das Buch bei der Nationalbibliothek verzeichnet, `dnb_hinweis = true` in `satz/veroeffentlichung.toml` setzen, damit der Hinweis ins Impressum kommt.
- Bei jeder neuen Ausgabe, die veröffentlicht werden soll, Innenteil und Umschlag gemeinsam neu hochladen, dazu EPUB und Titelbild. KDP prüft das Buch dann erneut.

## Quellen

Hilfeseiten von KDP, abgerufen am 24.09.2026: [Kategorien](https://kdp.amazon.com/en_US/help/topic/G200652170), [Schlüsselwörter](https://kdp.amazon.com/en_US/help/topic/G201298500), [Beschreibung](https://kdp.amazon.com/en_US/help/topic/G201189630), [Titel und Metadaten](https://kdp.amazon.com/en_US/help/topic/G201097560), [Inhaltsrichtlinien und KI](https://kdp.amazon.com/en_US/help/topic/G200672390), [Druckkosten](https://kdp.amazon.com/en_US/help/topic/G201834340), [Tantieme Taschenbuch](https://kdp.amazon.com/en_US/help/topic/G201834330), [Mehrwertsteuer bei Druckbüchern](https://kdp.amazon.com/en_US/help/topic/GPQL5W3J6WNRCZTV), [Tantieme E-Book](https://kdp.amazon.com/en_US/help/topic/G200644210), [Preisgrenzen E-Book](https://kdp.amazon.com/en_US/help/topic/G200634560), [Preisregeln E-Book](https://kdp.amazon.com/en_US/help/topic/G200634500), [DRM](https://kdp.amazon.com/en_US/help/topic/GDDXGH9VR22ACM8U), [Erweiterter Vertrieb](https://kdp.amazon.com/en_US/help/topic/GQTT4W3T5AYK7L45), [Druckoptionen](https://kdp.amazon.com/en_US/help/topic/G201834180). Die Kategorien stammen aus dem Kategoriebaum der Bestsellerlisten von Amazon.de, abgerufen am selben Tag.

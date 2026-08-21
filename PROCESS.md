# PROCESS.md – Register der offenen Handwerksaufträge

Stand: 21.08.2026.

Dieses Verzeichnis hält fest, was am Text noch zu tun ist, ohne dass es eine Aussage des Textes betrifft: Belege, die nur mittelbar bestätigt sind, Fundstellen, die aus der Arbeitsumgebung nicht einsehbar waren, Zahlen ohne amtliche Quelle, Inkonsistenzen zwischen den Dateien. Anlass seiner Anlage war ein solcher Fall: Am 21.08.2026 ist die Wohnungsgemeinnützigkeit als Feldbeleg in Kapitel 12 eingearbeitet worden, ohne dass der Gesetzestext einsehbar war – der Auftrag stand danach nur in einem Nebensatz des Belegapparats und wäre dort verschwunden.

## Was hier hineingehört – und was nicht

Dieses Projekt führt vier Verzeichnisse, und sie dürfen einander nicht ersetzen.

**Das Ledger** (Manuskript Kapitel 26, Thesenpapier Sektion VI, Essay Sektion VIII) verzeichnet *inhaltliche* Flanken: Was diese Ordnung nicht leistet, nicht weiß oder nicht sichern kann. Es ist Teil des Buches und wird gelesen. Nach Hausregel 3 wächst es und schrumpft nie stillschweigend.

**Der Backlog** (`CLAUDE.md`, Abschnitt *Backlog*) verzeichnet *Ausbaukandidaten*: Konstruktionen, die noch nicht gebaut sind, und Kapitel, die noch nicht geschrieben sind. Er entscheidet, woran eine nächste Sitzung arbeitet.

**Die Präzisierungsaufträge** (`quellen_und_glossar.md`, Abschnitt *Aus der Verifikation folgende Präzisierungsaufträge*) sind ein abgeschlossenes Änderungsprotokoll vom 22.07.2026 und bleiben als Dokumentation stehen. Dort wird nichts Neues eingetragen.

**Dieses Verzeichnis** verzeichnet *Handwerksaufträge*: Arbeit an Belegen, Fundstellen und Konsistenz, die den Text nicht anders sagen lässt, sondern besser gesichert. Ein Eintrag hier ist kein Zugeständnis in der Sache. Wer eine Lücke in der Sache findet, trägt sie in das Ledger ein und nicht hier.

Die Abgrenzung in einem Satz: **Das Ledger sagt, was dieses Buch nicht kann; dieses Verzeichnis sagt, was an diesem Buch noch nicht getan ist.**

## Regeln

*Erstens: Ein Auftrag wird eingetragen, sobald er entsteht* – also in derselben Sitzung, in der ein Beleg nur mittelbar bestätigt werden konnte. Der Vermerk im Belegapparat bleibt daneben stehen; er ist die Auskunft an den Leser, dieses Verzeichnis die Auskunft an die Arbeit.

*Zweitens: Ein Auftrag wird nur durch Erledigung geschlossen,* nicht durch Zeitablauf und nicht durch erneutes Scheitern. Wer ihn versucht und scheitert, schreibt den Versuch mit Datum in den Eintrag. Gelöscht wird nichts: Erledigte Aufträge wandern nach unten in Abschnitt III und behalten ihr Datum. Das ist Hausregel 3, angewandt auf die eigene Arbeit.

*Drittens: Jeder Eintrag nennt seine Folge.* Was passiert mit dem Text, wenn der Auftrag nie erledigt wird? Steht dort „nichts", ist der Auftrag Fleißarbeit; steht dort eine Aussage, die fallen müsste, gehört er zusätzlich in das Ledger.

*Viertens: Nicht Belegbares wird nicht behauptet.* Ein offener Auftrag ist kein Freibrief, die Aussage vorläufig stärker zu führen, als der Beleg trägt. Das gilt besonders für Paragraphen- und Seitenangaben: Was nicht am Text geprüft ist, wird nicht zitiert, sondern umschrieben.

---

## I. Offen

### V2 – Erreichbarkeit der zitierten Netzadressen
**Angelegt:** 20.08.2026, fortgeschrieben 21.08.2026 (Durchlauf).
**Gegenstand:** Der Belegapparat führte Netzadressen mit dem Vermerk „indiziert", nicht „abgerufen".
**Durchlauf vom 21.08.2026:** Aus einer Umgebung ohne Ausgangsfilter sind alle 181 Adresszeilen (213 Einzeladressen) der Abschnitte A bis U mit `curl` direkt abgerufen worden – der frühere Befund, `bundestag.de`, `gesetze-im-internet.de`, `de.wikipedia.org` und `recht.nrw.de` seien gesperrt, galt nur für die vorige Arbeitsumgebung. 150 Zeilen antworten mit vollständigem Inhalt und tragen „abgerufen 21.08.2026"; acht weitere – die EUR-Lex-Richtlinien und -Verträge, deren Server `curl` nur eine leere 202-Antwort schickt – sind einzeln im Browser bestätigt und mit dem Zusatz „(im Browser)" umgestellt, sodass 158 der 181 Zeilen abgerufen sind. **Sechs tote oder umgezogene Adressen berichtigt:** das eingestellte `mlwerke.de` (drei MEW-Seiten, ersetzt durch `marxists.org` für die Inauguraladresse und durch das Internet Archive für Kapital III und den Anti-Dühring) – dieser Fall zeigt, warum die reine Statusabfrage nicht genügt: `mlwerke.de` liefert für jede Seite eine 935 Byte große Parkseite („Hier entsteht eine neue Homepage") unter Code 200, was nur die Größenprüfung des Rumpfes aufdeckt; das eingestellte FES-Portal „Erinnerungsorte" (Lassalle, ersetzt durch das Archiv der sozialen Demokratie); ein 404 bei Projekt Gutenberg (Kants „Zum ewigen Frieden", neue Adressstruktur); ein 404 im MieterEcho-Archiv (GSW-Verkauf, ersetzt durch die taz-Rückschau „Ausverkauf der Stadt").
**Was noch fehlt:** 24 Adresszeilen bleiben ganz oder teilweise „indiziert", weil der automatische Abruf nicht am fehlenden Netz scheitert, sondern an Bot-Schutz (akademische Verlage über `doi.org`, deGruyter mit leerer 202-Antwort, SEC, GAO, CanLII, `academic.oup.com`, `scholar.harvard.edu`, `asiasociety.org`, `ademe.fr`, `niemanlab.org`, `wola.org`), an einer Anmelde- oder Aboschranke (`iwkoeln.de`-Studienseite mit 401, Statista mit Weiterleitung auf Anmeldung, `dejure.org`) oder an reiner JavaScript-Auslieferung (die Zensus-Datenbank und der Heidelberger Katalog liefern nur einen 600 bis 1700 Byte großen Rumpf). Diese Ziele existieren und sind im Browser erreichbar; wie bei den EUR-Lex-Adressen ließe sich jede einzeln im Browser bestätigen und umstellen, doch die verbliebenen führen entweder hinter eine Bezahlschranke oder verlangen eine Sitzung je Adresse ohne tragenden Ertrag.
**Folge, falls offen:** gering und benannt. Die Einschränkung ist von „der ganze Apparat ist nur indiziert" auf „ein charakterisierter Rest von rund zwei Dutzend Adressen ist nur im Browser oder gar nur mit Abo erreichbar" geschrumpft; Kapitel 26 Abschnitt V führt sie in dieser engeren Fassung.
**Betroffene Stellen:** `quellen_und_glossar.md` durchgehend; `manuskript/26_offene_flanken.md` Abschnitt V.

### V3 – MEW-Seitenangaben gegen die gedruckte Ausgabe
**Angelegt:** 20.08.2026.
**Gegenstand:** die drei tragenden Marx- und Engels-Stellen – Genossenschaftsfabriken MEW 25, S. 456; ideeller Gesamtkapitalist MEW 20, S. 260; Verwaltung von Sachen MEW 20, S. 262.
**Was fehlt:** die Prüfung an der gedruckten Dietz-Ausgabe. Die Angaben sind über mehrere voneinander unabhängige Fundstellennachweise übereinstimmend bestätigt, aber nicht am Buch selbst.
**Was ihn schließt:** Einsicht in die gedruckte Ausgabe – Bibliothek oder ein einsehbares Digitalisat der Dietz-Bände. Konkret ausgeliehen werden könnten die beiden Scans im Internet Archive: `karlmarxfriedric0020marx` (MEW 20) und `karlmarxfriedric0025marx` (MEW 25); beide sind derzeit leihbeschränkt (Collection `printdisabled`/`internetarchivebooks`), die Volltextsuche antwortet mit „item not available", ein Konto mit Leihberechtigung öffnet sie.
**Versuch 21.08.2026:** Kein einsehbarer Scan der gedruckten Ausgabe erreichbar – die Internet-Archive-Bände sind leihbeschränkt, die Dietz-Ausgabe ist bei HathiTrust nicht im durchsuchbaren Bestand (acht Treffer zur Formel, alle 1891–1994, kein MEW-Band), Google Books ist aus dieser Umgebung gesperrt. **Dafür ein weiterer unabhängiger Nachweis gewonnen:** die über das Internet Archive erreichbare Textfassung von `mlwerke.de` führt die Dietz-Seitenzahlen als Marken im Fließtext und setzt jede der drei Stellen genau auf die zitierte Seite – die Genossenschaftsstelle „Die Kooperativfabriken der Arbeiter selbst …" zwischen den Marken |456| und |457|, „der ideelle Gesamtkapitalist" auf |260| (und nachweislich nicht auf |261|), „An die Stelle der Regierung über Personen tritt die Verwaltung von Sachen …" auf |262|. Das ist eine Transkription mit ausgewiesener Paginierung, nicht das gedruckte Buch, und ersetzt die Einsicht darum nicht; es macht die Seitenzahlen aber so sicher, wie es ohne den Band geht.
**Folge, falls offen:** gering. Übereinstimmende unabhängige Nachweise tragen die Angabe; die Kapitel 7 und 24 führen sie mit Status.
**Betroffene Stellen:** `manuskript/07_der_endzustand.md`, `manuskript/24_marxistische_gegenprobe.md`, `quellen_und_glossar.md`.

### V4 – Gesetzesmaterialien zur Neufassung des § 5 Abs. 1 Nr. 10 KStG
**Angelegt:** 21.08.2026.
**Gegenstand:** die Aussage, die einzige Steuerbefreiung, die die Aufhebung der Wohnungsgemeinnützigkeit überlebt hat, hänge am Mitglied statt am Status – und sei im selben Gesetzgebungsvorgang neu gefasst worden. Der Merksatz „Was an einem Status hing, wurde gestrichen; was am Mitglied hing, steht noch" ruht darauf.
**Was fehlt:** der Nachweis aus den Materialien. Der geltende Normtext ist bestätigt; die Zuordnung der Neufassung zum Steuerreformgesetz 1990 stammt aus der steuerrechtlichen Kommentarliteratur (Frotscher/Drüen zu § 5 KStG; Dötsch/Pung/Möhlenbrock).
**Was ihn schließt:** die Bundestagsdrucksache zum Steuerreformgesetz 1990 oder die Textfassung des Gesetzes im BGBl. I 1988, S. 1093 ff. an der Stelle, die § 5 KStG ändert.
**Folge, falls offen:** gering für die Sache, spürbar für die Zuspitzung. Fiele die Zuordnung, bliebe die Aussage über den heutigen Rechtszustand richtig und verlöre ihre Pointe über den Gesetzgebungsvorgang.
**Betroffene Stellen:** `manuskript/12_allmende_und_sterberecht.md` (Beleg *Was die Aufhebung überlebte*), `quellen_und_glossar.md` Abschnitt U, `polyzentrische_ordnung.md` Sektion III.

### V5 – Fundstelle des BGH-Urteils VIII ZR 201/23
**Angelegt:** 20.08.2026.
**Gegenstand:** die Erstreckung des mietrechtlichen Vorkaufsrechts auf Teileigentum (Urteil vom 21.05.2025), im Text als Beleg dafür geführt, dass der Zug vom Grundstück zum Kontrollwechsel anderswo bereits vollzogen ist.
**Was fehlt:** die Fundstelle in der amtlichen Sammlung; bestätigt ist das Urteil bisher über die Rechtsprechungsberichterstattung.
**Was ihn schließt:** Abruf des Urteils über die Entscheidungsdatenbank des Bundesgerichtshofs.
**Folge, falls offen:** gering. Aktenzeichen, Datum und Tenor sind übereinstimmend belegt.
**Betroffene Stellen:** `manuskript/12_allmende_und_sterberecht.md`, `quellen_und_glossar.md` Abschnitt T.

### V6 – Firmenhistorie der GSW
**Angelegt:** 21.08.2026.
**Gegenstand:** die Angabe, die 2004 von Berlin verkaufte Gesellschaft habe seit 1937 Gemeinnützige Siedlungs- und Wohnungsbaugesellschaft Berlin mbH geheißen – ein kleiner Beleg mit Beweiskraft für die Abfolge, weil die Gesellschaft den Status im Namen trug, bis er 1990 wegfiel.
**Was fehlt:** ein Registerauszug oder eine Unternehmensgeschichte aus erster Hand; bestätigt ist der Name bisher über Unternehmens- und Lexikondarstellungen.
**Was ihn schließt:** Handelsregisterauszug oder Firmenchronik.
**Folge, falls offen:** gering. Fiele die Jahreszahl, bliebe der Name selbst und mit ihm das Argument.
**Betroffene Stellen:** `manuskript/12_allmende_und_sterberecht.md` (Beleg *Berlin*), `quellen_und_glossar.md` Abschnitt U.

### V7 – Marktanteil der gemeinnützigen Wohnungsunternehmen in Großstädten
**Angelegt:** 21.08.2026.
**Gegenstand:** die Angabe, die gemeinnützigen Unternehmen hätten in Großstädten bis zu einem Drittel des Wohnungsangebots gestellt.
**Was fehlt:** eine amtliche oder wissenschaftliche Quelle. Die Größenordnung ist verbreitet und wird im Text als solche geführt.
**Was ihn schließt:** eine Wohnungsstatistik der achtziger Jahre oder eine Untersuchung zur Wohnungsgemeinnützigkeit mit Zahlenwerk.
**Folge, falls offen:** keine. Der Satz trägt kein Argument; er beziffert die Bedeutung des Falls. Bleibt die Quelle aus, kann er ersatzlos entfallen.
**Betroffene Stellen:** `manuskript/12_allmende_und_sterberecht.md` (Beleg *Wohnungsgemeinnützigkeit*), `quellen_und_glossar.md` Abschnitt U.

---

## II. Geprüft und entschieden

Was hier steht, ist kein Auftrag, sondern eine Warnung: Diese Fragen sind einmal geklärt worden und sehen aus, als wären sie es nicht.

*Datum des Steuerreformgesetzes 1990.* Es ist das Gesetz **vom 25.07.1988** (BGBl. I S. 1093), mit Wirkung der Aufhebung zum 01.01.1990. Ein Teil der steuerrechtlichen Kommentarliteratur nennt „25.7.1989"; das ist mit der Fundstelle im Bundesgesetzblatt und mit der Verfügung der OFD Frankfurt/M. vom 23.09.2013 (S 2730 A – 15 – St 53) nicht vereinbar. Die Jahreszahl 1988 gilt und wird nicht ohne neuen Beleg geändert.

*Dresden 2006 gehört nicht in die Linie der Wohnungsgemeinnützigkeit.* Die WOBA kam aus der Kommunalisierung des DDR-Wohnungsbestands und war nie nach dem WGG anerkannt; für die neuen Länder galt ohnehin eine eigene Übergangsregelung. In der WGG-Abfolge steht allein Berlin. Der Fall Dresden bleibt Beleg der Sicherungsstufen und wird nicht zum Beleg des Statusmodells umgewidmet.

*Arizmendiarrieta war Diözesanpriester des Bistums Vitoria, nicht Jesuit.* Der Fehler steht auch in seriösen Darstellungen und ist mehrfach zurückgewiesen worden.

*Die Vier-Prozent-Grenze des WGG 1940 steht in § 9, nicht in § 8.* Eine über Websuche gewonnene Zusammenfassung des recht.nrw.de-Bestands ordnete die Ausschüttungsgrenze § 8 und die Vermögensbindung § 9 zu. Das Faksimile des Reichsgesetzblatts (RGBl. I 1940, S. 439) widerlegt beides: § 8 regelt die Weiterveräußerung (auf mindestens zwanzig Jahre zu bestellende Sicherung gegen Preiserhöhung beim Weiterverkauf), die Grenze von vier vom Hundert der eingezahlten Kapitaleinlagen steht in § 9 Buchstabe a, die Vermögensbindung an gemeinnützige Zwecke bei Auflösung in § 11. Musterfall der vierten Regel dieses Verzeichnisses: Was nicht am Text geprüft ist, wird nicht zitiert – auch eine plausible Paragraphenfolge nicht.

---

## III. Erledigt

*21.08.2026 – V1, Paragraphenzählung des WGG.* Am Faksimile des Reichsgesetzblatts geprüft (RGBl. I 1940, Nr. 38, S. 437–439; Bekanntmachung der neuen Fassung vom 29.02.1940 ab S. 437, Gesetzestext ab S. 438). Die vier Bindungen: Geschäftskreis – Bau von Kleinwohnungen im eigenen Namen – § 6 (dazu betreuter Personenkreis § 5); Preisbindung – Überlassung nur zu angemessenen Preisen, Ermittlung in den Durchführungsvorschriften – § 7 Absatz 2; Gewinnbeteiligung höchstens vier vom Hundert der eingezahlten Kapitaleinlagen § 9 Buchstabe a, Rückzahlung beim Ausscheiden nur in Einlagenhöhe § 9 Buchstabe b; Vermögensbindung an gemeinnützige Zwecke bei Auflösung § 11, Baupflicht bereits § 6 Absatz 1. Prüfungsverband § 14, Anerkennungsbehörde § 16. Die Paragraphen stehen jetzt im Belegapparat von Kapitel 12 und in Abschnitt U von `quellen_und_glossar.md`. Gegenprobe: § 7 Absatz 2 deckt sich mit dem Sachstand WD 7-006/13, die Folge §§ 1–4 und die Querverweise § 14/§ 16 mit der bei Haufe wiedergegebenen, bis 1988 geltenden Fassung – die frühen Paragraphen sind zwischen 1940 und der Aufhebung 1990 unverändert. Der Faksimile-Abruf zählt zugleich als erster erledigter Punkt von V2 (die Quelle steht jetzt als „abgerufen", nicht „indiziert").

*21.08.2026 – K1, Kapitelzahl im README.* `README.md` beschrieb das Manuskript an zwei Stellen als „26 Kapitel" – im Abschnitt *Inhalt* und beim Verweis auf das PDF. Die Umnummerierung vom 16.08.2026, mit der Kapitel 17 eingefügt und die bisherigen 17 bis 26 zu 18 bis 27 wurden, war dort nie nachgezogen worden. Beide Stellen stehen jetzt auf 27. Die übrigen Zählungen des README sind bei dieser Gelegenheit gegengelesen und stimmen: acht Teile und acht Teilseiten, neun Sektionen des Essays, neun Befunde, elf Einwände der marxistischen Gegenprobe im Thesenpapier, sieben ausgewiesene Differenzen des Essays, sieben Teile des Thesenpapiers. Der Dauerverweis auf das PDF trägt ebenfalls: Der Satzlauf legt neben der nummerierten Ausgabe eigens eine Datei mit festem Namen bei.

*20.08.2026 – Furubotn/Pejovich und Ellerman.* Die Fundstellen zum Horizontproblem (ZfN 30/1970, S. 431–454) und zu den Kapitalkonten (JCE 10/1986, S. 62–78; *The Democratic Worker-Owned Firm*, 1990) sind vervollständigt und stehen in Kapitel 11.

*20.08.2026 – Landesbanken-Größenordnung.* Präzisiert: Die 68 bis 70 Milliarden betreffen die Bankenrettung insgesamt, die Landesbanken allein 40 bis 50 Milliarden, der WestLB-Fall amtlich rund 18 Milliarden. Steht in Kapitel 8.

*20.08.2026 – MEW-Seitenangaben, mittelbare Prüfung.* Mehrfach unabhängig bestätigt; die Prüfung an der gedruckten Ausgabe bleibt als V3 offen.

*22.07.2026 – zehn Präzisierungsaufträge aus der ersten Verifikationsrunde.* Vollständig eingearbeitet; die Liste steht als Änderungsdokumentation in `quellen_und_glossar.md`.

#!/usr/bin/env python3
"""Setzt die Kapiteldateien aus manuskript/ zu den Erzeugnissen beider Bände.

Das Manuskript erscheint in zwei Bänden – dem Argument und der Bauanleitung –,
und jeder Band liegt in einem eigenen Verzeichnis: manuskript/band1/ und
manuskript/band2/. Jedes hat seine eigene Inhaltsdatei und zählt seine
Kapitel von eins an. Aus jedem Band entstehen fünf Dateien in drei Gruppen:

*Leseausgabe:* das PDF zum Lesen am Bildschirm, mit Lesezeichen, anklickbarem
Inhaltsverzeichnis und der Akzentfarbe der Überschriften.

*Druckausgabe für KDP:* der Innenteil des Taschenbuchs und sein Umschlag. Der
Innenteil ist seitengleich mit der Leseausgabe, aber so gebaut, wie KDP ihn
annimmt – in Graustufen, ohne Lesezeichen und ohne Verweisflächen, mit
geradem Seitenumfang und einem Bund, der zur Seitenzahl passt. Den Umschlag,
Rückseite, Rücken und Vorderseite auf einem Bogen, rechnet der Lauf aus der
Seitenzahl dieses Innenteils: Wird das Buch dicker, wird der Rücken breiter.

*E-Book:* ein EPUB 3, wie KDP es annimmt, und das Titelbild dazu, ein JPEG
in 1600 × 2560 Pixeln.

Leseausgabe und Innenteil setzt LuaLaTeX nach der Vorlage in satz/vorlage.tex,
den Umschlag nach satz/umschlag.tex; das E-Book baut Pandoc nach
satz/epub-vorlage.xhtml und satz/epub.css. Was nicht im Manuskript steht –
Format, Papier, Impressum, ISBN –, steht in satz/veroeffentlichung.toml, der
Text der Umschlagrückseite in satz/umschlag/, die Stichwörter des Registers
in satz/register.toml. Ohne Angabe setzt der Lauf beide Bände und alle
Erzeugnisse.

Vier Dinge macht das Skript dabei, die Pandoc allein nicht könnte:

*Kapitelköpfe:* Jede Kapiteldatei beginnt mit „# Neuntes Kapitel" und
„## Fehlertoleranz" – zwei Überschriften für einen Kopf. Sie werden zu einem
Kapitelanfang zusammengezogen; alle übrigen Überschriften der Datei rücken
auf die Abschnittsebene. Gezählt wird im Satz mit Ziffern („9. Kapitel"),
und die Ziffer kommt aus dem Dateinamen; die ausgeschriebene Bezeichnung der
Quelle wird dagegen geprüft, damit ein Umnummerieren nicht unbemerkt bleibt.

*Teilseiten:* Welches Kapitel zu welchem Teil seines Bandes gehört, steht
nicht in den Kapiteldateien, sondern im Aufbau-Abschnitt von 00_inhalt.md. Von
dort wird die Zuordnung gelesen, damit sie nur an einer Stelle gepflegt
werden muss. Gesetzt wird dieser eine Abschnitt nicht: Das Buch hat sein
Inhaltsverzeichnis, und derselbe Baum ein zweites Mal unmittelbar dahinter
wäre eine Dopplung. Im Verzeichnis bleibt er, wo er gebraucht wird – dort
gibt es kein Inhaltsverzeichnis, das ein Satzlauf erzeugt.

*Anführungszeichen:* Die Quellen setzen das öffnende Zeichen typografisch
(„), das schließende als geraden Zoll ("). Für den Satz wird daraus das
deutsche Paar „…“ beziehungsweise ‚…‘.

*Register:* Am Ende jedes Bandes steht ein Register der Begriffe, ohne
Erklärungen, nur mit Fundstellen. Die Stichwörter stehen in
satz/register.toml; gesucht wird im Fließtext der Kapitel, und an jeder
Fundstelle setzt der Lauf eine unsichtbare Marke. Im PDF wird daraus eine
Seitenzahl, im E-Book ein Verweis. Die Quellen bleiben dabei unberührt.

Aufruf:

    python3 satz/build.py                          # alles, beide Bände, nach build/
    python3 satz/build.py --band 1                 # nur den ersten Band
    python3 satz/build.py --nur lesen              # nur die Leseausgaben
    python3 satz/build.py --nur druck --nur ebook  # Innenteil, Umschlag, E-Book
    python3 satz/build.py --kennung 3.4            # Ausgabenummer für Impressum und Dateinamen
    python3 satz/build.py --band 2 --ziel /tmp/probe
    python3 satz/build.py --band 1 --nur-quelltext # nur den Zwischenstand zeigen
"""

from __future__ import annotations

import argparse
import datetime
import functools
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tomllib
import unicodedata
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

SATZ = Path(__file__).resolve().parent
WURZEL = SATZ.parent
MANUSKRIPT = WURZEL / "manuskript"
# Die beiden Bände, jeder in seinem Verzeichnis. Die Zahl ist die Bandnummer,
# und aus ihr entstehen Verzeichnis- und Dateiname.
BAENDE = (1, 2)
VORLAGE = SATZ / "vorlage.tex"
UMSCHLAG = SATZ / "umschlag.tex"
EPUB_VORLAGE = SATZ / "epub-vorlage.xhtml"
EPUB_STIL = SATZ / "epub.css"
ANGABEN = SATZ / "veroeffentlichung.toml"
UMSCHLAGTEXTE = SATZ / "umschlag"
REGISTER = SATZ / "register.toml"
# Die Schriftschnitte liegen im Verzeichnis, nicht im TeX-Baum: So setzt
# jeder Rechner mit denselben Dateien, und der Bauläufer braucht kein
# Schriftpaket. Den Pfad bekommen die Vorlagen als Variable herein.
SCHRIFTEN = SATZ / "schriften"
INHALT = "00_inhalt.md"
# Der Abschnitt des Vorspanns, aus dem die Teilzuordnung kommt. Er ist der
# einzige, der gelesen und nicht gesetzt wird – siehe lies_band.
AUFBAU = "Aufbau"
STAMM = "polyzentrische-ordnung"

# Die Erzeugnisse eines Bandes: Zusatz im Dateinamen und Endung. Die
# Leseausgabe behält den Namen, unter dem das PDF seit jeher erscheint;
# darauf zeigen die Dauerverweise.
ERZEUGNISSE = {
    "lesen": ("", ".pdf"),
    "innenteil": ("-kdp-innenteil", ".pdf"),
    "umschlag": ("-kdp-umschlag", ".pdf"),
    "ebook": ("", ".epub"),
    "titelbild": ("-ebook-titelbild", ".jpg"),
}
# Was sich mit --nur auswählen lässt, und was jeweils entsteht.
GRUPPEN = {
    "lesen": ("lesen",),
    "druck": ("innenteil", "umschlag"),
    "ebook": ("titelbild", "ebook"),
}

# --------------------------------------------------------------------------
# Vorgaben von KDP
# --------------------------------------------------------------------------
# Stand September 2026, aus den Hilfeseiten von Kindle Direct Publishing
# zu Format, Rändern, Umschlag und E-Book-Titelbild. Maße in Zoll, weil KDP
# in Zoll rechnet.

# Die Standardformate für Taschenbücher, Breite × Höhe. Ein anderes Format
# nimmt KDP als Sonderformat an, aber nicht für jeden Vertriebsweg.
KDP_FORMATE = {
    (5.0, 8.0), (5.06, 7.81), (5.25, 8.0), (5.5, 8.5), (6.0, 9.0),
    (6.14, 9.21), (6.69, 9.61), (7.0, 10.0), (7.44, 9.69), (7.5, 9.25),
    (8.0, 10.0), (8.25, 6.0), (8.25, 8.25), (8.5, 8.5), (8.5, 11.0),
    (8.27, 11.69),
}
# Der Mindestbund nach Seitenzahl: bis 150 Seiten 0,375 Zoll, bis 300 Seiten
# 0,5 Zoll und so fort. Außen, oben und unten verlangt KDP ohne Beschnitt
# mindestens 0,25 Zoll; die Vorlage hält überall mehr.
KDP_BUND = ((150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875))
KDP_SEITEN = (24, 828)
# Papierstärke je Seite: Daraus und aus der Seitenzahl folgt die
# Rückenbreite.
KDP_PAPIER = {"weiss": 0.002252, "creme": 0.0025}
KDP_BESCHNITT = 0.125
# Rückentext druckt KDP nur bei mehr als 79 Seiten, und er muss zu beiden
# Falzen 0,0625 Zoll Abstand halten.
KDP_RUECKENTEXT_AB = 80
KDP_FALZLUFT = 0.0625
# Das Titelbild des E-Books: 1600 × 2560 Pixel, Seitenverhältnis 1 : 1,6.
TITELBILD_PIXEL = (1600, 2560)

# Der Bund, den die Vorlage aus typografischen Gründen hält, in Millimetern.
# Er liegt über dem, was KDP bis 700 Seiten verlangt; wird ein Band dicker,
# setzt der Lauf ihn mit dem verlangten Bund neu.
BUND_MM = 20.0
# Die Schriftgröße des Rückentexts, wo der Rücken sie trägt.
RUECKEN_PT = 11.0

MM_JE_ZOLL = 25.4


class Fehler(Exception):
    """Ein Problem, das den Satz abbricht und erklärt werden muss."""


# Warnungen sammeln sich hier und stehen am Ende in ausgabe.json, damit der
# Workflow sie in die Zusammenfassung und die Veröffentlichung übernehmen
# kann. Eine Warnung bricht nichts ab: Die Leseausgabe soll erscheinen, auch
# wenn dem Druckbogen noch etwas fehlt.
WARNUNGEN: list[str] = []


def warne(text: str) -> None:
    WARNUNGEN.append(text)
    print(f"  Warnung: {text}", file=sys.stderr)


def hinweis(text: str) -> None:
    print(f"  {text}", file=sys.stderr)


# --------------------------------------------------------------------------
# Typografie
# --------------------------------------------------------------------------


HOCHSTELLEN = {hoch: str(ziffer) for ziffer, hoch in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
TIEFSTELLEN = {tief: str(ziffer) for ziffer, tief in enumerate("₀₁₂₃₄₅₆₇₈₉")}


def gestellte_ziffern(text: str) -> str:
    """Ersetzt hoch- und tiefgestellte Ziffern durch echten LaTeX-Satz.

    Brotschriften führen diese Zeichen selten mit; Pagella etwa kennt das
    tiefgestellte Zwei aus „CO₂" nicht, und LuaTeX setzt an solchen Stellen
    stillschweigend nichts. Der Satzbefehl erzeugt die Ziffer stattdessen
    aus der vorhandenen Schrift.
    """
    for zeichen, ziffer in HOCHSTELLEN.items():
        text = text.replace(zeichen, rf"\textsuperscript{{{ziffer}}}")
    for zeichen, ziffer in TIEFSTELLEN.items():
        text = text.replace(zeichen, rf"\textsubscript{{{ziffer}}}")
    return text


def gestellte_ziffern_markdown(text: str) -> str:
    """Dasselbe für das E-Book: Pandocs Hoch- und Tiefstellung statt Zeichen.

    Welche Schrift ein Lesegerät nimmt, bestimmt der Leser. Ob sie „₂“ führt,
    weiß niemand; ein <sub> setzt jede.
    """
    text = re.sub(
        "[⁰¹²³⁴⁵⁶⁷⁸⁹]+",
        lambda m: "^" + "".join(HOCHSTELLEN[z] for z in m.group()) + "^",
        text,
    )
    return re.sub(
        "[₀₁₂₃₄₅₆₇₈₉]+",
        lambda m: "~" + "".join(TIEFSTELLEN[z] for z in m.group()) + "~",
        text,
    )


def deutsche_anfuehrung(text: str) -> str:
    """Setzt die schließenden Anführungszeichen deutsch.

    Die Quellen schreiben »„Zitat"« – öffnend typografisch, schließend als
    gerades Zollzeichen. Zu jedem öffnenden Zeichen wird das nächste gerade
    Zeichen zum passenden schließenden gemacht. Doppelte und einfache
    Anführung stören einander nicht, weil sie verschiedene Zeichen benutzen.
    """
    for auf, gerade, zu in (("„", '"', "“"), ("‚", "'", "‘")):
        teile = text.split(auf)
        for i in range(1, len(teile)):
            teile[i] = teile[i].replace(gerade, zu, 1)
        text = auf.join(teile)
    return text


def typografie(text: str) -> str:
    """Alle Eingriffe am Fließtext, die Pandoc nicht selbst vornimmt.

    Dazu gehört der schmale Abstand, wo ein einfaches und ein doppeltes
    Anführungszeichen aufeinandertreffen („‚System‘“): Pandoc setzte ihn
    selbst, solange es die Zeichen in TeX-Umschreibungen übersetzte, und
    seit es das nicht mehr tut (siehe LATEX), steht er hier.
    """
    text = gestellte_ziffern(deutsche_anfuehrung(text))
    for paar in ("‘“", "„‚"):
        text = text.replace(paar, paar[0] + r"\thinspace{}" + paar[1])
    return text


def typografie_epub(text: str) -> str:
    """Dieselben Eingriffe für das E-Book."""
    return gestellte_ziffern_markdown(deutsche_anfuehrung(text))


def als_latex(text: str) -> str:
    """Bereitet Fließtext für die Übergabe als LaTeX-Argument auf.

    Überschriften wandern als Makroargument in den Satz und kommen damit an
    Pandocs Textbehandlung vorbei; die paar nötigen Ersetzungen stehen hier.
    """
    text = deutsche_anfuehrung(text)
    text = text.replace("'", "’")
    for zeichen, ersatz in (
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ):
        text = text.replace(zeichen, ersatz)
    # Erst nach dem Maskieren, weil dieser Schritt selbst LaTeX erzeugt.
    return gestellte_ziffern(text)


# --------------------------------------------------------------------------
# Angaben zur Veröffentlichung
# --------------------------------------------------------------------------


@dataclass
class Angaben:
    """Was satz/veroeffentlichung.toml festlegt."""

    breite: float
    hoehe: float
    papier: str
    lizenz: str
    lizenz_kurz: str
    lizenz_url: str
    verzeichnis: str
    verlag: str
    selbstverlag: bool
    anschrift: str
    druck: str
    dnb_hinweis: bool
    isbn: dict[tuple[int, str], str] = field(default_factory=dict)

    def isbn_fuer(self, band: int, ausgabe: str) -> str:
        return self.isbn.get((band, ausgabe), "")


def isbn13_gueltig(ziffern: str) -> bool:
    """Prüfziffer einer ISBN-13: Gewichte abwechselnd 1 und 3, Summe durch zehn teilbar."""
    if len(ziffern) != 13 or not ziffern.isdigit():
        return False
    return sum(int(z) * (3 if i % 2 else 1) for i, z in enumerate(ziffern)) % 10 == 0


def lies_angaben(pfad: Path = ANGABEN) -> Angaben:
    if not pfad.is_file():
        raise Fehler(f"{pfad} fehlt – ohne Angaben zur Veröffentlichung kein Impressum.")
    try:
        daten = tomllib.loads(pfad.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as fehler:
        raise Fehler(f"{pfad.name} ist kein gültiges TOML: {fehler}") from None

    def wert(abschnitt: str, schluessel: str, art: type, vorgabe=None):
        inhalt = daten.get(abschnitt, {}).get(schluessel, vorgabe)
        if inhalt is None:
            raise Fehler(f"{pfad.name}: [{abschnitt}] {schluessel} fehlt.")
        if art is float and isinstance(inhalt, int):
            inhalt = float(inhalt)
        if not isinstance(inhalt, art):
            raise Fehler(f"{pfad.name}: [{abschnitt}] {schluessel} hat die falsche Art.")
        return inhalt.strip() if isinstance(inhalt, str) else inhalt

    angaben = Angaben(
        breite=wert("format", "breite", float),
        hoehe=wert("format", "hoehe", float),
        papier=wert("format", "papier", str),
        lizenz=wert("werk", "lizenz", str),
        lizenz_kurz=wert("werk", "lizenz_kurz", str),
        lizenz_url=wert("werk", "lizenz_url", str),
        verzeichnis=wert("werk", "verzeichnis", str).rstrip("/"),
        verlag=wert("impressum", "verlag", str),
        selbstverlag=wert("impressum", "selbstverlag", bool, False),
        anschrift=wert("impressum", "anschrift", str, ""),
        druck=wert("impressum", "druck", str, ""),
        dnb_hinweis=wert("impressum", "dnb_hinweis", bool, False),
    )
    for band in BAENDE:
        for ausgabe in ("taschenbuch", "ebook"):
            nummer = wert(f"band{band}", f"isbn_{ausgabe}", str, "")
            if nummer:
                ziffern = re.sub(r"[^0-9X]", "", nummer.upper())
                if len(ziffern) != 13:
                    raise Fehler(
                        f"{pfad.name}: [band{band}] isbn_{ausgabe} = „{nummer}“ hat "
                        "nicht dreizehn Stellen."
                    )
                if not isbn13_gueltig(ziffern):
                    raise Fehler(
                        f"{pfad.name}: [band{band}] isbn_{ausgabe} = „{nummer}“ hat "
                        "eine falsche Prüfziffer."
                    )
                angaben.isbn[(band, ausgabe)] = nummer

    if angaben.papier not in KDP_PAPIER:
        raise Fehler(
            f"{pfad.name}: papier = „{angaben.papier}“ – KDP kennt hier "
            f"{' und '.join(KDP_PAPIER)}."
        )
    if (angaben.breite, angaben.hoehe) not in KDP_FORMATE:
        warne(
            f"Das Format {zoll(angaben.breite)} × {zoll(angaben.hoehe)} Zoll ist kein "
            "Standardformat von KDP; dort gilt es als Sonderformat."
        )
    return angaben


def zoll(wert: float) -> str:
    """Eine Zollangabe, wie man sie liest: 5,5 statt 5.5000."""
    return f"{wert:.4f}".rstrip("0").rstrip(".").replace(".", ",")


def ohne_schema(url: str) -> str:
    return re.sub(r"^https?://", "", url).rstrip("/")


# --------------------------------------------------------------------------
# Quellen lesen
# --------------------------------------------------------------------------


def bandverzeichnis(band: int) -> Path:
    return MANUSKRIPT / f"band{band}"


def lies_titelei(text: str) -> dict[str, str]:
    """Zieht Titel, Untertitel, Band, Verfasser und Stand aus 00_inhalt.md.

    Gelesen wird nur der Kopf – alles vor dem ersten Abschnitt. Sonst
    verwechselte der Verfassername sich mit den fett gesetzten Teilzeilen
    des Aufbaus. Die Bandzeile steht als `####` unter dem Untertitel
    („Erster Band: Das Argument").
    """
    kopf = re.split(r"^## ", text, maxsplit=1, flags=re.M)[0]
    titel = re.search(r"^# (.+)$", kopf, re.M)
    untertitel = re.search(r"^### (.+)$", kopf, re.M)
    band = re.search(r"^#### (.+)$", kopf, re.M)
    autor = re.search(r"^\*\*(.+?)\*\*$", kopf, re.M)
    # Bis zum 25.09.2026 hieß die Zeile „Manuskript. Stand: …“; beide Formen
    # werden gelesen, auf die Titelseite kommt nur der Stand.
    stand = re.search(r"^\*(?:Manuskript\.\s*)?(Stand:[^*]+)\*$", kopf, re.M)
    if not titel:
        raise Fehler(f"{INHALT}: keine Titelzeile (# …) gefunden.")
    return {
        "titel": titel.group(1).strip(),
        "untertitel": untertitel.group(1).strip() if untertitel else "",
        "band": band.group(1).strip() if band else "",
        "autor": autor.group(1).strip() if autor else "",
        "stand": stand.group(1).strip().rstrip(".") if stand else "",
    }


def lies_vorspann(text: str) -> list[tuple[str, str]]:
    """Zerlegt 00_inhalt.md in seine Abschnitte (## Überschrift plus Text)."""
    abschnitte: list[tuple[str, str]] = []
    for treffer in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        titel = treffer.group(1).strip()
        rumpf = treffer.group(2).strip().strip("-").strip()
        abschnitte.append((titel, rumpf))
    if not abschnitte:
        raise Fehler(f"{INHALT}: keine Abschnitte (## …) gefunden.")
    return abschnitte


def lies_teile(aufbau: str) -> list[tuple[str, list[int]]]:
    """Liest aus dem Aufbau-Abschnitt, welche Kapitel zu welchem Teil gehören.

    Erwartet wird ein Wechsel aus fetten Teilüberschriften (**Teil I – …**)
    und kursiven Kapitelzeilen (*1. Eine Frage …*).
    """
    teile: list[tuple[str, list[int]]] = []
    for zeile in aufbau.splitlines():
        zeile = zeile.strip()
        teil = re.match(r"^\*\*(Teil .+?)\*\*$", zeile)
        if teil:
            teile.append((teil.group(1).strip(), []))
            continue
        kapitel = re.match(r"^\*(\d+)\.\s", zeile)
        if kapitel and teile:
            teile[-1][1].append(int(kapitel.group(1)))
    if not teile:
        raise Fehler(
            f"{INHALT}: im Abschnitt „{AUFBAU}“ ließ sich kein Teil erkennen. "
            "Erwartet werden Zeilen der Form **Teil I – Die Frage** und "
            "darunter *1. Kapitelname.*"
        )
    return teile


def lies_kapitel(pfad: Path) -> dict[str, str]:
    """Zerlegt eine Kapiteldatei in Kapitelbezeichnung, Titel und Rumpf."""
    text = pfad.read_text(encoding="utf-8")
    kopf = re.match(r"\s*# (.+?)\n+## (.+?)\n(.*)", text, re.S)
    if not kopf:
        raise Fehler(
            f"{pfad.name}: erwartet wird eine Kapitelbezeichnung (# Neuntes "
            "Kapitel) und darunter der Kapiteltitel (## Fehlertoleranz)."
        )
    rumpf = kopf.group(3).lstrip()
    # Der Trennstrich direkt unter dem Titel ist eine Setzanweisung der
    # Quelle; im Satz übernimmt das der Kapitelkopf.
    rumpf = re.sub(r"^-{3,}\s*\n", "", rumpf).lstrip()
    return {
        "bezeichnung": kopf.group(1).strip(),
        "titel": kopf.group(2).strip(),
        "rumpf": rumpf,
    }


def kapitelnummer(pfad: Path) -> int:
    return int(pfad.name[:2])


# --------------------------------------------------------------------------
# Kapitelzählung
# --------------------------------------------------------------------------
# Die Quellen benennen ihre Kapitel ausgeschrieben („Siebzehntes Kapitel“),
# gesetzt wird die Ziffer („17. Kapitel“). Maßgeblich für die Zahl ist der
# Dateiname, denn er bestimmt auch die Reihenfolge und ist es, worauf sich
# der Aufbau in 00_inhalt.md bezieht. Die ausgeschriebene Bezeichnung taucht
# im PDF damit nicht mehr auf – deshalb wird sie wenigstens geprüft: Wer
# Dateien umnummeriert und die Überschriften stehen lässt, soll es im Lauf
# lesen und nicht erst Jahre später im Text.


EINER = ("", "ein", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun")
ZEHNER = ("", "zehn", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig",
          "siebzig", "achtzig", "neunzig")
ZEHN_BIS_NEUNZEHN = ("zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn",
                     "sechzehn", "siebzehn", "achtzehn", "neunzehn")
ORDNUNGSSTAMM = ("erst", "zweit", "dritt", "viert", "fünft", "sechst", "siebt",
                 "acht", "neunt", "zehnt", "elft", "zwölft")


def grundzahl(nummer: int) -> str:
    """Schreibt eine Zahl von 1 bis 99 aus („sechsundzwanzig")."""
    if nummer < 10:
        return EINER[nummer]
    if nummer < 20:
        return ZEHN_BIS_NEUNZEHN[nummer - 10]
    zehner, einer = divmod(nummer, 10)
    if einer:
        return f"{EINER[einer]}und{ZEHNER[zehner]}"
    return ZEHNER[zehner]


def ordnungszahl(nummer: int) -> str:
    """Bildet die Ordnungszahl, wie eine Kapitelüberschrift sie schreibt.

    Bis zwölf sind die Stämme unregelmäßig, danach hängt das Deutsche ein
    „t" an (dreizehnt-) und ab zwanzig ein „st" (zwanzigst-). Die Endung
    ist immer die des sächlichen Nominativs, weil das Wort „Kapitel" folgt.

    Jenseits von neunundneunzig gibt die Funktion auf und liefert nichts:
    Ein Buch mit dreistelliger Kapitelzahl ist ein anderes Problem.
    """
    if not 1 <= nummer <= 99:
        return ""
    if nummer <= 12:
        stamm = ORDNUNGSSTAMM[nummer - 1]
    elif nummer < 20:
        stamm = grundzahl(nummer) + "t"
    else:
        stamm = grundzahl(nummer) + "st"
    return stamm.capitalize() + "es"


def kapitelbezeichnung(nummer: int) -> str:
    """Die Zeile über dem Kapiteltitel, so wie sie im Satz erscheint."""
    return f"{nummer}. Kapitel"


def bezeichnung_stimmt(bezeichnung: str, nummer: int) -> bool:
    """Prüft die ausgeschriebene Bezeichnung der Quelle gegen die Zahl.

    Wo sich keine Ordnungszahl bilden lässt, wird nicht geprüft: Der Satz
    soll an einer Prüfung nicht mehr Anstoß nehmen als am Text selbst.
    """
    erwartet = ordnungszahl(nummer)
    return not erwartet or bezeichnung.strip() == f"{erwartet} Kapitel"


# --------------------------------------------------------------------------
# Einen Band lesen
# --------------------------------------------------------------------------


@dataclass
class Kapitel:
    nummer: int
    datei: Path
    titel: str
    text: str
    belege: str


@dataclass
class Band:
    nummer: int
    verzeichnis: Path
    titelei: dict[str, str]
    # Der Vorspann ohne den Aufbau-Abschnitt, also das, was gesetzt wird.
    vorspann: list[tuple[str, str]]
    teile: list[tuple[str, list[int]]]
    kapitel: list[Kapitel]
    # Die Stichwörter des Registers mit ihren Fundstellen, siehe baue_register.
    register: list[Registereintrag] = field(default_factory=list)

    def teil_von(self, nummer: int) -> str | None:
        for teiltitel, nummern in self.teile:
            if nummer in nummern:
                return teiltitel
        return None


def teile_belege_ab(rumpf: str) -> tuple[str, str]:
    """Trennt den Belegapparat vom Fließtext des Kapitels ab.

    Der Apparat steht immer am Schluss unter der Überschrift „Belege“; ein
    Trennstrich unmittelbar davor gehört zu ihm und entfällt.
    """
    treffer = re.search(r"^#{2,4}\s*Belege\s*$", rumpf, re.M)
    if not treffer:
        return rumpf, ""
    text = rumpf[: treffer.start()]
    belege = rumpf[treffer.end() :].strip()
    text = re.sub(r"\n-{3,}\s*$", "", text.rstrip()).rstrip()
    return text, belege


def setze_ueberschriften(rumpf: str, ebene: int = 2) -> str:
    """Hebt alle verbliebenen Überschriften des Kapitels auf eine Ebene.

    Innerhalb eines Kapitels gliedern die Quellen mal mit ##, mal mit ###
    (das Ledger tut beides). Für den Satz ist das dieselbe Ebene: der
    Abschnitt unterhalb des Kapitels. Im PDF ist das die zweite, im E-Book,
    wo die Teile die erste und die Kapitel die zweite Ebene bilden, die
    dritte.
    """
    return re.sub(r"^#{2,6}\s+", "#" * ebene + " ", rumpf, flags=re.M)


def lies_band(nummer: int) -> Band:
    """Liest einen Band und meldet, was an seiner Struktur nicht stimmt."""
    verzeichnis = bandverzeichnis(nummer)
    inhalt_pfad = verzeichnis / INHALT
    if not inhalt_pfad.is_file():
        raise Fehler(f"{inhalt_pfad} fehlt – ohne Inhaltsdatei kein Satz.")
    inhalt = inhalt_pfad.read_text(encoding="utf-8")

    titelei = lies_titelei(inhalt)
    vorspann = lies_vorspann(inhalt)
    teile = lies_teile(dict(vorspann).get(AUFBAU, ""))

    dateien = sorted(p for p in verzeichnis.glob("[0-9][0-9]_*.md") if p.name != INHALT)
    if not dateien:
        raise Fehler(f"In {verzeichnis} liegt keine Kapiteldatei.")

    band = Band(
        nummer=nummer,
        verzeichnis=verzeichnis,
        titelei=titelei,
        # Der Aufbau ist Quelle und nicht Text: Seine Teilzuordnung braucht
        # der Satz, seine Kapitelzeilen stünden im Buch als zweites
        # Inhaltsverzeichnis wenige Seiten hinter dem ersten.
        vorspann=[(titel, rumpf) for titel, rumpf in vorspann if titel != AUFBAU],
        teile=teile,
        kapitel=[],
    )

    ohne_teil: list[str] = []
    for pfad in dateien:
        zahl = kapitelnummer(pfad)
        quelle = lies_kapitel(pfad)
        if band.teil_von(zahl) is None:
            ohne_teil.append(pfad.name)
        if not bezeichnung_stimmt(quelle["bezeichnung"], zahl):
            hinweis(
                f"Hinweis: {pfad.name} nennt sich „{quelle['bezeichnung']}“, "
                f"gesetzt wird nach dem Dateinamen als {kapitelbezeichnung(zahl)}."
            )
        text, belege = teile_belege_ab(quelle["rumpf"])
        if not belege:
            hinweis(f"Hinweis: {pfad.name} hat keinen Belegabschnitt.")
        band.kapitel.append(Kapitel(zahl, pfad, quelle["titel"], text, belege))

    if ohne_teil:
        hinweis(
            "Hinweis: ohne Teilzuordnung im Aufbau von "
            f"{INHALT}, deshalb ohne Teilseite gesetzt: {', '.join(ohne_teil)}"
        )
    hinweis(
        f"Band {nummer}: {len(band.kapitel)} Kapitel in {len(teile)} Teilen, "
        f"{len(band.vorspann)} Vorspannabschnitte gesetzt, {AUFBAU} nur gelesen."
    )
    baue_register(band)
    return band


# --------------------------------------------------------------------------
# Register
# --------------------------------------------------------------------------
# Am Ende jedes Bandes steht ein Register der Begriffe. Es nennt Fundstellen
# und erklärt nichts: Jede Erklärung, die dort stünde, wäre eine weitere
# Fassung eines Begriffs neben der im Text, und zwei Fassungen driften.
#
# Die Stichwörter stehen je Band in satz/register.toml, jedes mit den
# Wortformen, nach denen gesucht wird, und wahlweise mit einer wörtlichen
# Wortfolge aus dem Satz, der den Begriff in diesem Band erklärt. Gesucht
# wird nur im Fließtext der Kapitel – nicht im Vorspann, nicht in den
# Überschriften, nicht im Belegapparat. Erfasst wird je Kapitel die erste
# Nennung und dazu die Erklärungsstelle. An jede dieser Stellen setzt der
# Lauf eine unsichtbare Marke: im PDF einen Eintrag in die .aux-Datei, aus
# dem nach dem Satz die Seitenzahl kommt, im E-Book einen Anker, auf den das
# Register verweist. Die Quellen bleiben unberührt, wie bei den
# Anführungszeichen.
#
# Findet der Lauf eine Wortform oder eine Erklärungsstelle nicht, warnt er.
# Das ist der Zweck der wörtlichen Wortfolge: Wer den erklärenden Satz
# umschreibt, erfährt es beim nächsten Satz und nicht erst vom Leser, der
# auf der genannten Seite nichts findet. Ebenso warnt er, wenn im Fließtext
# eine gebeugte Form eines Stichworts steht, die die Liste nicht führt, und
# ihretwegen ein Kapitel fehlt oder die erste Nennung zu spät steht. Sonst
# bliebe das Übersehen einer Beugung ohne Folge, denn die genaue Suche
# findet nur, was in der Liste steht.


@dataclass
class Stichwort:
    anzeige: str
    sortierung: str
    formen: list[str]
    erklaerung: str
    # Wortformen, die aussehen wie eine Beugung des Stichworts und etwas
    # anderes meinen; die Beugungsprüfung übergeht sie.
    ausnahmen: list[str] = field(default_factory=list)


@dataclass
class Marke:
    """Eine Fundstelle: wo im Kapiteltext, und ob es die Erklärung ist."""

    kennung: str
    kapitel: int
    stelle: int
    erklaerung: bool


@dataclass
class Registereintrag:
    stichwort: Stichwort
    marken: list[Marke]


@functools.cache
def lies_register() -> tuple[dict[str, str], dict[int, tuple[Stichwort, ...]]]:
    """Liest satz/register.toml: den Hinweis über dem Register und die Listen.

    Fehlt die Datei, bekommt kein Band ein Register, und der Lauf sagt es.
    Auch ein Fehler in der Datei bricht den Satz nicht ab: Ist sie kein
    gültiges TOML, erscheinen die Bände ohne Register; ist ein einzelner
    Eintrag falsch, entfällt er. In beiden Fällen warnt der Lauf.
    """
    if not REGISTER.is_file():
        hinweis(f"Hinweis: {REGISTER.name} fehlt, die Bände bleiben ohne Register.")
        return {}, {}
    try:
        daten = tomllib.loads(REGISTER.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as fehler:
        warne(f"{REGISTER.name} ist kein gültiges TOML ({fehler}); die Bände bleiben ohne Register.")
        return {}, {}

    vorbemerkung = {}
    for art in ("pdf", "ebook"):
        text = daten.get("hinweis", {}).get(art, "")
        vorbemerkung[art] = text.strip() if isinstance(text, str) else ""

    listen: dict[int, tuple[Stichwort, ...]] = {}
    erlaubt = {"stichwort", "sortierung", "formen", "erklaerung", "ausnahmen"}
    for band in BAENDE:
        eintraege = []
        for nummer, roh in enumerate(daten.get(f"band{band}", []), start=1):
            ort = f"{REGISTER.name}, [[band{band}]] Nr. {nummer}"
            anzeige = roh.get("stichwort") if isinstance(roh, dict) else None
            if not isinstance(anzeige, str) or not anzeige.strip():
                warne(f"{ort}: ohne stichwort, entfällt.")
                continue
            fremd = sorted(set(roh) - erlaubt)
            if fremd:
                warne(f"{ort} („{anzeige}“): unbekannte Angabe {', '.join(fremd)}.")
            formen = roh.get("formen", [anzeige])
            if isinstance(formen, str):
                formen = [formen]
            if not isinstance(formen, list) or not all(isinstance(f, str) and f.strip() for f in formen):
                warne(f"{ort} („{anzeige}“): formen muss eine Liste von Wortfolgen sein, entfällt.")
                continue
            ausnahmen = roh.get("ausnahmen", [])
            if isinstance(ausnahmen, str):
                ausnahmen = [ausnahmen]
            if not isinstance(ausnahmen, list) or not all(isinstance(a, str) and a.strip() for a in ausnahmen):
                warne(f"{ort} („{anzeige}“): ausnahmen muss eine Liste von Wortfolgen sein, entfällt.")
                continue
            sortierung = roh.get("sortierung", "")
            erklaerung = roh.get("erklaerung", "")
            if not isinstance(sortierung, str) or not isinstance(erklaerung, str):
                warne(f"{ort} („{anzeige}“): sortierung und erklaerung müssen Text sein, entfällt.")
                continue
            eintraege.append(Stichwort(
                anzeige=anzeige.strip(),
                sortierung=sortierung.strip() or anzeige.strip(),
                formen=[f.strip() for f in formen],
                erklaerung=" ".join(erklaerung.split()),
                ausnahmen=[" ".join(a.split()) for a in ausnahmen],
            ))
        listen[band] = tuple(eintraege)
    return vorbemerkung, listen


def suchtext(text: str) -> str:
    """Der Kapiteltext, so wie das Register ihn durchsucht.

    Was nicht Fließtext ist, wird durch Leerzeichen gleicher Länge ersetzt:
    Überschriften, Code, Kommentare und die Adressen hinter Verweisen. So
    bleibt jede Stelle, die die Suche findet, dieselbe Stelle im Original.
    """
    def leer(treffer: re.Match) -> str:
        return re.sub(r"[^\n]", " ", treffer.group())

    text = re.sub(r"<!--.*?-->", leer, text, flags=re.S)
    text = re.sub(r"^#{1,6}\s.*$", leer, text, flags=re.M)
    text = re.sub(r"`[^`\n]*`", leer, text)
    return re.sub(r"\]\([^)\n]*\)", leer, text)


@functools.cache
def suchmuster(wortfolge: str) -> re.Pattern:
    """Das Suchmuster für eine Wortform oder eine Erklärungsstelle.

    Gesucht wird genau, mit Groß- und Kleinschreibung und an Wortgrenzen:
    „Engpass“ findet „Engpass-Argument“, nicht aber „Engpasses“. Zwischen
    zwei Wörtern darf ein Zeilenumbruch stehen, und wo ein Wort an ein
    anderes oder an ein Satzzeichen stößt, darf eine Auszeichnung anfangen
    oder enden („*weiche* Budgetbeschränkung“, „der *Asset Lock*, mit“).
    """
    auszeichnung = r"[*_]*"

    def wort(teil: str) -> str:
        return auszeichnung.join(re.escape(stueck) for stueck in re.findall(r"\w+|\W+", teil))

    woerter = [wort(teil) for teil in wortfolge.split()]
    zwischen = auszeichnung + r"\s+" + auszeichnung
    return re.compile(r"(?<!\w)" + zwischen.join(woerter) + r"(?!\w)")


# Die Endungen, um die eine gebeugte Form von der geführten abweichen darf,
# und die Umlaute, die eine Beugung in den Stamm bringt („Treuhand“,
# „Treuhänden“).
BEUGUNGSENDUNGEN = ("e", "en", "er", "ern", "es", "em", "n", "ns", "r", "m", "s")
UMLAUTE = {"a": "ä", "o": "ö", "u": "ü", "A": "Ä", "O": "Ö", "U": "Ü"}


def umgelautet(wort: str) -> str | None:
    """Das Wort mit umgelautetem letzten Vokal, wenn er ein a, o, u oder au ist."""
    for i in range(len(wort) - 1, -1, -1):
        zeichen = wort[i]
        if zeichen.lower() not in "aeiouäöü":
            continue
        if zeichen not in UMLAUTE:
            return None
        if zeichen in "uU" and i > 0 and wort[i - 1] in "aA":
            return wort[: i - 1] + UMLAUTE[wort[i - 1]] + wort[i:]
        return wort[:i] + UMLAUTE[zeichen] + wort[i + 1 :]
    return None


@functools.cache
def beugungsmuster(wortfolge: str) -> re.Pattern:
    """Das Suchmuster für gebeugte Formen einer Wortfolge.

    Jedes Wort darf um eine der üblichen Endungen länger sein und seinen
    letzten Vokal umlauten; das erste Wort darf am Satzanfang groß stehen,
    und das erste Wort einer Wortgruppe klein, wenn es in der Liste nur am
    Satzanfang groß steht („Harte Budgetbeschränkungen“). Das Muster
    findet mehr als das Deutsche kennt, aber gesucht wird damit nur in
    Texten, in denen die genaue Suche schon versagt hat.
    """
    auszeichnung = r"[*_]*"
    teile = wortfolge.split()

    def anfang(stueck: str, gross: bool, klein: bool) -> str:
        zeichen = {stueck[0]}
        if gross:
            zeichen.add(stueck[0].upper())
        if klein:
            zeichen.add(stueck[0].lower())
        if len(zeichen) == 1:
            return re.escape(stueck)
        return "[" + "".join(sorted(zeichen)) + "]" + re.escape(stueck[1:])

    woerter = []
    for nummer, teil in enumerate(teile):
        stuecke = re.findall(r"\w+|\W+", teil)
        mit_buchstaben = [i for i, s in enumerate(stuecke) if re.match(r"\w", s)]
        if not mit_buchstaben:
            woerter.append(re.escape(teil))
            continue
        muster = []
        for i, stueck in enumerate(stuecke):
            erstes = nummer == 0 and i == 0
            gross = erstes and stueck[0].islower()
            klein = erstes and stueck[0].isupper() and len(teile) > 1
            if i == mit_buchstaben[-1]:
                staemme = [stueck] + [u for u in (umgelautet(stueck),) if u]
                alternativen = "|".join(anfang(s, gross, klein) for s in staemme)
                muster.append(f"(?:{alternativen})(?:{'|'.join(BEUGUNGSENDUNGEN)})?")
            else:
                muster.append(anfang(stueck, gross, klein) if i == 0 else re.escape(stueck))
        woerter.append(auszeichnung.join(muster))
    zwischen = auszeichnung + r"\s+" + auszeichnung
    return re.compile(r"(?<!\w)" + zwischen.join(woerter) + r"(?!\w)")


def ohne_auszeichnung(text: str) -> str:
    return " ".join(re.sub(r"[*_]", "", text).split())


def baue_register(band: Band) -> None:
    """Sucht die Stichwörter eines Bandes und legt ihre Marken fest."""
    _, listen = lies_register()
    stichwoerter = listen.get(band.nummer, ())
    if not stichwoerter:
        return
    texte = {kapitel.nummer: suchtext(kapitel.text) for kapitel in band.kapitel}
    ungenutzt: list[str] = []
    ungefuehrt: list[str] = []
    for index, wort in enumerate(stichwoerter, start=1):
        marken: list[Marke] = []
        gefunden: set[str] = set()
        bekannt = {ohne_auszeichnung(f) for f in wort.formen + wort.ausnahmen}
        erklaert: tuple[int, int] | None = None
        if wort.erklaerung:
            orte = [
                (kapitel.nummer, treffer.start())
                for kapitel in band.kapitel
                for treffer in suchmuster(wort.erklaerung).finditer(texte[kapitel.nummer])
            ]
            if not orte:
                warne(
                    f"Band {band.nummer}, Register: Die Erklärungsstelle zu „{wort.anzeige}“ "
                    f"(„{wort.erklaerung}“) steht nicht im Fließtext; das Stichwort erscheint "
                    "ohne hervorgehobene Seite."
                )
            else:
                if len(orte) > 1:
                    warne(
                        f"Band {band.nummer}, Register: Die Erklärungsstelle zu „{wort.anzeige}“ "
                        f"(„{wort.erklaerung}“) steht {len(orte)}-mal im Fließtext; genommen ist die "
                        f"erste, im {orte[0][0]}. Kapitel."
                    )
                erklaert = orte[0]
                marken.append(Marke(f"r{band.nummer}-{index}-e", erklaert[0], erklaert[1], True))

        for kapitel in band.kapitel:
            erste = None
            for form in wort.formen:
                treffer = suchmuster(form).search(texte[kapitel.nummer])
                if treffer:
                    gefunden.add(form)
                    if erste is None or treffer.start() < erste:
                        erste = treffer.start()
            if erste is not None:
                marken.append(Marke(f"r{band.nummer}-{index}-{kapitel.nummer}", kapitel.nummer, erste, False))

            # Eine gebeugte Form, die die Liste nicht führt, vor der ersten
            # erfassten Stelle des Kapitels oder in einem Kapitel ohne eine.
            erfasst = [stelle for stelle in (erste,) if stelle is not None]
            if erklaert and erklaert[0] == kapitel.nummer:
                erfasst.append(erklaert[1])
            grenze = min(erfasst) if erfasst else None
            frueher = None
            for form in wort.formen:
                for treffer in beugungsmuster(form).finditer(texte[kapitel.nummer]):
                    if grenze is not None and treffer.start() >= grenze:
                        break
                    if ohne_auszeichnung(treffer.group()) in bekannt:
                        continue
                    if frueher is None or treffer.start() < frueher.start():
                        frueher = treffer
                    break
            if frueher is not None:
                folge = "das Kapitel fehlt im Register" if grenze is None else "vor der ersten erfassten Stelle"
                ungefuehrt.append(
                    f"„{ohne_auszeichnung(frueher.group())}“ im {kapitel.nummer}. Kapitel "
                    f"({wort.anzeige}; {folge})"
                )

        if not marken:
            warne(f"Band {band.nummer}, Register: „{wort.anzeige}“ steht nirgends im Fließtext und entfällt.")
            continue
        ungenutzt += [f"„{form}“ ({wort.anzeige})" for form in wort.formen if form not in gefunden]
        band.register.append(Registereintrag(wort, marken))

    if ungenutzt:
        warne(
            f"Band {band.nummer}, Register: nicht im Fließtext gefunden – "
            + "; ".join(ungenutzt) + "."
        )
    if ungefuehrt:
        warne(
            f"Band {band.nummer}, Register: gebeugte Formen im Fließtext, die die Liste nicht "
            "führt; als Form eintragen oder, wo sie etwas anderes meinen, als Ausnahme – "
            + "; ".join(ungefuehrt) + "."
        )
    hinweis(f"Band {band.nummer}: Register mit {len(band.register)} Stichwörtern.")


# Die Marke im Quelltext: für das PDF ein LaTeX-Befehl, der die Seite in die
# .aux-Datei schreibt, für das E-Book ein leerer Anker. Beide stehen als
# Pandoc-Inline, das auch am Absatzanfang ein Inline bleibt: der LaTeX-Befehl
# als Rohtext mit Formatangabe, der Anker als leere Spanne mit Kennung.
MARKEN = {
    "latex": "`\\regmarke{{{}}}`{{=latex}}",
    "epub": "[]{{#{}}}",
}


def mit_marken(band: Band, kapitel: Kapitel, art: str) -> str:
    """Der Kapiteltext mit den Marken des Registers, art „latex“ oder „epub“.

    Eine Marke steht unmittelbar vor dem Wort, in dem der Treffer liegt.
    Ist das Wort zusammengesetzt („Ehrlichkeits-Ledger“), steht sie vor dem
    ganzen Wort. Beginnt dort eine Auszeichnung, ein Anführungszeichen, eine
    Klammer oder ein Verweis, rückt sie davor, damit Pandoc die Auszeichnung
    weiter als solche erkennt.
    """
    stellen: dict[int, list[str]] = {}
    for eintrag in band.register:
        for marke in eintrag.marken:
            if marke.kapitel == kapitel.nummer:
                stellen.setdefault(marke.stelle, []).append(marke.kennung)
    text = kapitel.text
    for stelle in sorted(stellen, reverse=True):
        anfang = stelle
        if anfang > 0 and text[anfang - 1] == "-":
            while anfang > 0 and (text[anfang - 1] == "-" or text[anfang - 1].isalnum()):
                anfang -= 1
        while anfang > 0 and text[anfang - 1] in "*_„‚([":
            anfang -= 1
        text = text[:anfang] + "".join(MARKEN[art].format(k) for k in stellen[stelle]) + text[anfang:]
    return text


def sortierschluessel(text: str) -> tuple[str, str]:
    """Deutsche Sortierung: ä wie a, ö wie o, ü wie u, ß wie ss.

    Groß- und Kleinschreibung zählen nicht, Bindestriche und Satzzeichen
    auch nicht. Bei Gleichstand entscheidet die Schreibung selbst.
    """
    schluessel = text.lower().replace("ß", "ss")
    schluessel = unicodedata.normalize("NFKD", schluessel)
    schluessel = "".join(z for z in schluessel if not unicodedata.combining(z))
    schluessel = " ".join(re.sub(r"[^0-9a-z]+", " ", schluessel).split())
    return schluessel, text


def registerzeilen(band: Band) -> list[tuple[str, Registereintrag]]:
    """Die Einträge in der Reihenfolge des Registers, jeder mit seinem Anfangsbuchstaben."""
    eintraege = sorted(band.register, key=lambda e: sortierschluessel(e.stichwort.sortierung))
    return [(sortierschluessel(e.stichwort.sortierung)[0][:1], e) for e in eintraege]


def lies_registerseiten(aux: Path) -> dict[str, str]:
    """Die Seiten der Marken, wie der letzte Satz sie in die .aux-Datei schrieb."""
    if not aux.is_file():
        return {}
    text = aux.read_text(encoding="utf-8", errors="replace")
    return dict(re.findall(r"^\\regseite\{([^}]*)\}\{([^}]*)\}", text, re.M))


def register_tex(band: Band, seiten: dict[str, str]) -> str:
    """Der Inhalt des Registers für das PDF, mit den Seiten aus der .aux-Datei.

    Je Stichwort die Seiten aufsteigend, jede nur einmal; die Seite der
    Erklärungsstelle halbfett. Marken ohne Seite – vor dem ersten Satz sind
    es alle – bleiben weg.
    """
    zeilen: list[str] = []
    buchstabe = None
    for anfang, eintrag in registerzeilen(band):
        fundstellen: dict[str, bool] = {}
        for marke in eintrag.marken:
            seite = seiten.get(marke.kennung)
            if seite:
                fundstellen[seite] = fundstellen.get(seite, False) or marke.erklaerung
        if not fundstellen:
            continue
        if buchstabe is not None and anfang != buchstabe:
            zeilen.append(r"\registerbuchstabe")
        buchstabe = anfang
        folge = sorted(fundstellen, key=lambda s: (0, int(s), "") if s.isdigit() else (1, 0, s))
        angaben = ", ".join(
            (r"\registerseitefett" if fundstellen[s] else r"\registerseite") + f"{{{s}}}" for s in folge
        )
        zeilen.append(rf"\registerzeile{{{als_latex(eintrag.stichwort.anzeige)}}}{{{angaben}}}")
    return "\n".join(zeilen) + "\n"


def register_markdown(band: Band) -> str:
    """Das Register des E-Books: je Stichwort die Kapitel, jedes ein Verweis.

    Ein E-Book hat keine Seiten; an ihre Stelle tritt das Kapitel. Jedes
    Kapitel steht einmal, verwiesen wird auf die erste Nennung darin; im
    Kapitel der Erklärungsstelle auf diese, halbfett. Pandoc löst die
    Verweise auf die Dateien der Kapitel auf.

    Ausgezeichnet ist der Abschnitt als appendix, was ihn in den Anhang des
    Buches stellt. Die Angabe index gehört zu einem eigenen Inhaltsmodell der
    EPUB-Register, mit ausgezeichneten Listen für Begriffe und Fundstellen,
    das diese schlichte Form nicht erfüllt.
    """
    vorbemerkung, _ = lies_register()
    zeilen = ["# Register {#register .register epub:type=appendix}", ""]
    if vorbemerkung.get("ebook"):
        zeilen += ["::: registerhinweis", "", typografie_epub(vorbemerkung["ebook"]), "", ":::", ""]
    buchstabe = None
    for anfang, eintrag in registerzeilen(band):
        ziele: dict[int, tuple[str, bool]] = {}
        for marke in eintrag.marken:
            if marke.erklaerung or marke.kapitel not in ziele:
                ziele[marke.kapitel] = (marke.kennung, marke.erklaerung)
        if anfang != buchstabe:
            if buchstabe is not None:
                zeilen += [":::", ""]
            zeilen += ["::: registergruppe", ""]
            buchstabe = anfang
        verweise = ", ".join(
            f"[**{nummer}**](#{kennung})" if fett else f"[{nummer}](#{kennung})"
            for nummer, (kennung, fett) in sorted(ziele.items())
        )
        stichwort = re.sub(r"([\\*_\[\]<>`#])", r"\\\1", deutsche_anfuehrung(eintrag.stichwort.anzeige))
        zeilen += [f"{stichwort} – Kapitel {verweise}", ""]
    if buchstabe is not None:
        zeilen += [":::", ""]
    return "\n".join(zeilen) + "\n"


# --------------------------------------------------------------------------
# Der Lauf und seine Dateien
# --------------------------------------------------------------------------


@dataclass
class Lauf:
    """Was für alle Erzeugnisse eines Aufrufs gleich ist."""

    fassung: str
    satzdatum: str  # „23.09.2026“, wie es im Impressum steht
    datum_iso: str  # „2026-09-23“, für die Metadaten des E-Books
    jahr: str
    kennung: str  # „3.4“, „entwurf-a1b2c3d“ oder leer
    ziel: Path

    def ausgabe(self) -> str:
        """„Ausgabe 3.4“ – nur für gezählte Ausgaben, nicht für Entwürfe."""
        return f"Ausgabe {self.kennung}" if re.fullmatch(r"\d+\.\d+", self.kennung) else ""


def dateiname(band: int, erzeugnis: str, kennung: str = "") -> str:
    zusatz, endung = ERZEUGNISSE[erzeugnis]
    nummer = f"-{kennung}" if kennung else ""
    return f"{STAMM}-band-{band}{zusatz}{nummer}{endung}"


def arbeitsordner(lauf: Lauf, band: int, art: str) -> Path:
    """Ein Ordner je Band und Erzeugnis für die Zwischenstände.

    Scheitert ein Satz, liegt dort, woran man den Fehler sieht: der
    zusammengesetzte Quelltext, die LaTeX-Datei, das Protokoll.
    """
    ordner = lauf.ziel / "zwischenstand" / f"band-{band}-{art}"
    ordner.mkdir(parents=True, exist_ok=True)
    return ordner


def git(*argumente: str, ersatz: str = "") -> str:
    try:
        ergebnis = subprocess.run(
            ["git", *argumente],
            cwd=WURZEL,
            capture_output=True,
            text=True,
            check=True,
        )
        return ergebnis.stdout.strip() or ersatz
    except (OSError, subprocess.CalledProcessError):
        return ersatz


def pandoc_hauptversion() -> int:
    try:
        ausgabe = subprocess.run(
            ["pandoc", "--version"], capture_output=True, text=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return 0
    treffer = re.search(r"pandoc\S*\s+(\d+)\.", ausgabe)
    return int(treffer.group(1)) if treffer else 0


# Pandoc schreibt LaTeX ohne seine Erweiterung „smart“. Mit ihr übersetzt
# es typografische Zeichen zurück in die alten TeX-Umschreibungen, das
# schließende Anführungszeichen etwa in zwei Gravis (``). Hinter einem
# Frage- oder Ausrufezeichen bildet der erste Gravis mit ihm die TeX-Ligatur
# für ¿ oder ¡, und aus „Ein großer Bluff?“ wurde „Bluff¿‘“; die leere Gruppe,
# die Pandoc dazwischensetzt, trennt unter LuaTeX keine Ligatur. Ohne
# „smart“ bleiben Anführungszeichen, Striche und Auslassungspunkte die
# Zeichen, die in den Quellen stehen, und die Schrift setzt sie selbst.
LATEX = "--to=latex-smart"


def pandoc(*argumente: str, eingabe: str | None = None) -> str:
    lauf = subprocess.run(
        ["pandoc", *argumente],
        input=eingabe,
        capture_output=True,
        text=True,
        cwd=WURZEL,
    )
    if lauf.returncode != 0:
        raise Fehler(f"Pandoc ist gescheitert: {lauf.stderr.strip()}")
    for zeile in lauf.stderr.splitlines():
        if zeile.strip():
            hinweis(f"Pandoc: {zeile.strip()}")
    return lauf.stdout


# --------------------------------------------------------------------------
# Das Impressum
# --------------------------------------------------------------------------
# Es steht in drei Erzeugnissen und ist in allen dreien fast dasselbe: im
# Innenteil für den Druck mit der Zeile zum Druckort und der ISBN des
# Taschenbuchs, in der Leseausgabe ohne beide, im E-Book mit der ISBN des
# E-Books. Eine ISBN bezeichnet genau eine Ausgabe, und eine kostenlose von
# KDP darf nur beim Taschenbuch von KDP stehen; die freie Leseausgabe ist
# eine andere Veröffentlichung. Gebaut wird es als Markdown, damit Pandoc es
# für das PDF in LaTeX und für das E-Book in XHTML setzt.


def impressum(band: Band, angaben: Angaben, lauf: Lauf, art: str) -> str:
    """Das Impressum eines Bandes; art ist „lesen“, „druck“ oder „ebook“."""
    autor = band.titelei["autor"]
    absaetze: list[str] = []
    if autor:
        absaetze.append(f"© {lauf.jahr} {autor}")
    absaetze.append(
        f"Dieses Werk steht unter der Lizenz {angaben.lizenz}: "
        f"[{ohne_schema(angaben.lizenz_url)}]({angaben.lizenz_url})."
    )

    bezeichnung = "Selbstverlag" if angaben.selbstverlag else "Verlag"
    zeilen = [f"{bezeichnung}: {angaben.verlag}" + (f", {angaben.anschrift}" if angaben.anschrift else "")]
    if art == "druck" and angaben.druck:
        zeilen.append(f"Druck: {angaben.druck}")
    ausgabe = {"druck": "taschenbuch", "ebook": "ebook"}.get(art)
    isbn = angaben.isbn_fuer(band.nummer, ausgabe) if ausgabe else ""
    if isbn:
        zeilen.append(f"ISBN {isbn}")
    # Pandocs harter Zeilenumbruch: ein Rückstrich am Zeilenende.
    absaetze.append("\\\n".join(zeilen))

    if angaben.dnb_hinweis:
        absaetze.append(
            "Bibliografische Information der Deutschen Nationalbibliothek: Die "
            "Deutsche Nationalbibliothek verzeichnet diese Publikation in der "
            "Deutschen Nationalbibliografie; detaillierte bibliografische Daten "
            "sind im Internet über dnb.dnb.de abrufbar."
        )

    quelle = f"`{band.verzeichnis.relative_to(WURZEL).as_posix()}/`"
    verzeichnis = f"[{ohne_schema(angaben.verzeichnis)}]({angaben.verzeichnis})"
    herkunft = "Erzeugt" if art == "ebook" else "Gesetzt"
    satz = f"{herkunft} aus den Kapiteldateien in {quelle} des offenen Verzeichnisses {verzeichnis}"
    if lauf.fassung:
        satz += f", Quellstand `{lauf.fassung}`"
        if lauf.satzdatum:
            satz += f" vom {lauf.satzdatum}"
    satz += "."
    if lauf.ausgabe():
        satz = f"{lauf.ausgabe()}. {satz}"
    absaetze.append(satz)
    # Der Zeilenumbruch am Ende ist nicht Kosmetik: Ohne ihn liest Pandoc
    # ein Metadatum als eine einzige Zeile und macht aus den Absätzen
    # Zeilenumbrüche.
    return "\n\n".join(absaetze) + "\n"


# --------------------------------------------------------------------------
# PDF: Leseausgabe und Innenteil
# --------------------------------------------------------------------------


def baue_quelltext(band: Band, angaben: Angaben, lauf: Lauf, art: str, bund_mm: float) -> str:
    """Setzt den Markdown-Quelltext zusammen, aus dem Pandoc die LaTeX-Datei macht.

    art ist „lesen“ oder „druck“. Beide bekommen denselben Text und denselben
    Satzspiegel; was sie unterscheidet, schaltet die Vorlage über die
    Variable druck.
    """
    titelei = band.titelei
    kopf = {
        "titel": deutsche_anfuehrung(titelei["titel"]),
        "untertitel": deutsche_anfuehrung(titelei["untertitel"]),
        "band": deutsche_anfuehrung(titelei["band"]),
        "autor": titelei["autor"],
        "stand": titelei["stand"],
        "impressum": impressum(band, angaben, lauf, art),
        "papierbreite": f"{angaben.breite}in",
        "papierhoehe": f"{angaben.hoehe}in",
        "bund": f"{bund_mm:.1f}mm",
        "lang": "de",
    }
    zeilen: list[str] = ["---"]
    # JSON-Zeichenketten sind gültiges YAML und maskieren alles, was in
    # einem Titel stehen kann.
    zeilen += [f"{feld}: {json.dumps(wert, ensure_ascii=False)}" for feld, wert in kopf.items()]
    if art == "druck":
        zeilen.append("druck: true")
    zeilen += ["---", ""]

    for titel, rumpf in band.vorspann:
        zeilen.append(f"\\vorspann{{{als_latex(titel)}}}")
        zeilen.append("")
        zeilen.append(typografie(rumpf))
        zeilen.append("")

    zeilen.append("\\hauptteil")
    zeilen.append("")

    offener_teil = None
    for kapitel in band.kapitel:
        teiltitel = band.teil_von(kapitel.nummer)
        if teiltitel is not None and teiltitel != offener_teil:
            offener_teil = teiltitel
            zeilen.append(f"\\teil{{{als_latex(teiltitel)}}}")
            zeilen.append("")

        zeilen.append(
            f"\\kapitel{{{als_latex(kapitelbezeichnung(kapitel.nummer))}}}"
            f"{{{als_latex(kapitel.titel)}}}"
        )
        zeilen.append("")
        zeilen.append(typografie(setze_ueberschriften(mit_marken(band, kapitel, "latex"))).strip())
        zeilen.append("")
        if kapitel.belege:
            zeilen.append("\\belegeanfang")
            zeilen.append("")
            zeilen.append(typografie(setze_ueberschriften(kapitel.belege)).strip())
            zeilen.append("")
            zeilen.append("\\belegeende")
            zeilen.append("")

    # Das Register nach dem letzten Kapitel. Seine Zeilen liest die Vorlage
    # aus buch.reg, die setze_pdf nach jedem Satz aus den Seiten der Marken
    # schreibt; hier steht nur der Kopf.
    if band.register:
        vorbemerkung, _ = lies_register()
        zeilen.append(f"\\registerteil{{Register}}{{{als_latex(vorbemerkung.get('pdf', ''))}}}")
        zeilen.append("")

    return "\n".join(zeilen) + "\n"


def tex_umgebung(epoche: str) -> dict[str, str]:
    """Die Umgebung für LuaLaTeX.

    Das Protokoll bekommt lange Zeilen, damit „Output written on …“ nie
    umbricht. Und mit dem Zeitpunkt des Quellstands als SOURCE_DATE_EPOCH
    trägt ein späterer Satz derselben Fassung dasselbe Datum in der Datei.
    """
    umgebung = dict(os.environ, max_print_line="100000")
    if epoche:
        umgebung.update(SOURCE_DATE_EPOCH=epoche, FORCE_SOURCE_DATE="1")
    return umgebung


def setze_tex(tex: Path, epoche: str, laeufe: int = 5, nach_lauf=None) -> int:
    """Setzt eine LaTeX-Datei, bis Inhaltsverzeichnis und Verweise stehen.

    Der erste Lauf schreibt das Verzeichnis, der zweite setzt es ein – und
    weil es im Vorspann Platz nimmt, rücken die Seitenzahlen dahinter, was
    einen dritten Lauf verlangen kann. Gibt die Seitenzahl zurück.

    nach_lauf wird nach jedem Lauf gerufen und sagt, ob es eine Datei
    geändert hat, die der nächste Lauf einliest; dann folgt noch einer. So
    kommt das Register herein: Die Seiten seiner Marken stehen nach dem
    ersten Lauf fest, denn der Hauptteil zählt ab eins und hängt weder am
    Inhaltsverzeichnis noch am Register, das hinter ihm steht.
    """
    verzeichnis = tex.parent
    toc = tex.with_suffix(".toc")
    protokoll = tex.with_suffix(".log")
    vorher: bytes | None = None
    for nummer in range(1, laeufe + 1):
        lauf = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", tex.name],
            cwd=verzeichnis,
            capture_output=True,
            text=True,
            env=tex_umgebung(epoche),
        )
        text = protokoll.read_text(encoding="utf-8", errors="replace") if protokoll.exists() else ""
        if lauf.returncode != 0:
            fehlerzeilen = [z for z in text.splitlines() if z.startswith("!") or ":" in z and ".tex:" in z]
            auszug = "\n".join(fehlerzeilen[-12:]) or "\n".join(text.splitlines()[-30:])
            raise Fehler(
                f"LuaLaTeX ist an {tex} gescheitert (Lauf {nummer}).\n{auszug}\n"
                f"Das vollständige Protokoll liegt in {protokoll}."
            )
        jetzt = toc.read_bytes() if toc.exists() else b""
        # Eine Aufforderung zum nächsten Lauf, von LaTeX, hyperref oder
        # rerunfilecheck. Nicht mitzählen darf die Zeile, mit der sich
        # rerunfilecheck beim Laden vorstellt („… Rerun checks for auxiliary
        # files“) – sie steht in jedem Protokoll, und solange sie zählte,
        # lief die Schleife immer bis zum letzten Lauf.
        nochmal = bool(re.search(r"(?im)^(?!package: ).*\brerun\b", text))
        if nach_lauf is not None and nach_lauf():
            nochmal = True
        if nummer > 1 and jetzt == vorher and not nochmal:
            break
        vorher = jetzt
    else:
        if laeufe > 1:
            warne(f"{tex.name}: Nach {laeufe} Läufen stehen Inhaltsverzeichnis und Register noch nicht fest.")
    seiten = re.search(r"Output written on .*?\((\d+) pages?", text, re.S)
    if not seiten:
        raise Fehler(f"LuaLaTeX hat in {tex.name} keine Seite geschrieben.")
    return int(seiten.group(1))


def kdp_bund_zoll(seiten: int) -> float:
    for grenze, bund in KDP_BUND:
        if seiten <= grenze:
            return bund
    raise Fehler(
        f"{seiten} Seiten – KDP druckt Taschenbücher bis {KDP_SEITEN[1]} Seiten."
    )


def mediaboxen(pdf: Path) -> set[tuple[float, float]]:
    """Breite und Höhe aller MediaBoxen in Punkt, soweit im Klartext lesbar."""
    daten = pdf.read_bytes()
    boxen = set()
    for x0, y0, x1, y1 in re.findall(
        rb"/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]", daten
    ):
        boxen.add((round(float(x1) - float(x0), 2), round(float(y1) - float(y0), 2)))
    return boxen


def pruefe_masse(pdf: Path, breite_zoll: float, hoehe_zoll: float, was: str) -> None:
    boxen = mediaboxen(pdf)
    soll = (breite_zoll * 72, hoehe_zoll * 72)
    if not boxen:
        raise Fehler(f"{pdf.name}: keine MediaBox lesbar, das Maß von {was} ist ungeprüft.")
    for breite, hoehe in boxen:
        if abs(breite - soll[0]) > 0.05 or abs(hoehe - soll[1]) > 0.05:
            raise Fehler(
                f"{pdf.name}: {was} misst {breite / 72:.4f} × {hoehe / 72:.4f} Zoll, "
                f"KDP erwartet {soll[0] / 72:.4f} × {soll[1] / 72:.4f} Zoll."
            )


def pruefe_innenteil(pdf: Path, angaben: Angaben, seiten: int, bund_mm: float) -> None:
    """Prüft den Innenteil gegen die Vorgaben von KDP, soweit die Datei es zeigt."""
    pruefe_masse(pdf, angaben.breite, angaben.hoehe, "die Seite")
    daten = pdf.read_bytes()
    # KDP nimmt keine Lesezeichen, Anmerkungen oder Verweisflächen an.
    for merkmal, name in ((b"/Annots", "Anmerkungen oder Verweise"), (b"/Outlines", "Lesezeichen")):
        if merkmal in daten:
            raise Fehler(f"{pdf.name} enthält {name}; KDP lehnt das ab.")
    if not KDP_SEITEN[0] <= seiten <= KDP_SEITEN[1]:
        raise Fehler(f"{pdf.name}: {seiten} Seiten, KDP druckt {KDP_SEITEN[0]} bis {KDP_SEITEN[1]}.")
    if seiten % 2:
        warne(f"{pdf.name} hat eine ungerade Seitenzahl ({seiten}); KDP füllt auf.")
    noetig = kdp_bund_zoll(seiten) * MM_JE_ZOLL
    if bund_mm + 1e-6 < noetig:
        raise Fehler(f"{pdf.name}: Bund {bund_mm:.1f} mm, KDP verlangt bei {seiten} Seiten {noetig:.1f} mm.")


def setze_pdf(band: Band, angaben: Angaben, lauf: Lauf, art: str, bund_mm: float) -> tuple[Path, int]:
    """Setzt Leseausgabe (art „lesen“) oder Innenteil (art „druck“) eines Bandes."""
    ordner = arbeitsordner(lauf, band.nummer, art)
    quelle = ordner / "buch.md"
    quelle.write_text(baue_quelltext(band, angaben, lauf, art, bund_mm), encoding="utf-8")
    tex = ordner / "buch.tex"
    pandoc(
        str(quelle),
        "--from=markdown+raw_tex-auto_identifiers",
        LATEX,
        "--template", str(VORLAGE),
        "--top-level-division=chapter",
        f"--resource-path={band.verzeichnis}",
        f"--variable=schriftverzeichnis={SCHRIFTEN}/",
        "--output", str(tex),
    )

    # Das Register liest die Vorlage aus buch.reg. Nach jedem Lauf wird die
    # Datei aus den Seiten neu geschrieben, die der Lauf in buch.aux
    # hinterlassen hat; ändert sie sich, folgt ein weiterer Lauf.
    aux = tex.with_suffix(".aux")
    reg = tex.with_suffix(".reg")
    reg.unlink(missing_ok=True)

    def register_nachziehen() -> bool:
        if not band.register:
            return False
        neu = register_tex(band, lies_registerseiten(aux))
        if reg.exists() and reg.read_text(encoding="utf-8") == neu:
            return False
        reg.write_text(neu, encoding="utf-8")
        return True

    seiten = setze_tex(tex, epoche=git("log", "-1", "--format=%ct"), nach_lauf=register_nachziehen)
    if band.register:
        gesetzt = lies_registerseiten(aux)
        ohne_seite = [m.kennung for e in band.register for m in e.marken if m.kennung not in gesetzt]
        if ohne_seite:
            warne(
                f"Band {band.nummer}, Register: {len(ohne_seite)} Marken haben im Satz keine Seite "
                f"bekommen ({', '.join(ohne_seite[:5])}{' …' if len(ohne_seite) > 5 else ''})."
            )
    erzeugnis = "lesen" if art == "lesen" else "innenteil"
    ziel = lauf.ziel / dateiname(band.nummer, erzeugnis, lauf.kennung)
    shutil.copyfile(tex.with_suffix(".pdf"), ziel)
    return ziel, seiten


def setze_mit_bund(band: Band, angaben: Angaben, lauf: Lauf, art: str, bund_mm: float) -> tuple[Path, int, float]:
    """Setzt ein PDF und wiederholt den Satz, wenn der Bund zu schmal wird.

    Welchen Bund KDP verlangt, hängt von der Seitenzahl ab, und die kennt
    erst der fertige Satz. Die Vorlage hält mehr, als KDP bis 700 Seiten
    fordert; erst ein dickerer Band löst einen zweiten Satz aus, und der
    kann wiederum Seiten hinzufügen – deshalb die Schleife.
    """
    for _ in range(4):
        ziel, seiten = setze_pdf(band, angaben, lauf, art, bund_mm)
        noetig = kdp_bund_zoll(seiten) * MM_JE_ZOLL
        if noetig <= bund_mm + 1e-6:
            return ziel, seiten, bund_mm
        hinweis(
            f"Band {band.nummer}: {seiten} Seiten verlangen bei KDP {noetig:.1f} mm Bund, "
            f"gesetzt waren {bund_mm:.1f} mm – neuer Satz."
        )
        bund_mm = math.ceil(noetig * 10) / 10
    raise Fehler(f"Band {band.nummer}: Der Bund kommt nicht zur Ruhe.")


# --------------------------------------------------------------------------
# Umschlag und Titelbild
# --------------------------------------------------------------------------


def lies_umschlagtext(band: int) -> str:
    pfad = UMSCHLAGTEXTE / f"band{band}.md"
    if not pfad.is_file():
        raise Fehler(f"{pfad} fehlt – ohne Umschlagtext keine Rückseite.")
    text = re.sub(r"<!--.*?-->", "", pfad.read_text(encoding="utf-8"), flags=re.S)
    return deutsche_anfuehrung(text.strip())


def bandzeile_teilen(zeile: str) -> tuple[str, str]:
    """„Erster Band: Das Argument“ wird zu („Erster Band“, „Das Argument“)."""
    vorn, _, hinten = zeile.partition(":")
    return (vorn.strip(), hinten.strip()) if hinten else (zeile.strip(), "")


def titelzeilen(titel: str) -> str:
    """Bricht den Titel für die Vorderseite vor dem letzten Wort um."""
    woerter = titel.split()
    if len(woerter) < 3:
        return als_latex(titel)
    return als_latex(" ".join(woerter[:-1])) + r"\\" + als_latex(woerter[-1])


def rueckenbreite(angaben: Angaben, seiten: int) -> float:
    return seiten * KDP_PAPIER[angaben.papier]


def rueckenschrift(ruecken: float, seiten: int) -> float:
    """Die Schriftgröße auf dem Rücken, oder null, wo kein Text hingehört.

    Zu beiden Falzen bleiben 0,0625 Zoll frei und dazu ein kleiner Rand für
    Ober- und Unterlängen; was dann übrig bleibt, trägt die Zeile. Unter
    sechs Punkt wird der Rücken lieber leer gelassen.
    """
    if seiten < KDP_RUECKENTEXT_AB:
        return 0.0
    verfuegbar = (ruecken - 2 * KDP_FALZLUFT) * 72 * 0.8
    groesse = min(RUECKEN_PT, verfuegbar)
    return round(groesse, 1) if groesse >= 6 else 0.0


def setze_umschlagbogen(band: Band, angaben: Angaben, lauf: Lauf, art: str, seiten: int = 0) -> tuple[Path, dict]:
    """Setzt den Umschlag (art „druck“) oder das Titelbild (art „ebook“) als PDF."""
    druck = art == "druck"
    titelei = band.titelei
    bandzahl, bandtitel = bandzeile_teilen(titelei["band"])
    breite = angaben.breite
    if druck:
        beschnitt = KDP_BESCHNITT
        hoehe = angaben.hoehe
        ruecken = rueckenbreite(angaben, seiten)
        bogenbreite = 2 * beschnitt + 2 * breite + ruecken
        bogenhoehe = 2 * beschnitt + hoehe
        vorderseite_links = breite + ruecken
    else:
        # Das Titelbild hat das Seitenverhältnis, das KDP empfiehlt.
        beschnitt = 0.0
        hoehe = breite * TITELBILD_PIXEL[1] / TITELBILD_PIXEL[0]
        ruecken = 0.0
        bogenbreite, bogenhoehe = breite, hoehe
        vorderseite_links = 0.0
    schrift = rueckenschrift(ruecken, seiten) if druck else 0.0

    # Die Werkangabe der Rückseite nennt beide Bände, den eigenen fett.
    reihe = []
    for nummer in BAENDE:
        zeile = lies_titelei((bandverzeichnis(nummer) / INHALT).read_text(encoding="utf-8"))["band"]
        zeile = als_latex(zeile)
        reihe.append(rf"\textbf{{{zeile}}}" if nummer == band.nummer else zeile)
    klappentext = pandoc("--from=markdown", LATEX, eingabe=lies_umschlagtext(band.nummer)) if druck else ""
    nachweis = (
        rf"© {lauf.jahr} {als_latex(titelei['autor'])} · {als_latex(angaben.lizenz_kurz)}\\"
        rf"Offenes Manuskript:\\{als_latex(ohne_schema(angaben.verzeichnis))}"
    )

    werte = {
        "UBand": str(band.nummer),
        "UDruck": "1" if druck else "0",
        "UFarbmodell": "cmyk" if druck else "rgb",
        "USchriften": f"{SCHRIFTEN}/",
        "UBeschnitt": f"{beschnitt:.6f}",
        "UBreite": f"{breite:.6f}",
        "UHoehe": f"{hoehe:.6f}",
        "URuecken": f"{ruecken:.6f}",
        "UVorderseiteLinks": f"{vorderseite_links:.6f}",
        "UBogenbreite": f"{bogenbreite:.6f}",
        "UBogenhoehe": f"{bogenhoehe:.6f}",
        "URueckentext": "1" if schrift else "0",
        "URueckengroesse": f"{schrift or RUECKEN_PT}",
        "UTitel": als_latex(titelei["titel"]),
        "UTitelzeilen": titelzeilen(titelei["titel"]),
        "UUntertitel": als_latex(titelei["untertitel"]),
        "UBandzahl": als_latex(bandzahl),
        "UBandtitel": als_latex(bandtitel),
        "URueckenband": f"Band {band.nummer}",
        "UAutor": als_latex(titelei["autor"]),
        "UReihe": r"\\".join(reihe),
        "UNachweis": nachweis,
    }
    kopf = [f"\\def\\{name}{{{wert}}}" for name, wert in werte.items()]
    kopf.append(f"\\long\\def\\UKlappentext{{{klappentext.strip()}}}")

    ordner = arbeitsordner(lauf, band.nummer, "umschlag" if druck else "titelbild")
    tex = ordner / ("umschlag.tex" if druck else "titelbild.tex")
    tex.write_text(
        "% Erzeugt von satz/build.py – geändert wird in satz/umschlag.tex.\n"
        + "\n".join(kopf) + "\n\n" + UMSCHLAG.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    setze_tex(tex, epoche=git("log", "-1", "--format=%ct"), laeufe=1)
    protokoll = tex.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
    for ueberhang in re.findall(r"UMSCHLAG-UEBERLAUF: ([\d.]+)", protokoll):
        millimeter = float(ueberhang) / 72.27 * MM_JE_ZOLL
        warne(
            f"Band {band.nummer}: Der Umschlagtext in satz/umschlag/band{band.nummer}.md ist um "
            f"{millimeter:.1f} mm zu lang für die Rückseite und läuft in die Werkangabe."
        )
    pdf = tex.with_suffix(".pdf")
    pruefe_masse(pdf, bogenbreite, bogenhoehe, "der Umschlagbogen" if druck else "das Titelbild")
    masse = {
        "ruecken_zoll": round(ruecken, 4),
        "ruecken_mm": round(ruecken * MM_JE_ZOLL, 1),
        "bogen_zoll": [round(bogenbreite, 4), round(bogenhoehe, 4)],
        "rueckentext": bool(schrift),
    }
    if druck and not schrift:
        hinweis(f"Band {band.nummer}: Der Rücken ist zu schmal für Text und bleibt leer.")
    return pdf, masse


def jfif_dichte(jpg: Path, dpi: int = 300) -> None:
    """Trägt die Auflösung in den JFIF-Kopf ein.

    Die Pixelzahl bestimmt die Qualität, nicht diese Angabe; KDP liest sie
    beim Hochladen aber mit und erwartet für Titelbilder 300 dpi.
    """
    daten = bytearray(jpg.read_bytes())
    if daten[2:4] == b"\xff\xe0" and daten[6:11] == b"JFIF\x00":
        daten[13] = 1  # Einheit: Punkte je Zoll
        daten[14:16] = dpi.to_bytes(2, "big")
        daten[16:18] = dpi.to_bytes(2, "big")
        jpg.write_bytes(bytes(daten))


def jpeg_masse(jpg: Path) -> tuple[int, int]:
    daten = jpg.read_bytes()
    i = 2
    while i + 9 < len(daten):
        if daten[i] != 0xFF:
            i += 1
            continue
        marke = daten[i + 1]
        if marke in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(daten[i + 7 : i + 9], "big"), int.from_bytes(daten[i + 5 : i + 7], "big")
        i += 2 + int.from_bytes(daten[i + 2 : i + 4], "big")
    return 0, 0


def rastere(pdf: Path, jpg: Path) -> bool:
    """Macht aus dem Titelbild-PDF ein JPEG in 1600 × 2560 Pixeln.

    Bevorzugt mit pdftoppm aus Poppler, das auf dem Bauläufer ohnehin für
    die Seitenzählung liegt; sonst mit Ghostscript. Fehlt beides, gibt es
    kein Titelbild, und das E-Book entsteht ohne.
    """
    breite, hoehe = TITELBILD_PIXEL
    if shutil.which("pdftoppm"):
        befehl = ["pdftoppm", "-jpeg", "-jpegopt", "quality=92", "-scale-to-x", str(breite),
                  "-scale-to-y", str(hoehe), "-singlefile", str(pdf), str(jpg.with_suffix(""))]
    elif shutil.which("gs"):
        befehl = ["gs", "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=jpeg", "-dJPEGQ=92",
                  "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4", f"-g{breite}x{hoehe}",
                  "-dPDFFitPage", f"-sOutputFile={jpg}", str(pdf)]
    else:
        return False
    subprocess.run(befehl, check=True, capture_output=True)
    jfif_dichte(jpg)
    if jpeg_masse(jpg) != TITELBILD_PIXEL:
        raise Fehler(f"{jpg.name} misst {jpeg_masse(jpg)} statt {TITELBILD_PIXEL} Pixel.")
    return True


# --------------------------------------------------------------------------
# E-Book
# --------------------------------------------------------------------------


def baue_epub_quelltext(band: Band) -> str:
    """Der Markdown-Quelltext des E-Books.

    Die Gliederung ist dieselbe wie im PDF, nur in Pandocs eigenen Mitteln:
    Vorspann und Teile auf der ersten Ebene, die Kapitel darunter, ihre
    Abschnitte auf der dritten. Jedes Kapitel wird eine eigene Datei im
    EPUB. Die Kapitelmarke („9. Kapitel“) steht als eigene Zeile im Kopf;
    im Inhaltsverzeichnis wird sie mit Gedankenstrich vor den Titel gesetzt,
    wie im PDF – das erledigt die Nachbearbeitung. Am Schluss steht das
    Register, mit Kapiteln statt Seiten.
    """
    zeilen: list[str] = []
    for nummer, (titel, rumpf) in enumerate(band.vorspann, start=1):
        zeilen.append(f"# {deutsche_anfuehrung(titel)} {{#vorspann-{nummer} .vorspann epub:type=preface}}")
        zeilen.append("")
        zeilen.append(typografie_epub(setze_ueberschriften(rumpf, 3)).strip())
        zeilen.append("")

    offener_teil = None
    teilnummer = 0
    for kapitel in band.kapitel:
        teiltitel = band.teil_von(kapitel.nummer)
        if teiltitel is not None and teiltitel != offener_teil:
            offener_teil = teiltitel
            teilnummer += 1
            zeilen.append(f"# {deutsche_anfuehrung(teiltitel)} {{#teil-{teilnummer} .teil epub:type=part}}")
            zeilen.append("")
        zeilen.append(
            f"## [{kapitelbezeichnung(kapitel.nummer)}]{{.kapitelzahl}} "
            f"{deutsche_anfuehrung(kapitel.titel)} "
            f"{{#kapitel-{kapitel.nummer} .kapitel epub:type=chapter}}"
        )
        zeilen.append("")
        zeilen.append(typografie_epub(setze_ueberschriften(mit_marken(band, kapitel, "epub"), 3)).strip())
        zeilen.append("")
        if kapitel.belege:
            zeilen += [
                "::: belege",
                "",
                f"### Belege {{#belege-{kapitel.nummer}}}",
                "",
                typografie_epub(setze_ueberschriften(kapitel.belege, 4)).strip(),
                "",
                ":::",
                "",
            ]
    if band.register:
        zeilen.append(register_markdown(band))
    return "\n".join(zeilen) + "\n"


def epub_metadaten(band: Band, angaben: Angaben, lauf: Lauf) -> dict:
    titelei = band.titelei
    isbn = angaben.isbn_fuer(band.nummer, "ebook")
    if isbn:
        kennung = {"scheme": "ISBN-13", "text": isbn}
    else:
        # Ohne ISBN eine UUID, die aus dem Verzeichnis und der Bandnummer
        # folgt: Jeder Satz desselben Bandes trägt dieselbe Kennung, und
        # ein Lesegerät hält eine neue Ausgabe nicht für ein neues Buch.
        ableitung = uuid.uuid5(uuid.NAMESPACE_URL, f"{angaben.verzeichnis}#band-{band.nummer}")
        kennung = {"scheme": "URN", "text": f"urn:uuid:{ableitung}"}
    # Die Beschreibung ist in EPUB reiner Text. Als Markdown mit Absätzen
    # übergeben, klebte Pandoc die Absätze ohne Leerzeichen aneinander;
    # deshalb ein einziger Absatz ohne Auszeichnung.
    beschreibung = " ".join(
        absatz.replace("\n", " ").strip()
        for absatz in re.sub(r"\*+", "", lies_umschlagtext(band.nummer)).split("\n\n")
        if absatz.strip()
    )
    return {
        "title": deutsche_anfuehrung(titelei["titel"]),
        "author": [titelei["autor"]],
        "lang": "de-DE",
        "date": lauf.datum_iso,
        "publisher": angaben.verlag,
        "rights": f"© {lauf.jahr} {titelei['autor']}, {angaben.lizenz_kurz}",
        "identifier": [kennung],
        "description": beschreibung,
        "belongs-to-collection": deutsche_anfuehrung(titelei["titel"]),
        "group-position": band.nummer,
        "toc-title": "Inhalt",
        # Diese Felder liest allein die Vorlage für die Titelseite.
        "untertitel": deutsche_anfuehrung(titelei["untertitel"]),
        "bandzeile": deutsche_anfuehrung(titelei["band"]),
        "standzeile": titelei["stand"],
        "impressum": impressum(band, angaben, lauf, "ebook"),
    }


def setze_epub(band: Band, angaben: Angaben, lauf: Lauf, titelbild: Path | None) -> Path:
    ordner = arbeitsordner(lauf, band.nummer, "ebook")
    quelle = ordner / "buch.md"
    quelle.write_text(baue_epub_quelltext(band), encoding="utf-8")
    metadaten = ordner / "metadaten.yaml"
    # JSON ist gültiges YAML; so muss nichts von Hand maskiert werden.
    metadaten.write_text(
        json.dumps(epub_metadaten(band, angaben, lauf), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    epub = ordner / "buch.epub"
    teilung = "--split-level=2" if pandoc_hauptversion() >= 3 else "--epub-chapter-level=2"
    argumente = [
        str(quelle),
        "--from=markdown+ascii_identifiers-raw_tex",
        "--to=epub3",
        "--template", str(EPUB_VORLAGE),
        "--css", str(EPUB_STIL),
        "--metadata-file", str(metadaten),
        "--toc",
        "--toc-depth=2",
        teilung,
        "--output", str(epub),
    ]
    if titelbild:
        argumente += ["--epub-cover-image", str(titelbild)]
    epoche = git("log", "-1", "--format=%ct")
    umgebung = dict(os.environ, SOURCE_DATE_EPOCH=epoche) if epoche else None
    lauf_pandoc = subprocess.run(["pandoc", *argumente], capture_output=True, text=True, cwd=WURZEL, env=umgebung)
    if lauf_pandoc.returncode != 0:
        raise Fehler(f"Pandoc ist am E-Book von Band {band.nummer} gescheitert: {lauf_pandoc.stderr.strip()}")
    nachbearbeite_epub(epub)
    ziel = lauf.ziel / dateiname(band.nummer, "ebook", lauf.kennung)
    shutil.copyfile(epub, ziel)
    pruefe_epub(ziel)
    return ziel


def attribute(tag: str) -> dict[str, str]:
    return dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))


def nachbearbeite_epub(pfad: Path) -> None:
    """Bringt Pandocs EPUB in die Form, die KDP verlangt.

    *Titelbildseite:* Pandoc legt zum Titelbild eine eigene XHTML-Seite an.
    Die Kindle-Richtlinien verbieten genau das – eine Titelbildseite
    zusätzlich zum Titelbild lässt es doppelt erscheinen oder die Umwandlung
    scheitern. Die Seite fällt, das Bild bleibt mit der Eigenschaft
    cover-image und zusätzlich mit der älteren Angabe <meta name="cover">.

    *Lesebeginn:* Ein Verweis auf den ersten Vorspannabschnitt, damit das
    Buch dort aufgeht und nicht auf der Titelseite.

    *Kapitelmarken:* Im Inhaltsverzeichnis stehen Marke und Titel mit
    Gedankenstrich hintereinander, wie im PDF („9. Kapitel – Fehlertoleranz“).
    Ausgeblendet wird dafür nichts: Versteckter Text im Inhaltsverzeichnis
    bricht die Umwandlung bei Kindle ab.
    """
    with zipfile.ZipFile(pfad) as archiv:
        eintraege = [(info.filename, archiv.read(info.filename)) for info in archiv.infolist()]
    inhalt = dict(eintraege)

    container = inhalt["META-INF/container.xml"].decode("utf-8")
    opf_name = re.search(r'full-path="([^"]+)"', container).group(1)
    opf_ordner = opf_name.rpartition("/")[0]

    def voll(href: str) -> str:
        return f"{opf_ordner}/{href}" if opf_ordner else href

    opf = inhalt[opf_name].decode("utf-8")
    eintraege_opf = {attribute(tag).get("id"): (tag, attribute(tag)) for tag in re.findall(r"<item\b[^>]*>", opf)}

    entfernt: set[str] = set()
    for ident, (tag, attrs) in eintraege_opf.items():
        href = attrs.get("href", "")
        if href.rpartition("/")[2] != "cover.xhtml":
            continue
        opf = re.sub(rf"\n?[ \t]*{re.escape(tag)}", "", opf, count=1)
        opf = re.sub(rf'\s*<itemref\b[^>]*idref="{re.escape(ident)}"[^>]*/>', "", opf)
        opf = re.sub(rf'\s*<reference\b[^>]*href="{re.escape(href)}"[^>]*/>', "", opf)
        entfernt.add(voll(href))

    bild = next((i for i, (_, a) in eintraege_opf.items() if "cover-image" in a.get("properties", "").split()), None)
    if bild and '<meta name="cover"' not in opf:
        opf = re.sub(r"(\s*)</metadata>", rf'\1  <meta name="cover" content="{bild}" />\1</metadata>', opf, count=1)

    # Wo das Lesen beginnt: die Datei mit dem ersten Vorspannabschnitt.
    beginn = next(
        (name for name, daten in eintraege if name.endswith(".xhtml") and b'id="vorspann-1"' in daten),
        None,
    )
    nav_name = next(
        (voll(a["href"]) for _, a in eintraege_opf.values() if "nav" in a.get("properties", "").split()),
        None,
    )
    ncx_name = next(
        (voll(a["href"]) for _, a in eintraege_opf.values() if a.get("media-type") == "application/x-dtbncx+xml"),
        None,
    )

    if beginn:
        relativ_opf = os.path.relpath(beginn, opf_ordner or ".")
        if "<guide>" in opf and 'type="text"' not in opf:
            opf = opf.replace(
                "<guide>", f'<guide>\n    <reference type="text" title="Beginn" href="{relativ_opf}" />', 1
            )

    if nav_name:
        nav = inhalt[nav_name].decode("utf-8")
        nav = re.sub(r'<span class="kapitelzahl">([^<]*)</span>\s*', r"\1 – ", nav)
        nav = re.sub(r'\s*<li>\s*<a href="[^"]*cover\.xhtml"[^>]*>.*?</a>\s*</li>', "", nav, flags=re.S)
        nav = nav.replace(">Title Page<", ">Titelseite<").replace(">Table of Contents<", ">Inhalt<")
        if beginn and 'epub:type="bodymatter"' not in nav:
            relativ = os.path.relpath(beginn, os.path.dirname(nav_name))
            nav = re.sub(
                r'(<nav epub:type="landmarks".*?<ol>)',
                rf'\1\n    <li>\n      <a href="{relativ}" epub:type="bodymatter">Beginn</a>\n    </li>',
                nav,
                count=1,
                flags=re.S,
            )
        inhalt[nav_name] = nav.encode("utf-8")

    if ncx_name:
        ncx = inhalt[ncx_name].decode("utf-8")
        ncx = re.sub(r"(<text>\d+\. Kapitel) (?=\S)", r"\1 – ", ncx)
        if bild:
            ncx = re.sub(r'<meta name="cover" content="[^"]*"', f'<meta name="cover" content="{bild}"', ncx)
        inhalt[ncx_name] = ncx.encode("utf-8")

    inhalt[opf_name] = opf.encode("utf-8")

    # Neu packen: mimetype zuerst und unkomprimiert, so verlangt es EPUB.
    neu = pfad.with_suffix(".neu")
    with zipfile.ZipFile(neu, "w") as archiv:
        archiv.writestr(zipfile.ZipInfo("mimetype"), inhalt["mimetype"], compress_type=zipfile.ZIP_STORED)
        for name, _ in eintraege:
            if name == "mimetype" or name in entfernt:
                continue
            archiv.writestr(zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0)), inhalt[name],
                            compress_type=zipfile.ZIP_DEFLATED)
    neu.replace(pfad)

    with zipfile.ZipFile(pfad) as archiv:
        namen = archiv.namelist()
        opf_neu = archiv.read(opf_name).decode("utf-8")
    if any(name.endswith("cover.xhtml") for name in namen) or "cover.xhtml" in opf_neu:
        raise Fehler(f"{pfad.name}: Die Titelbildseite ließ sich nicht entfernen.")


def pruefe_epub(pfad: Path) -> None:
    """Prüft das E-Book mit EPUBCheck, wenn es greifbar ist.

    Gesucht wird in der Umgebungsvariable EPUBCHECK (Pfad zur .jar-Datei oder
    zum Programm) und dann im Suchpfad. Ohne EPUBCheck bleibt das E-Book
    ungeprüft, und der Lauf sagt es.
    """
    werkzeug = os.environ.get("EPUBCHECK", "")
    if werkzeug.endswith(".jar"):
        befehl = ["java", "-jar", werkzeug]
    elif werkzeug:
        befehl = [werkzeug]
    elif shutil.which("epubcheck"):
        befehl = ["epubcheck"]
    else:
        hinweis(f"Hinweis: EPUBCheck nicht gefunden, {pfad.name} ist ungeprüft.")
        return
    lauf = subprocess.run([*befehl, "--quiet", str(pfad)], capture_output=True, text=True)
    meldungen = (lauf.stdout + lauf.stderr).strip()
    if lauf.returncode != 0:
        raise Fehler(f"EPUBCheck lehnt {pfad.name} ab:\n{meldungen}")
    hinweis(f"EPUBCheck: {pfad.name} ist gültig." + (f"\n{meldungen}" if meldungen else ""))


# --------------------------------------------------------------------------
# Aufruf
# --------------------------------------------------------------------------


def setze_band(nummer: int, angaben: Angaben, lauf: Lauf, erzeugnisse: set[str]) -> dict:
    """Setzt die gewählten Erzeugnisse eines Bandes und gibt ihre Daten zurück."""
    band = lies_band(nummer)
    daten: dict = {
        "band": nummer,
        "bandzeile": band.titelei["band"],
        "stand": band.titelei["stand"],
        "registerstichwoerter": len(band.register),
        "dateien": {},
    }

    bund = BUND_MM
    if "innenteil" in erzeugnisse:
        pdf, seiten, bund = setze_mit_bund(band, angaben, lauf, "druck", bund)
        pruefe_innenteil(pdf, angaben, seiten, bund)
        daten["dateien"]["innenteil"] = pdf.name
        daten["seiten"] = seiten
        daten["bund_mm"] = bund
        hinweis(f"Fertig: {pdf.name} ({seiten} Seiten, Bund {bund:.1f} mm)")

        umschlag, masse = setze_umschlagbogen(band, angaben, lauf, "druck", seiten)
        ziel = lauf.ziel / dateiname(nummer, "umschlag", lauf.kennung)
        shutil.copyfile(umschlag, ziel)
        daten["dateien"]["umschlag"] = ziel.name
        daten.update(masse)
        hinweis(
            f"Fertig: {ziel.name} (Rücken {masse['ruecken_zoll']:.4f} Zoll = {masse['ruecken_mm']} mm, "
            f"Bogen {masse['bogen_zoll'][0]:.4f} × {masse['bogen_zoll'][1]:.4f} Zoll)"
        )

    if "lesen" in erzeugnisse:
        pdf, seiten, bund_lesen = setze_mit_bund(band, angaben, lauf, "lesen", bund)
        daten["dateien"]["lesen"] = pdf.name
        if "seiten" in daten and seiten != daten["seiten"]:
            warne(
                f"Band {nummer}: Leseausgabe {seiten} Seiten, Innenteil {daten['seiten']} – "
                "sie sollten seitengleich sein."
            )
        daten.setdefault("seiten", seiten)
        hinweis(f"Fertig: {pdf.name} ({seiten} Seiten)")

    if "ebook" in erzeugnisse:
        titelbild_pdf, _ = setze_umschlagbogen(band, angaben, lauf, "ebook")
        titelbild = lauf.ziel / dateiname(nummer, "titelbild", lauf.kennung)
        if rastere(titelbild_pdf, titelbild):
            daten["dateien"]["titelbild"] = titelbild.name
            hinweis(f"Fertig: {titelbild.name} ({TITELBILD_PIXEL[0]} × {TITELBILD_PIXEL[1]} Pixel)")
        else:
            warne("Weder pdftoppm noch Ghostscript gefunden – kein Titelbild, das E-Book bleibt ohne.")
            titelbild = None
        epub = setze_epub(band, angaben, lauf, titelbild)
        daten["dateien"]["ebook"] = epub.name
        hinweis(f"Fertig: {epub.name} ({epub.stat().st_size / 1024:.0f} kB)")

    if ("innenteil" in erzeugnisse or "ebook" in erzeugnisse) and not angaben.anschrift:
        warne(
            f"Band {nummer}: Im Impressum fehlt die Anschrift des Verlags "
            f"({ANGABEN.relative_to(WURZEL)}, [impressum] anschrift) – für KDP noch nicht einreichbar."
        )
    return daten


def main() -> int:
    zerleger = argparse.ArgumentParser(
        description="Setzt das Manuskript zu Leseausgabe, Druckausgabe für KDP und E-Book.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    zerleger.add_argument("--band", type=int, choices=BAENDE, help="nur diesen Band setzen (Vorgabe: beide)")
    zerleger.add_argument(
        "--nur",
        action="append",
        choices=tuple(GRUPPEN),
        help="nur diese Erzeugnisse: lesen (PDF), druck (Innenteil und Umschlag für KDP), "
        "ebook (EPUB und Titelbild); mehrfach möglich (Vorgabe: alle)",
    )
    zerleger.add_argument(
        "--kennung",
        default="",
        help="Ausgabenummer (3.4) oder Entwurfskennung; steht in den Dateinamen, "
        "eine Ausgabenummer auch im Impressum (Vorgabe: keine)",
    )
    zerleger.add_argument("--ziel", type=Path, default=WURZEL / "build", help="Zielordner (Vorgabe: build/)")
    zerleger.add_argument(
        "--fassung",
        default="",
        help="Kennung des Quellstands für das Impressum (Vorgabe: git-Commit)",
    )
    zerleger.add_argument(
        "--nur-quelltext",
        action="store_true",
        help="nur den zusammengesetzten Markdown-Quelltext ausgeben – den des PDFs, "
        "mit --nur ebook den des E-Books",
    )
    argumente = zerleger.parse_args()
    baende = (argumente.band,) if argumente.band else BAENDE
    gruppen = argumente.nur or list(GRUPPEN)
    erzeugnisse = {e for g in gruppen for e in GRUPPEN[g]}
    if argumente.kennung and not re.fullmatch(r"[\w.-]+", argumente.kennung):
        zerleger.error("--kennung darf nur Buchstaben, Ziffern, Punkt und Bindestrich enthalten.")

    fassung = argumente.fassung or git("rev-parse", "--short", "HEAD", ersatz="ohne git")
    satzdatum = git("log", "-1", "--format=%cd", "--date=format:%d.%m.%Y", ersatz="")
    datum_iso = git("log", "-1", "--format=%cd", "--date=format:%Y-%m-%d", ersatz="") or (
        datetime.date.today().isoformat()
    )
    # Das Jahr der Rechteangabe im Impressum. Es kommt aus dem Quellstand und
    # nicht aus der Uhr des Bauläufers: Ein späterer Satz derselben Fassung
    # soll dieselbe Jahreszahl tragen. Ohne git bleibt nur das heutige Jahr.
    jahr = datum_iso[:4]
    ziel = argumente.ziel.resolve()
    lauf = Lauf(fassung, satzdatum, datum_iso, jahr, argumente.kennung, ziel)

    try:
        angaben = lies_angaben()
        if argumente.nur_quelltext:
            for nummer in baende:
                band = lies_band(nummer)
                if gruppen == ["ebook"]:
                    sys.stdout.write(baue_epub_quelltext(band))
                else:
                    art = "druck" if gruppen == ["druck"] else "lesen"
                    sys.stdout.write(baue_quelltext(band, angaben, lauf, art, BUND_MM))
            return 0

        fehlt = [p for p in ("pandoc", "lualatex") if not shutil.which(p)]
        if fehlt:
            print(
                f"Es fehlt: {', '.join(fehlt)}. Unter Debian/Ubuntu: sudo apt-get install "
                "pandoc texlive-luatex texlive-latex-recommended texlive-lang-german "
                "texlive-fonts-recommended texlive-pictures poppler-utils",
                file=sys.stderr,
            )
            return 1

        ziel.mkdir(parents=True, exist_ok=True)
        ergebnisse = []
        for nummer in baende:
            hinweis(f"Band {nummer}")
            ergebnisse.append(setze_band(nummer, angaben, lauf, erzeugnisse))
    except Fehler as fehler:
        print(f"Satz abgebrochen: {fehler}", file=sys.stderr)
        return 1

    bericht = {
        "kennung": lauf.kennung,
        "fassung": lauf.fassung,
        "satzdatum": lauf.satzdatum,
        "format": {
            "breite_zoll": angaben.breite,
            "hoehe_zoll": angaben.hoehe,
            "breite_cm": round(angaben.breite * 2.54, 2),
            "hoehe_cm": round(angaben.hoehe * 2.54, 2),
            "papier": angaben.papier,
        },
        "baende": ergebnisse,
        "warnungen": WARNUNGEN,
    }
    (ziel / "ausgabe.json").write_text(json.dumps(bericht, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

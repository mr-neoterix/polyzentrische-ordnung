#!/usr/bin/env python3
"""Setzt die Kapiteldateien aus manuskript/ zu einem einzelnen Buch-PDF.

Das Skript liest die Manuskriptquellen, fügt sie in der Reihenfolge ihrer
Dateinamen zu einem Quelltext zusammen und übergibt diesen an Pandoc, das
mit LuaLaTeX und der Vorlage in satz/vorlage.tex daraus ein PDF setzt.

Drei Dinge macht es dabei, die Pandoc allein nicht könnte:

*Kapitelköpfe:* Jede Kapiteldatei beginnt mit „# Neuntes Kapitel" und
„## Fehlertoleranz" – zwei Überschriften für einen Kopf. Sie werden zu einem
Kapitelanfang zusammengezogen; alle übrigen Überschriften der Datei rücken
auf die Abschnittsebene. Gezählt wird im Satz mit Ziffern („9. Kapitel"),
und die Ziffer kommt aus dem Dateinamen; die ausgeschriebene Bezeichnung der
Quelle wird dagegen geprüft, damit ein Umnummerieren nicht unbemerkt bleibt.

*Teilseiten:* Welches Kapitel zu welchem der acht Teile gehört, steht nicht
in den Kapiteldateien, sondern im Aufbau-Abschnitt von 00_inhalt.md. Von
dort wird die Zuordnung gelesen, damit sie nur an einer Stelle gepflegt
werden muss.

*Anführungszeichen:* Die Quellen setzen das öffnende Zeichen typografisch
(„), das schließende als geraden Zoll ("). Für den Satz wird daraus das
deutsche Paar „…“ beziehungsweise ‚…‘.

Aufruf:

    python3 satz/build.py                      # nach build/ setzen
    python3 satz/build.py --ausgabe buch.pdf
    python3 satz/build.py --nur-quelltext      # nur den Zwischenstand zeigen
"""

from __future__ import annotations

import argparse
import datetime
import re
import shutil
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
MANUSKRIPT = WURZEL / "manuskript"
VORLAGE = Path(__file__).resolve().parent / "vorlage.tex"
# Die Schriftschnitte liegen im Verzeichnis, nicht im TeX-Baum: So setzt
# jeder Rechner mit denselben Dateien, und der Bauläufer braucht kein
# Schriftpaket. Den Pfad bekommt die Vorlage als Variable herein.
SCHRIFTEN = Path(__file__).resolve().parent / "schriften"
INHALT = "00_inhalt.md"
STANDARDAUSGABE = WURZEL / "build" / "polyzentrische-ordnung-manuskript.pdf"


class Fehler(Exception):
    """Ein Problem, das den Satz abbricht und erklärt werden muss."""


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
    """Alle Eingriffe am Fließtext, die Pandoc nicht selbst vornimmt."""
    return gestellte_ziffern(deutsche_anfuehrung(text))


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
# Quellen lesen
# --------------------------------------------------------------------------


def lies_titelei(text: str) -> dict[str, str]:
    """Zieht Titel, Untertitel, Verfasser und Stand aus 00_inhalt.md.

    Gelesen wird nur der Kopf – alles vor dem ersten Abschnitt. Sonst
    verwechselte der Verfassername sich mit den fett gesetzten Teilzeilen
    des Aufbaus.
    """
    kopf = re.split(r"^## ", text, maxsplit=1, flags=re.M)[0]
    titel = re.search(r"^# (.+)$", kopf, re.M)
    untertitel = re.search(r"^### (.+)$", kopf, re.M)
    autor = re.search(r"^\*\*(.+?)\*\*$", kopf, re.M)
    stand = re.search(r"^\*(Manuskript\.[^*]+)\*$", kopf, re.M)
    if not titel:
        raise Fehler(f"{INHALT}: keine Titelzeile (# …) gefunden.")
    return {
        "titel": titel.group(1).strip(),
        "untertitel": untertitel.group(1).strip() if untertitel else "",
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
            f"{INHALT}: im Abschnitt „Aufbau“ ließ sich kein Teil erkennen. "
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
# Quelltext bauen
# --------------------------------------------------------------------------


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


def setze_ueberschriften(rumpf: str) -> str:
    """Hebt alle verbliebenen Überschriften des Kapitels auf eine Ebene.

    Innerhalb eines Kapitels gliedern die Quellen mal mit ##, mal mit ###
    (Kapitel 25 tut beides). Für den Satz ist das dieselbe Ebene: der
    Abschnitt unterhalb des Kapitels.
    """
    return re.sub(r"^#{2,6}\s+", "## ", rumpf, flags=re.M)


def baue_quelltext(fassung: str, satzdatum: str, jahr: str) -> str:
    inhalt_pfad = MANUSKRIPT / INHALT
    if not inhalt_pfad.is_file():
        raise Fehler(f"{inhalt_pfad} fehlt – ohne Inhaltsdatei kein Satz.")
    inhalt = inhalt_pfad.read_text(encoding="utf-8")

    titelei = lies_titelei(inhalt)
    vorspann = lies_vorspann(inhalt)
    aufbau = dict(vorspann).get("Aufbau", "")
    teile = lies_teile(aufbau)

    dateien = sorted(p for p in MANUSKRIPT.glob("[0-9][0-9]_*.md") if p.name != INHALT)
    if not dateien:
        raise Fehler(f"In {MANUSKRIPT} liegt keine Kapiteldatei.")

    teil_von_kapitel: dict[int, str] = {}
    for teiltitel, nummern in teile:
        for nummer in nummern:
            teil_von_kapitel[nummer] = teiltitel

    def kopfzeile(feld: str, wert: str) -> str:
        wert = deutsche_anfuehrung(wert).replace("\\", "\\\\").replace('"', '\\"')
        return f'{feld}: "{wert}"'

    zeilen: list[str] = []
    zeilen.append("---")
    zeilen.append(kopfzeile("titel", titelei["titel"]))
    zeilen.append(kopfzeile("untertitel", titelei["untertitel"]))
    zeilen.append(kopfzeile("autor", titelei["autor"]))
    zeilen.append(kopfzeile("stand", titelei["stand"]))
    zeilen.append(kopfzeile("jahr", jahr))
    zeilen.append(kopfzeile("fassung", fassung))
    zeilen.append(kopfzeile("satzdatum", satzdatum))
    zeilen.append("lang: de")
    zeilen.append("---")
    zeilen.append("")

    for titel, rumpf in vorspann:
        zeilen.append(f"\\vorspann{{{als_latex(titel)}}}")
        zeilen.append("")
        zeilen.append(typografie(rumpf))
        zeilen.append("")

    zeilen.append("\\hauptteil")
    zeilen.append("")

    offener_teil = None
    ohne_teil: list[str] = []
    schiefe_zaehlung: list[str] = []
    for pfad in dateien:
        nummer = kapitelnummer(pfad)
        kapitel = lies_kapitel(pfad)
        teiltitel = teil_von_kapitel.get(nummer)
        if teiltitel is None:
            ohne_teil.append(pfad.name)
        elif teiltitel != offener_teil:
            offener_teil = teiltitel
            zeilen.append(f"\\teil{{{als_latex(teiltitel)}}}")
            zeilen.append("")

        if not bezeichnung_stimmt(kapitel["bezeichnung"], nummer):
            schiefe_zaehlung.append(
                f"{pfad.name} nennt sich „{kapitel['bezeichnung']}“, "
                f"gesetzt wird nach dem Dateinamen als {kapitelbezeichnung(nummer)}"
            )

        zeilen.append(
            f"\\kapitel{{{als_latex(kapitelbezeichnung(nummer))}}}"
            f"{{{als_latex(kapitel['titel'])}}}"
        )
        zeilen.append("")

        text, belege = teile_belege_ab(kapitel["rumpf"])
        zeilen.append(typografie(setze_ueberschriften(text)).strip())
        zeilen.append("")
        if belege:
            zeilen.append("\\belegeanfang")
            zeilen.append("")
            zeilen.append(typografie(setze_ueberschriften(belege)).strip())
            zeilen.append("")
            zeilen.append("\\belegeende")
            zeilen.append("")
        else:
            print(f"  Hinweis: {pfad.name} hat keinen Belegabschnitt.", file=sys.stderr)

    if ohne_teil:
        print(
            "  Hinweis: ohne Teilzuordnung im Aufbau von "
            f"{INHALT}, deshalb ohne Teilseite gesetzt: {', '.join(ohne_teil)}",
            file=sys.stderr,
        )

    for meldung in schiefe_zaehlung:
        print(f"  Hinweis: {meldung}.", file=sys.stderr)

    print(
        f"  {len(dateien)} Kapitel in {len(teile)} Teilen, "
        f"{len(vorspann)} Vorspannabschnitte.",
        file=sys.stderr,
    )
    return "\n".join(zeilen) + "\n"


# --------------------------------------------------------------------------
# Aufruf
# --------------------------------------------------------------------------


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


def main() -> int:
    zerleger = argparse.ArgumentParser(
        description="Setzt das Manuskript zu einem Buch-PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    zerleger.add_argument(
        "--ausgabe",
        type=Path,
        default=STANDARDAUSGABE,
        help=f"Zieldatei (Vorgabe: {STANDARDAUSGABE.relative_to(WURZEL)})",
    )
    zerleger.add_argument(
        "--fassung",
        default="",
        help="Kennung des Quellstands für die Fußzeile (Vorgabe: git-Commit)",
    )
    zerleger.add_argument(
        "--nur-quelltext",
        action="store_true",
        help="nur den zusammengesetzten Markdown-Quelltext ausgeben",
    )
    argumente = zerleger.parse_args()

    fassung = argumente.fassung or git("rev-parse", "--short", "HEAD", ersatz="ohne git")
    satzdatum = git("log", "-1", "--format=%cd", "--date=format:%d.%m.%Y", ersatz="")
    # Das Jahr der Rechteangabe im Impressum. Es kommt aus dem Quellstand und
    # nicht aus der Uhr des Bauläufers: Ein späterer Satz derselben Fassung
    # soll dieselbe Jahreszahl tragen. Ohne git bleibt nur das heutige Jahr.
    jahr = git("log", "-1", "--format=%cd", "--date=format:%Y", ersatz="") or str(
        datetime.date.today().year
    )

    try:
        quelltext = baue_quelltext(fassung, satzdatum, jahr)
    except Fehler as fehler:
        print(f"Satz abgebrochen: {fehler}", file=sys.stderr)
        return 1

    if argumente.nur_quelltext:
        sys.stdout.write(quelltext)
        return 0

    if not shutil.which("pandoc"):
        print(
            "Pandoc fehlt. Unter Debian/Ubuntu: sudo apt-get install pandoc "
            "texlive-luatex texlive-latex-recommended texlive-lang-german "
            "texlive-fonts-recommended",
            file=sys.stderr,
        )
        return 1

    ausgabe = argumente.ausgabe.resolve()
    ausgabe.parent.mkdir(parents=True, exist_ok=True)
    zwischenstand = ausgabe.with_suffix(".md")
    zwischenstand.write_text(quelltext, encoding="utf-8")

    befehl = [
        "pandoc",
        str(zwischenstand),
        "--from=markdown+raw_tex-auto_identifiers",
        "--to=pdf",
        "--pdf-engine=lualatex",
        "--template",
        str(VORLAGE),
        "--top-level-division=chapter",
        f"--resource-path={MANUSKRIPT}",
        f"--variable=schriftverzeichnis={SCHRIFTEN}/",
        "--output",
        str(ausgabe),
    ]
    print(f"  {' '.join(befehl)}", file=sys.stderr)
    lauf = subprocess.run(befehl, cwd=WURZEL)
    if lauf.returncode != 0:
        print(
            "Pandoc ist gescheitert. Der zusammengesetzte Quelltext liegt in "
            f"{zwischenstand} und lässt sich von Hand nachprüfen.",
            file=sys.stderr,
        )
        return lauf.returncode

    groesse = ausgabe.stat().st_size / 1024
    print(f"  Fertig: {ausgabe} ({groesse:.0f} kB)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

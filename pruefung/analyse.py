#!/usr/bin/env python3
"""Prüfung der Friedensvermutung nach der Vorregistrierung vom 15.08.2026.

Frage: Sind Staat-Jahre mit gewählter Regierung, in denen politische Macht nach
sozioökonomischer Stellung gleicher verteilt ist, seltener Ausgangspunkt
zwischenstaatlicher militarisierter Auseinandersetzungen?

Die Datenherkunft steht in der Vorregistrierung. Das Skript erwartet die Dateien
im Arbeitsverzeichnis, das über --daten übergeben wird:

    vdem_sub.csv            Auszug aus V-Dem v16 (vdemdata, data/vdem.RData)
    gml_mid_ddydisps.rda    Gibler-Miller-Little MID, gerichtete Dyaden-Jahre
    cow_mid_dirdisps.rda    COW MID 5.0, gerichtete Dyaden-Jahre
    cow_states.rda          COW-Staatensystem
    cow_majors.rda          Großmächte
    cow_nmc.rda             Machtanteil (CINC)

Aufruf:  python3 analyse.py --daten <verzeichnis>
"""

import argparse
import warnings

import numpy as np
import pandas as pd
import pyreadr
import statsmodels.api as sm

warnings.filterwarnings("ignore")

JAHR_VON, JAHR_BIS = 1946, 2010


def lies(pfad, name):
    return pyreadr.read_r(f"{pfad}/{name}.rda")[name]


def mid_kennzeichen(dd, praefix, onset_spalte):
    """Staat-Jahr-Kennzeichen aus gerichteten Dyaden-Jahr-Daten.

    ccode1 ist der handelnde Staat der gerichteten Dyade. Gezählt wird nur der
    Beginn einer Auseinandersetzung, nicht ihr Fortdauern.
    """
    d = dd[dd[onset_spalte] == 1].copy()
    initiator = d[(d.orig1 == 1) & (d.sidea1 == 1)]
    beteiligt = d
    gewalt = d[(d.orig1 == 1) & (d.sidea1 == 1) & (d.hostlev1 >= 4)]

    out = []
    for name, teil in [("init", initiator), ("teiln", beteiligt), ("gewalt", gewalt)]:
        g = (teil.groupby(["ccode1", "year"]).size().rename(f"{praefix}_{name}")
             .reset_index().rename(columns={"ccode1": "ccode"}))
        g[f"{praefix}_{name}"] = 1
        out.append(g)

    res = out[0]
    for g in out[1:]:
        res = res.merge(g, on=["ccode", "year"], how="outer")
    return res


def staatensystem(cs):
    """Staat-Jahre des COW-Systems, damit eine Null auch eine Null sein kann."""
    zeilen = []
    for _, r in cs.iterrows():
        for j in range(int(r.styear), int(r.endyear) + 1):
            zeilen.append((r.ccode, j))
    return pd.DataFrame(zeilen, columns=["ccode", "year"]).drop_duplicates()


def grossmaechte(cm):
    zeilen = []
    for _, r in cm.iterrows():
        for j in range(int(r.styear), int(r.endyear) + 1):
            zeilen.append((r.ccode, j))
    df = pd.DataFrame(zeilen, columns=["ccode", "year"]).drop_duplicates()
    df["grossmacht"] = 1
    return df


def schaetze(df, dv, iv, kontrollen, jahres_fe=True, etikett=""):
    """Logit mit Jahres-Fixeffekten und nach Staat geclusterten Standardfehlern.

    Jahre ohne Variation in der abhängigen Variablen können mit Fixeffekten nicht
    identifiziert werden und fallen heraus; die Zahl wird ausgewiesen.
    """
    d = df.dropna(subset=[dv, iv] + kontrollen).copy()
    n_roh = len(d)
    verworfen = 0
    if jahres_fe:
        var = d.groupby("year")[dv].nunique()
        gute = var[var > 1].index
        verworfen = n_roh - len(d[d.year.isin(gute)])
        d = d[d.year.isin(gute)]

    X = d[[iv] + kontrollen].copy()
    if jahres_fe:
        X = pd.concat([X, pd.get_dummies(d["year"].astype(int), prefix="j",
                                         drop_first=True, dtype=float)], axis=1)
    else:
        X["jahr"] = d["year"] - d["year"].mean()
    X = sm.add_constant(X.astype(float))
    y = d[dv].astype(float)

    res = sm.Logit(y, X).fit(disp=0, maxiter=200, cov_type="cluster",
                             cov_kwds={"groups": d["ccode"].values})

    beta, se = res.params[iv], res.bse[iv]
    p = res.pvalues[iv]

    # Substanzieller Effekt: mittlere vorhergesagte Wahrscheinlichkeit bei
    # beobachtetem IV gegen dieselbe bei IV plus einer Standardabweichung.
    p0 = res.predict(X).mean()
    Xs = X.copy()
    Xs[iv] = Xs[iv] + 1.0          # IV ist standardisiert
    p1 = res.predict(Xs).mean()
    rel = (p1 - p0) / p0 * 100

    return dict(etikett=etikett, dv=dv, n=len(d), verworfen=verworfen,
                ereignisse=int(y.sum()), staaten=d.ccode.nunique(),
                beta=beta, se=se, p=p, p0=p0, p1=p1, rel=rel)


def zeile(r):
    stern = "***" if r["p"] < .01 else "**" if r["p"] < .05 else "*" if r["p"] < .1 else ""
    return (f"{r['etikett']:<44} N={r['n']:>5}  Ereign.={r['ereignisse']:>4}  "
            f"b={r['beta']:+.4f}  SE={r['se']:.4f}  p={r['p']:.3f}{stern:<3}  "
            f"Effekt={r['rel']:+.1f}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--daten", required=True)
    a = ap.parse_args()
    P = a.daten

    vdem = pd.read_csv(f"{P}/vdem_sub.csv")
    gml = lies(P, "gml_mid_ddydisps")
    cow = lies(P, "cow_mid_dirdisps")
    cs, cm, nmc = lies(P, "cow_states"), lies(P, "cow_majors"), lies(P, "cow_nmc")

    system = staatensystem(cs)
    gm = grossmaechte(cm)
    g_flags = mid_kennzeichen(gml, "gml", "gmlmidonset")
    c_flags = mid_kennzeichen(cow, "cow", "disponset")

    v = vdem.dropna(subset=["COWcode"]).rename(columns={"COWcode": "ccode"})
    v = v[(v.year >= JAHR_VON) & (v.year <= JAHR_BIS + 1)].copy()
    v["ccode"] = v.ccode.astype(float)

    df = system.merge(v, on=["ccode", "year"], how="inner")
    df = df.merge(gm, on=["ccode", "year"], how="left")
    df = df.merge(g_flags, on=["ccode", "year"], how="left")
    df = df.merge(c_flags, on=["ccode", "year"], how="left")
    df = df.merge(nmc[["ccode", "year", "cinc"]], on=["ccode", "year"], how="left")
    for c in ["grossmacht", "gml_init", "gml_teiln", "gml_gewalt",
              "cow_init", "cow_teiln", "cow_gewalt"]:
        df[c] = df[c].fillna(0.0)

    # Abhängige Variablen im Folgejahr
    df = df.sort_values(["ccode", "year"])
    for c in ["gml_init", "gml_teiln", "gml_gewalt", "cow_init"]:
        naechstes = df[["ccode", "year", c]].copy()
        naechstes["year"] = naechstes["year"] - 1
        df = df.merge(naechstes.rename(columns={c: c + "_f1"}), on=["ccode", "year"], how="left")

    df = df[(df.year >= JAHR_VON) & (df.year <= JAHR_BIS)].copy()
    df["lgdppc"] = np.log(df["e_gdppc"])
    df["lpop"] = np.log(df["e_pop"])

    # Grundgesamtheit: Wahldemokratien und liberale Demokratien
    haupt = df[df.v2x_regime.isin([2, 3])].copy()
    alt = df[df.v2x_polyarchy >= 0.5].copy()

    for d in (haupt, alt):
        m, s = d["v2pepwrses"].mean(), d["v2pepwrses"].std()
        d["macht_z"] = (d["v2pepwrses"] - m) / s

    K = ["lgdppc", "lpop", "grossmacht"]
    K_cinc = ["lgdppc", "lpop", "cinc"]

    print("=" * 118)
    print("PRÜFUNG DER FRIEDENSVERMUTUNG – Ergebnisse nach der Vorregistrierung vom 15.08.2026")
    print("=" * 118)
    print(f"Panel gesamt {JAHR_VON}-{JAHR_BIS}: {len(df)} Staat-Jahre, {df.ccode.nunique()} Staaten")
    print(f"Hauptgrundgesamtheit (v2x_regime 2/3): {len(haupt)} Staat-Jahre, "
          f"{haupt.ccode.nunique()} Staaten")
    print(f"Alternative (v2x_polyarchy >= 0,5):    {len(alt)} Staat-Jahre, "
          f"{alt.ccode.nunique()} Staaten")
    print(f"Verteilungsgröße v2pepwrses in der Hauptgrundgesamtheit: "
          f"M={haupt.v2pepwrses.mean():.3f}  SD={haupt.v2pepwrses.std():.3f}")
    print()

    erg = []
    erg.append(schaetze(haupt, "gml_init_f1", "macht_z", K,
                        etikett="HAUPTMODELL  Initiierung (GML), t+1"))
    print("HAUPTMODELL")
    print(" ", zeile(erg[-1]))
    print()

    print("ROBUSTHEIT")
    erg.append(schaetze(alt, "gml_init_f1", "macht_z", K,
                        etikett="R1 andere Gruppenabgrenzung (polyarchy)"))
    erg.append(schaetze(haupt, "gml_teiln_f1", "macht_z", K,
                        etikett="R2a jede Beteiligung statt Initiierung"))
    erg.append(schaetze(haupt, "gml_gewalt_f1", "macht_z", K,
                        etikett="R2b nur Gewaltanwendung/Krieg"))
    erg.append(schaetze(haupt, "cow_init_f1", "macht_z", K,
                        etikett="R3 COW MID statt GML"))
    erg.append(schaetze(haupt, "gml_init_f1", "macht_z", K_cinc,
                        etikett="R4 Machtanteil statt Großmachtstatus"))
    for r in erg[1:]:
        print(" ", zeile(r))
    print()

    print("ZUSATZ (nicht vorregistriert, nur zur Einordnung)")
    zus = [schaetze(haupt, "gml_init_f1", "macht_z", K, jahres_fe=False,
                    etikett="Z1 Jahrestrend statt Jahres-Fixeffekte"),
           schaetze(haupt, "gml_init_f1", "macht_z", [],
                    etikett="Z2 ohne Kontrollen")]
    for r in zus:
        print(" ", zeile(r))
    print()

    haupt_r = erg[0]
    rob = erg[1:]
    rob_ok = sum(1 for r in rob if r["beta"] < 0 and r["p"] < .05)
    b1 = haupt_r["beta"] < 0 and haupt_r["p"] < .05
    b2 = rob_ok >= 3
    b3 = haupt_r["rel"] <= -10.0

    print("=" * 118)
    print("ENTSCHEIDUNG NACH DER VORREGISTRIERTEN REGEL")
    print("=" * 118)
    print(f"  (1) Hauptmodell negativ und p < 0,05                : {'JA' if b1 else 'NEIN'}"
          f"   (b={haupt_r['beta']:+.4f}, p={haupt_r['p']:.3f})")
    print(f"  (2) mindestens 3 von 4 Robustheitsvarianten desgl.  : {'JA' if b2 else 'NEIN'}"
          f"   ({rob_ok} von {len(rob)})")
    print(f"  (3) Effekt mindestens -10 Prozent relativ           : {'JA' if b3 else 'NEIN'}"
          f"   ({haupt_r['rel']:+.1f} %)")
    print()
    if b1 and b2 and b3:
        urteil = "GESTÜTZT"
    elif not b1:
        urteil = "NICHT GESTÜTZT"
    else:
        urteil = "UNENTSCHIEDEN"
    print(f"  ERGEBNIS: {urteil}")
    print("=" * 118)

    pd.DataFrame(erg + zus).to_csv(f"{P}/ergebnisse.csv", index=False)


if __name__ == "__main__":
    main()

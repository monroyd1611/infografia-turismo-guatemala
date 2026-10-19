"""Bloque 3. Estacionalidad por mes y comparacion de las siete series en cuatro preguntas."""
import textwrap

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

from datos import NOMBRES
from estilo import AZUL, CAJAS, GRIS, NARANJA, TEXTO, ejes

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
MESES_LARGO = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
               "Septiembre", "Octubre", "Noviembre", "Diciembre"]
CAUSAS = {12: "Aguinaldo y\nfin de año", 7: "Vacaciones\ny Bono 14", 3: "Semana Santa", 4: "Semana Santa"}


def _cociente(a, b):
    return a / b if b else np.nan


def metricas(series):
    """Fuerza estacional (STL), crecimiento 2019 vs 2009, volatilidad y caida abr-jun 2020."""
    filas = {}
    for k, s in series.items():
        x = s.replace(0, np.nan).interpolate().bfill()
        r = STL(x, period=12, robust=True).fit()
        fs = max(0.0, 1 - np.var(r.resid) / np.var(r.seasonal + r.resid))
        p19, p09 = s["2019"].mean(), s["2009"].mean()
        con_base = p19 > 0
        filas[k] = {
            "estacionalidad": fs,
            "crecimiento": (_cociente(p19, p09) - 1) * 100 if con_base else np.nan,
            "volatilidad": s.pct_change().replace([np.inf, -np.inf], np.nan).std(),
            "pandemia": (_cociente(s["2020-04":"2020-06"].mean(), p19) - 1) * 100 if con_base else np.nan,
        }
    return pd.DataFrame(filas).T


def _parte_a(fig, series):
    caja = CAJAS["b3a"]
    x0, y0, w, h = caja
    total = series["Total"]["2009":"2019"]
    prom = total.groupby(total.index.month).mean() / 1000
    mes_max, mes_min = prom.idxmax(), prom.idxmin()
    sobre = (prom.max() / prom.min() - 1) * 100

    titulo = textwrap.fill("%s trae %.0f%% más viajeros que el mes más bajo" % (MESES_LARGO[mes_max - 1], sobre), 40)
    fig.text(x0, y0 + h, titulo, fontsize=15, fontweight="bold", color=AZUL, va="top", linespacing=1.15)
    fig.text(x0, y0 + h - 0.0335, "Viajeros por mes, promedio 2009-2019, miles (gris: mínimo)", fontsize=10.5, color=GRIS, va="top")

    ax = ejes(fig, (x0 + 0.035, y0 + 0.012, w - 0.035, h - 0.065))
    ymax = prom.max() * 1.42
    naranja = {m for m in prom.nlargest(5).index if m in CAUSAS}
    colores = [NARANJA if m in naranja else AZUL for m in range(1, 13)]
    ax.bar(range(1, 13), prom.values, color=colores, width=0.72)

    for m in sorted(naranja):
        ax.text(m, prom[m] + 0.012 * ymax, "%.0f" % prom[m], ha="center", va="bottom",
                fontsize=9.5, color=NARANJA, fontweight="bold")
    ax.text(mes_min, prom[mes_min] + 0.012 * ymax, "%.0f" % prom[mes_min], ha="center", va="bottom",
            fontsize=9.5, color=GRIS, fontweight="bold")

    grupos = []
    santa = sorted({3, 4} & naranja)
    if santa:
        grupos.append((santa, "Semana Santa\n(mar-abr)" if len(santa) == 2 else "Semana Santa"))
    for m in (7, 12):
        if m in naranja:
            grupos.append(([m], CAUSAS[m]))
    for ms, texto in grupos:
        y = max(prom[m] for m in ms) + 0.085 * ymax
        if ms[-1] == 12:
            ax.text(12.5, y, texto, ha="right", va="bottom", fontsize=9, color=NARANJA, linespacing=1.15)
        else:
            ax.text(float(np.mean(ms)), y, texto, ha="center", va="bottom", fontsize=9, color=NARANJA,
                    linespacing=1.15)

    ax.set_ylim(0, ymax)
    ax.set_xlim(0.4, 12.6)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MESES)
    ax.set_yticks([v for v in range(0, int(ymax), 100)])
    ax.grid(axis="y", color="#E5E7EB", lw=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=9.5)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#D1D5DB")


def _barras(ax, claves, vals, fmt, invertir=False):
    largo = {k: (-vals[k] if invertir else vals[k]) for k in claves}
    validas = sorted([k for k in claves if np.isfinite(largo[k])], key=lambda k: -largo[k])
    nulas = [k for k in claves if not np.isfinite(largo[k])]
    orden = validas + nulas
    mejor = fmt(vals[validas[0]])
    ganadoras = {k for k in validas if fmt(vals[k]) == mejor}
    tope = max(max(largo[k] for k in validas), 0)
    piso = min(min(largo[k] for k in validas), 0)
    span = (tope - piso) or 1

    for i, k in enumerate(orden):
        if k in nulas:
            ax.text(0.02 * span, i, "no aplica*", va="center", fontsize=9, color=GRIS)
            continue
        gana = k in ganadoras
        ax.barh(i, largo[k], color=NARANJA if gana else AZUL, height=0.68)
        ax.text(max(largo[k], 0) + 0.03 * span, i, fmt(vals[k]), va="center", fontsize=9,
                color=NARANJA if gana else GRIS, fontweight="bold" if gana else "normal")

    ax.set_ylim(len(orden) - 0.5, -0.5)
    ax.set_xlim(piso * 1.55 if piso < 0 else 0, tope * 1.55)
    ax.set_yticks(range(len(orden)))
    ax.set_yticklabels([NOMBRES[k] for k in orden], fontsize=9)
    for lbl, k in zip(ax.get_yticklabels(), orden):
        lbl.set_color(TEXTO)
        if k in ganadoras:
            lbl.set_fontweight("bold")
    ax.set_xticks([])
    ax.tick_params(length=0)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_color("#D1D5DB")
    return ganadoras


def _parte_b(fig, series):
    x0, y0, w, h = CAJAS["b3b"]
    m = metricas(series)
    claves = list(NOMBRES)

    def mejor(col, signo=1):
        return (m[col] * signo).idxmax()

    g1, g2, g3 = mejor("estacionalidad"), mejor("crecimiento"), mejor("volatilidad")
    cambiantes = [NOMBRES[g1]] if g1 == g3 else [NOMBRES[g1], NOMBRES[g3]]
    titulo = "%s creció más; %s, %s cambiantes" % (
        NOMBRES[g2], " y ".join(cambiantes), "la más" if len(cambiantes) == 1 else "las más")
    fig.text(x0, y0 + h, textwrap.fill(titulo, 40), fontsize=15, fontweight="bold", color=AZUL,
             va="top", linespacing=1.15)

    preguntas = [
        ("Más estacional", "Fuerza de la temporada, 0 a 1", "estacionalidad", lambda v: "%.3f" % v, False),
        ("Mayor crecimiento", "Viajeros/mes, 2019 vs. 2009", "crecimiento", lambda v: "%+.1f%%" % v, False),
        ("Más volátil", "Variación típica mes a mes", "volatilidad", lambda v: "%.3f" % v, False),
        ("Mayor caída en 2020", "Abr-jun 2020 vs. prom. 2019", "pandemia", lambda v: "%+.1f%%" % v, True),
    ]
    sep = 0.03
    pw = (w - sep) / 2
    tope, piso, sep_y = y0 + h - 0.038, y0 + 0.026, 0.008
    ph = (tope - piso - sep_y) / 2
    for i, (tit, desc, col, fmt, inv) in enumerate(preguntas):
        px = x0 + (i % 2) * (pw + sep)
        py = tope - (i // 2 + 1) * ph - (i // 2) * sep_y
        fig.text(px, py + ph, tit, fontsize=10, fontweight="bold", color=AZUL, va="top")
        fig.text(px, py + ph - 0.0125, desc, fontsize=9, color=GRIS, va="top")
        ax = ejes(fig, (px + 0.083, py, pw - 0.083, ph - 0.027))
        _barras(ax, claves, m[col].to_dict(), fmt, invertir=inv)

    sin_base = [k for k in claves if not series[k]["2019"].sum()]
    if sin_base:
        k = sin_base[0]
        ultimo = series[k][series[k] > 0].index.max().year
        nota = "* %s: último registro de turistas en %d, por eso no se mide su crecimiento ni su caída." % (
            NOMBRES[k], ultimo)
        fig.text(x0, y0 + 0.002, textwrap.fill(nota, 60), fontsize=9, color=GRIS, va="bottom")


def dibujar(fig, series, train, test):
    _parte_a(fig, series)
    _parte_b(fig, series)
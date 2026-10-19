"""Bloque 4. Comparacion de modelos en el conjunto de prueba y proyeccion del ganador."""
import textwrap

import pandas as pd

from estilo import AZUL, CAJAS, GRIS, LINEA, NARANJA, TEXTO, ejes
from modelos import ajustar

ETIQUETAS = {
    "prophet": "Prophet",
    "holt": "Holt",
    "snaive": "Seasonal naive",
    "arima": "ARIMA estacional",
    "hw": "Holt-Winters",
}


def _miles(v):
    return "{:,.0f}".format(v)


def _titulo(fig, caja, texto, sub):
    x0, y0, w, h = caja
    fig.text(x0, y0 + h, textwrap.fill(texto, 40), fontsize=15, fontweight="bold", color=AZUL,
             va="top", linespacing=1.15)
    fig.text(x0, y0 + h - 0.0335, sub, fontsize=10.5, color=GRIS, va="top")


def _parte_a(fig, metricas):
    caja = CAJAS["b4a"]
    x0, y0, w, h = caja
    ganador = metricas.index[0]
    _titulo(fig, caja, "Prophet es el modelo que menos se equivoca",
            "Error en abr 2021 - jun 2026, viajeros por mes (menor es mejor)")

    orden = list(metricas.index)
    nombres = 0.088
    sep = 0.022
    pw = (w - nombres - sep) / 2
    tope = y0 + h - 0.062
    piso = y0 + 0.048
    paneles = [("MAE", "Error promedio (MAE)"), ("RMSE", "Penaliza errores grandes (RMSE)")]
    xmax = metricas.values.max() * 1.42
    for j, (col, tit) in enumerate(paneles):
        px = x0 + nombres + j * (pw + sep)
        fig.text(px, tope, tit, fontsize=10, fontweight="bold", color=AZUL, va="top")
        ax = ejes(fig, (px, piso, pw, tope - piso - 0.016))
        for i, k in enumerate(orden):
            v = metricas.loc[k, col]
            gana = k == ganador
            ax.barh(i, v, color=NARANJA if gana else AZUL, height=0.64)
            ax.text(v + 0.03 * xmax, i, _miles(v), va="center", fontsize=9,
                    color=NARANJA if gana else GRIS, fontweight="bold" if gana else "normal")
        ax.set_xlim(0, xmax)
        ax.set_ylim(len(orden) - 0.5, -0.5)
        ax.set_xticks([])
        ax.set_yticks(range(len(orden)))
        if j == 0:
            ax.set_yticklabels([ETIQUETAS[k] for k in orden], fontsize=9.5)
            for lbl, k in zip(ax.get_yticklabels(), orden):
                lbl.set_color(TEXTO)
                if k == ganador:
                    lbl.set_fontweight("bold")
        else:
            ax.set_yticklabels([])
        ax.tick_params(length=0)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_color(LINEA)

    nota = ("Modelos entrenados con ene 2009 - mar 2021 y evaluados con meses que no vieron. "
            "No se usa AIC/BIC: no es comparable entre familias de modelos distintas.")
    fig.text(x0, y0 + 0.002, textwrap.fill(nota, 82), fontsize=9, color=GRIS, va="bottom", linespacing=1.3)


def _parte_b(fig, series, test, banda):
    caja = CAJAS["b4b"]
    x0, y0, w, h = caja
    real = test["Total"]
    desvio = (banda["yhat"].sum() / real.sum() - 1) * 100
    _titulo(fig, caja, "Ni el mejor modelo previó el rebote: estimó %.0f%% menos viajeros" % abs(desvio),
            "Viajeros mensuales, miles: real frente a la estimación de Prophet")

    ax = ejes(fig, (x0 + 0.035, y0 + 0.060, w - 0.035, h - 0.122))
    inicio = real.index[0]
    previo = series["Total"][inicio - pd.DateOffset(months=24):inicio - pd.DateOffset(months=1)] / 1000
    r = real / 1000
    b = banda / 1000

    ax.fill_between(b.index, b["yhat_lower"], b["yhat_upper"], color=NARANJA, alpha=0.16, lw=0)
    ax.plot(previo.index, previo.values, color=GRIS, lw=1.4)
    ax.plot([previo.index[-1], r.index[0]], [previo.iloc[-1], r.iloc[0]], color=GRIS, lw=1.4)
    ax.plot(r.index, r.values, color=AZUL, lw=1.6)
    ax.plot(b.index, b["yhat"], color=NARANJA, lw=1.6, ls=(0, (4, 2)))
    ax.axvline(inicio, color=LINEA, lw=0.8)

    ymax = max(previo.max(), r.max(), b["yhat_upper"].max()) * 1.30
    ax.text(previo.index[1], ymax * 0.97, "Entrenamiento", fontsize=9, color=GRIS, va="top")
    ax.text(inicio + pd.DateOffset(months=1), ymax * 0.97, "Prueba", fontsize=9, color=GRIS, va="top")

    pos = r.index[-14]
    ax.annotate("Real", (pos, r[pos]), xytext=(0, 12), textcoords="offset points", fontsize=9.5,
                color=AZUL, fontweight="bold", ha="center", va="bottom")
    ax.text(b.index[20], ymax * 0.97, "Estimación (intervalo 80%)", fontsize=9.5, color=NARANJA,
            fontweight="bold", va="top")

    ax.set_ylim(0, ymax)
    ax.set_xlim(previo.index[0], real.index[-1] + pd.DateOffset(months=1))
    ax.grid(axis="y", color="#E5E7EB", lw=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=9.5)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(LINEA)

    dentro = ((real >= banda["yhat_lower"]) & (real <= banda["yhat_upper"])).mean() * 100
    nota = ("Los últimos 12 meses de entrenamiento son la caída de 2020, así que el modelo proyecta esa baja; "
            "el rebote pospandemia no estaba en sus datos. Solo %.0f%% de los meses reales cae dentro del intervalo." % dentro)
    fig.text(x0, y0 + 0.002, textwrap.fill(nota, 82), fontsize=9, color=GRIS, va="bottom", linespacing=1.3)


def dibujar(fig, series, train, test):
    metricas, _, banda = ajustar(train, test)
    _parte_a(fig, metricas)
    _parte_b(fig, series, test, banda)

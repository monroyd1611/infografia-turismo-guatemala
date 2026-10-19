"""Bloque 5. Recomendaciones para INGUAT y ficha tecnica."""
import textwrap

from matplotlib.lines import Line2D

from estilo import AZUL, CAJAS, GRIS, LINEA, NARANJA, TEXTO
from modelos import ajustar


def _vs19(s):
    return (s["2025-07":].mean() / s["2019"].mean() - 1) * 100


def dibujar(fig, series, train, test):
    x0, y0, w, h = CAJAS["b5"]
    total = series["Total"]
    centro, norte, europa = series["America Del Centro"], series["America Del Norte"], series["Europa"]
    hist = total["2009":"2019"]
    prom = hist.groupby(hist.index.month).mean()
    dic = (prom[12] / prom.mean() - 1) * 100
    _, _, banda = ajustar(train, test)
    desvio = abs(banda["yhat"].sum() / test["Total"].sum() - 1) * 100

    fig.text(x0, y0 + h, "Qué hacer: cuatro decisiones para INGUAT", fontsize=15, fontweight="bold",
             color=AZUL, va="top")
    recs = [
        ("%.1f%%" % (centro.sum() / total.sum() * 100), "Reactivar Centroamérica",
         "Es el %.1f%% del flujo 2009-2026 y sigue %.1f%% abajo de 2019." % (centro.sum() / total.sum() * 100, abs(_vs19(centro)))),
        ("+%.1f%%" % _vs19(norte), "Consolidar Norte y Europa",
         "Norteamérica crece %.1f%% y Europa %.1f%% frente a 2019; reforzar sus temporadas altas." % (_vs19(norte), _vs19(europa))),
        ("+%.0f%%" % dic, "Planificar los picos",
         "Diciembre trae %.0f%% más viajeros que un mes promedio; preparar capacidad para diciembre, Semana Santa y julio." % dic),
        ("%.0f%%" % desvio, "Pronosticar por segmento",
         "El mejor modelo del total se quedó %.0f%% corto; cada mercado se mueve distinto." % desvio),
    ]
    cw = w / 4
    for i, (cifra, tit, txt) in enumerate(recs):
        cx = x0 + i * cw + (0.012 if i else 0)
        fig.text(cx, y0 + h - 0.026, "%d. %s" % (i + 1, tit), fontsize=10.5, fontweight="bold", color=AZUL, va="top")
        fig.text(cx, y0 + h - 0.040, cifra, fontsize=22, fontweight="bold", color=NARANJA, va="top")
        fig.text(cx, y0 + h - 0.064, textwrap.fill(txt, 34), fontsize=9, color=TEXTO, va="top", linespacing=1.25)
        if i:
            fig.add_artist(Line2D([x0 + i * cw] * 2, [y0 + 0.022, y0 + h - 0.024], color=LINEA, lw=0.8,
                                  transform=fig.transFigure))

    fig.add_artist(Line2D([x0, x0 + w], [y0 + 0.016, y0 + 0.016], color=LINEA, lw=0.8, transform=fig.transFigure))
    ficha = ("Fuente: Base de Migración 2009-2026 INGUAT/IGM.  Metodología: Turista + Excursionista, partición 70/30 "
             "(ene 2009 - mar 2021 / abr 2021 - jun 2026), pronóstico con Prophet.\n"
             "Diego Monroy, Marco Carbajal, Carlos Angel. UVG CC3084 Sección 20, Grupo 7.")
    fig.text(x0, y0 + 0.012, ficha, fontsize=9, color=GRIS, va="top", linespacing=1.3)

"""Bloque 2. Panorama historico 2009-2026: linea mensual con anotaciones."""
import pandas as pd

from estilo import AZUL, CAJAS, GRIS, LINEA, NARANJA, ejes, titulo_bloque


def dibujar(fig, series):
    caja = CAJAS["b2"]
    x0, y0, w, h = caja
    titulo_bloque(fig, caja, "Dos décadas de crecimiento, un golpe en 2020 y una recuperación a medias",
                  "Viajeros mensuales (turistas y excursionistas), miles")
    ax = ejes(fig, (x0 + 0.035, y0 + 0.012, w - 0.035, h - 0.062))
    s = series["Total"] / 1000

    ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2021-06-01"), color=NARANJA, alpha=0.12, lw=0)
    ax.plot(s.index, s.values, color=AZUL, lw=1.6)
    ref = series["Total"]["2019"].mean() / 1000
    ax.axhline(ref, color=GRIS, lw=0.8, ls=(0, (4, 3)))
    ax.text(pd.Timestamp("2009-02-01"), ref - 10, "Promedio mensual 2019: %d mil" % round(ref),
            color=GRIS, fontsize=9, va="top")

    pico = s["2019"].idxmax()
    ax.scatter([pico], [s[pico]], color=AZUL, s=22, zorder=3)
    ax.annotate("Récord: %d mil viajeros\nen dic 2019" % round(s[pico]), (pico, s[pico]),
                xytext=(-60, 4), textcoords="offset points", fontsize=9.5, color=AZUL,
                ha="right", va="center", arrowprops=dict(arrowstyle="-", color=AZUL, lw=0.7))

    ini = pd.Timestamp("2009-01-01")
    ax.annotate("Crecimiento sostenido: de %d mil\na %d mil al mes (2009-2019)" % (round(s["2009"].mean()), round(s["2019"].mean())),
                (pd.Timestamp("2013-06-01"), s["2013"].mean()), xytext=(pd.Timestamp("2013-06-01"), 440),
                textcoords="data", fontsize=9.5, color=AZUL, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=AZUL, lw=0.7))

    bajo = s["2020-04":"2020-06"].mean()
    ax.annotate("Cierre de fronteras (mar 2020)\n%d mil viajeros en abril, %.1f%% vs. prom. 2019" % (
                    round(s[pd.Timestamp("2020-04-01")]), (s[pd.Timestamp("2020-04-01")] / ref - 1) * 100),
                (pd.Timestamp("2020-04-01"), s[pd.Timestamp("2020-04-01")]), xytext=(-30, 60), textcoords="offset points",
                fontsize=9.5, color=NARANJA, fontweight="bold", ha="right", va="center",
                arrowprops=dict(arrowstyle="-", color=NARANJA, lw=0.8))

    ax.annotate("Reapertura gradual\n(2021)", (pd.Timestamp("2021-04-01"), s[pd.Timestamp("2021-04-01")]),
                xytext=(16, -22), textcoords="offset points", fontsize=9.5, color=NARANJA, ha="left",
                arrowprops=dict(arrowstyle="-", color=NARANJA, lw=0.8))

    ult = s.index[-1]
    var = (s["2025-07":].mean() / ref - 1) * 100
    ax.annotate("Últimos 12 meses:\n%.0f%% vs. 2019" % var, (ult, s[ult]),
                xytext=(-8, -78), textcoords="offset points", fontsize=9.5, color=NARANJA,
                fontweight="bold", ha="right",
                arrowprops=dict(arrowstyle="-", color=NARANJA, lw=0.8))

    ax.set_ylim(-40, 520)
    ax.set_xlim(ini, pd.Timestamp("2026-08-01"))
    ax.set_yticks([0, 100, 200, 300, 400, 500])
    ax.grid(axis="y", color=LINEA, lw=0.5)
    ax.tick_params(length=0, labelsize=9.5)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(LINEA)

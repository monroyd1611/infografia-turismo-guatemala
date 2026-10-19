"""Bloque 1. Titular estrategico y tarjetas de KPIs."""
import textwrap

from matplotlib.lines import Line2D

from estilo import AZUL, CAJAS, GRIS, LINEA, NARANJA, TEXTO

TITULAR = "Los vecinos aún no regresan"
SUBTITULAR = "17 años de flujo migratorio y el futuro del turismo en Guatemala, 2009-2026"


def calcular_kpis(series):
    total = series["Total"]
    anual = total.groupby(total.index.year).sum()
    base19 = total["2019"].mean()
    ult12 = total["2025-07":].mean()
    centro = series["America Del Centro"]
    norte = series["America Del Norte"]
    return {
        "viajeros_2019": anual[2019],
        "caida_2020": (anual[2020] / anual[2019] - 1) * 100,
        "brecha_actual": (ult12 / base19 - 1) * 100,
        "norte": (norte["2025-07":].mean() / norte["2019"].mean() - 1) * 100,
        "centro": (centro["2025-07":].mean() / centro["2019"].mean() - 1) * 100,
        "centro_pct": centro.sum() / total.sum() * 100,
    }


def dibujar(fig, series):
    k = calcular_kpis(series)
    x0, y0, w, h = CAJAS["titular"]
    fig.text(x0, y0 + h, TITULAR, fontsize=38, fontweight="bold", color=AZUL, va="top")
    fig.text(x0, y0 + 0.012, SUBTITULAR, fontsize=14.5, color=GRIS, va="bottom")

    x0, y0, w, h = CAJAS["kpis"]
    tarjetas = [
        ("%.2f M" % (k["viajeros_2019"] / 1e6), "viajeros en 2019, máximo antes de la pandemia", AZUL),
        ("%.1f%%" % k["caida_2020"], "caída de viajeros en 2020 frente a 2019", NARANJA),
        ("%.0f%%" % k["brecha_actual"], "brecha de los últimos 12 meses frente a 2019", NARANJA),
        ("+%.1f%%" % k["norte"], "Norteamérica ya supera su nivel de 2019", AZUL),
    ]
    ancho = w / 4
    for i, (num, txt, col) in enumerate(tarjetas):
        x = x0 + i * ancho + (0.012 if i else 0)
        fig.text(x, y0 + h, num, fontsize=36, fontweight="bold", color=col, va="top")
        fig.text(x, y0 + h - 0.040, textwrap.fill(txt, 28), fontsize=10, color=TEXTO, va="top", linespacing=1.3)
        if i:
            fig.add_artist(Line2D([x0 + i * ancho, x0 + i * ancho], [y0, y0 + h], color=LINEA, lw=0.8,
                                  transform=fig.transFigure))
    fig.add_artist(Line2D([x0, x0 + w], [y0 - 0.008, y0 - 0.008], color=LINEA, lw=0.8, transform=fig.transFigure))

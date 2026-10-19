"""Paleta, tipografia y cajas de cada bloque de la infografia (A3 vertical, 11x17 in)."""
import matplotlib as mpl
import matplotlib.pyplot as plt

AZUL = "#1F3A5F"
CELESTE = "#4A90C2"
GRIS = "#6B7280"
NARANJA = "#E8772E"
TEXTO = "#111827"
LINEA = "#D1D5DB"
FONDO = "#FFFFFF"

ANCHO, ALTO = 11, 17
DPI = 200
MARGEN = 0.05

# (x0, y0, ancho, alto) en fracciones de la figura; y crece hacia arriba
CAJAS = {
    "titular": (MARGEN, 0.915, 1 - 2 * MARGEN, 0.070),
    "kpis": (MARGEN, 0.835, 1 - 2 * MARGEN, 0.070),
    "b2": (MARGEN, 0.580, 1 - 2 * MARGEN, 0.240),
    "b3a": (MARGEN, 0.335, 0.43, 0.230),
    "b3b": (0.52, 0.335, 0.43, 0.230),
    "b4a": (MARGEN, 0.155, 0.43, 0.165),
    "b4b": (0.52, 0.155, 0.43, 0.165),
    "b5": (MARGEN, 0.018, 1 - 2 * MARGEN, 0.120),
}


def aplicar():
    mpl.rcParams.update({
        "font.family": ["Arial", "DejaVu Sans"],
        "font.size": 10,
        "text.color": TEXTO,
        "axes.edgecolor": LINEA,
        "axes.labelcolor": GRIS,
        "xtick.color": GRIS,
        "ytick.color": GRIS,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": FONDO,
        "axes.facecolor": FONDO,
        "pdf.fonttype": 42,
    })


def nueva_figura():
    aplicar()
    return plt.figure(figsize=(ANCHO, ALTO), dpi=DPI)


def ejes(fig, caja, **kw):
    return fig.add_axes(caja, **kw)


def titulo_bloque(fig, caja, texto, sub=None):
    """Titular del bloque (mensaje, no etiqueta) sobre la caja; devuelve el y libre."""
    x0, y0, w, h = caja
    fig.text(x0, y0 + h, texto, fontsize=15, fontweight="bold", color=AZUL, va="top", ha="left")
    if sub:
        fig.text(x0, y0 + h - 0.0195, sub, fontsize=10.5, color=GRIS, va="top", ha="left")

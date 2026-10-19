"""Ensambla la infografia completa y exporta PNG y PDF A3 vertical (11x17 in)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bloque1, bloque2, bloque3, bloque4, bloque5
from datos import cargar_series
from estilo import DPI, nueva_figura

SALIDA = Path(__file__).resolve().parent.parent / "entrega"


def main():
    te, series, train, test = cargar_series()
    fig = nueva_figura()
    bloque1.dibujar(fig, series)
    bloque2.dibujar(fig, series)
    bloque3.dibujar(fig, series, train, test)
    bloque4.dibujar(fig, series, train, test)
    bloque5.dibujar(fig, series, train, test)
    SALIDA.mkdir(exist_ok=True)
    fig.savefig(SALIDA / "infografia.png", dpi=DPI)
    fig.savefig(SALIDA / "infografia.pdf")


if __name__ == "__main__":
    main()

"""Carga de la base de migracion y construccion de las series del Laboratorio 1."""
from pathlib import Path

import numpy as np
import pandas as pd

RUTA = Path(__file__).resolve().parent.parent / "datos" / "Base_Migracion_2009-2026jun.xlsx"

IDX = pd.date_range("2009-01-01", "2026-06-01", freq="MS")
N_TRAIN = int(len(IDX) * 0.7)

NOMBRES = {
    "Total": "Total",
    "Aerea": "Vía aérea",
    "Terrestre": "Vía terrestre",
    "Maritima": "Vía marítima",
    "America Del Centro": "Centroamérica",
    "America Del Norte": "Norteamérica",
    "Europa": "Europa",
}


def cargar():
    df = pd.read_excel(RUTA, sheet_name="Datos")
    df["fecha"] = pd.to_datetime(dict(year=df["Año"], month=df["Mes cod"], day=1))
    return df


def turistas(df):
    """Turista + Excursionista, la base de todas las series del laboratorio."""
    return df[df["Tipo de Viajero"].isin(["Turista", "Excursionista"])]


def construir_series(te):
    def serie(mask=None):
        base = te if mask is None else te[mask]
        s = base.groupby("fecha")["Viajero"].sum().reindex(IDX).fillna(0)
        s.index.freq = "MS"
        return s

    return {
        "Total": serie(),
        "Aerea": serie(te["Vía"] == "Aérea"),
        "Terrestre": serie(te["Vía"] == "Terrestre"),
        "Maritima": serie(te["Vía"] == "Marítima"),
        "America Del Centro": serie(te["Región dos"] == "América Del Centro"),
        "America Del Norte": serie(te["Región dos"] == "América Del Norte"),
        "Europa": serie(te["Región dos"] == "Europa"),
    }


def cargar_series():
    te = turistas(cargar())
    series = construir_series(te)
    train = {k: v.iloc[:N_TRAIN] for k, v in series.items()}
    test = {k: v.iloc[N_TRAIN:] for k, v in series.items()}
    return te, series, train, test

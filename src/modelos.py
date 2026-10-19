"""Modelos de la serie Total del Laboratorio 1, evaluados en el conjunto de prueba."""
import hashlib
import logging
import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

CACHE = Path(__file__).resolve().parent.parent / "datos" / "modelos.pkl"

NOMBRES_MODELO = {
    "prophet": "Prophet",
    "holt": "Suavizamiento exponencial (Holt)",
    "snaive": "Seasonal naive",
    "arima": "ARIMA",
    "hw": "Holt-Winters",
}


def _prophet(tr, idx):
    from prophet import Prophet
    logging.getLogger("cmdstanpy").disabled = True
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False, interval_width=0.8)
    m.fit(pd.DataFrame({"ds": tr.index, "y": tr.values}))
    np.random.seed(0)
    f = m.predict(pd.DataFrame({"ds": idx})).set_index("ds")
    return f[["yhat", "yhat_lower", "yhat_upper"]].clip(lower=0)


def _pronosticos(tr, idx):
    h = len(idx)
    out = {}
    banda = _prophet(tr, idx)
    out["prophet"] = banda["yhat"].values
    out["holt"] = ExponentialSmoothing(tr, trend="add", initialization_method="estimated").fit().forecast(h).values
    out["snaive"] = np.tile(tr.values[-12:], h // 12 + 1)[:h]
    # SARIMA(0,1,0)(1,1,0,12) sobre log, sin restricciones de estacionariedad
    r = SARIMAX(np.log(tr), order=(0, 1, 0), seasonal_order=(1, 1, 0, 12),
                enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    out["arima"] = np.exp(r.forecast(h)).values
    out["hw"] = ExponentialSmoothing(tr, trend="add", seasonal="add", seasonal_periods=12,
                                     initialization_method="estimated").fit().forecast(h).values
    pred = pd.DataFrame({k: np.clip(v, 0, None) for k, v in out.items()}, index=idx)
    return pred, banda


def _huella(tr, ts):
    return hashlib.md5(pd.concat([tr, ts]).to_numpy().tobytes()).hexdigest()


def ajustar(train, test):
    """Devuelve (metricas, predicciones, banda Prophet 80%) para la serie Total."""
    tr, ts = train["Total"], test["Total"]
    huella = _huella(tr, ts)
    if CACHE.exists():
        with open(CACHE, "rb") as f:
            c = pickle.load(f)
        if c.get("huella") == huella:
            return c["metricas"], c["pred"], c["banda"]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pred, banda = _pronosticos(tr, ts.index)
    err = pred.sub(ts, axis=0)
    metricas = pd.DataFrame({"MAE": err.abs().mean(), "RMSE": np.sqrt((err ** 2).mean())}).sort_values("MAE")

    CACHE.parent.mkdir(exist_ok=True)
    with open(CACHE, "wb") as f:
        pickle.dump({"huella": huella, "metricas": metricas, "pred": pred, "banda": banda}, f)
    return metricas, pred, banda

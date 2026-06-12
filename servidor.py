# -*- coding: utf-8 -*-
"""Liquidador Oasis — backend FastAPI.

Sirve el frontend del Quick Design System (carpeta "Quick Design System/",
export de Claude Design, SIN modificar) y expone la API que lo alimenta:

    GET  /                      → frontend/index.html (PayrollScreen cableado)
    POST /api/procesar          → xlsx GeoVictoria → JSON (métricas, totales,
                                  conciliación, alertas) + token de descarga
    GET  /api/descargar/{token} → Oasis_Liquidacion_<periodo>.xlsx
    GET  /api/historial         → últimas ejecuciones (LogsOasis)

Uso local:
    .venv\\Scripts\\python.exe -m uvicorn servidor:app --port 8400 --app-dir liquidador_oasis
"""
from __future__ import annotations

import io
import json
import os
import re
import secrets as pysecrets
import tomllib
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

import logs_oasis
from procesador_geovictoria_oasis import (
    FACTORES,
    cargar_geovictoria,
    construir_filas_oasis,
    detectar_periodo,
    escribir_excel,
)

APP_VERSION = "2.0"
HERE = Path(__file__).parent
DS_DIR = HERE / "Quick Design System"
FRONT_DIR = HERE / "frontend"
SECRETS_PATH = HERE.parent / ".streamlit" / "secrets.toml"

app = FastAPI(title="Liquidador Oasis", version=APP_VERSION)

# Archivos generados en memoria: token -> (nombre, bytes). Cap LRU simple.
_DESCARGAS: OrderedDict[str, tuple[str, bytes]] = OrderedDict()
_DESCARGAS_MAX = 20


def co(v, dec=2):
    """Formato numérico colombiano: punto de miles, coma decimal."""
    s = f"{float(v):,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def _leer_secrets() -> dict | None:
    """Credenciales para LogsOasis.

    Orden: variables de entorno (GCP_SA_JSON + SHEET_ID — modo Hugging Face
    Spaces / Docker) y, si no existen, .streamlit/secrets.toml (modo local).
    """
    sa_json = os.environ.get("GCP_SA_JSON")
    sheet_id = os.environ.get("SHEET_ID")
    if sa_json and sheet_id:
        try:
            return {"gcp_service_account": json.loads(sa_json), "sheet_id": sheet_id}
        except Exception:
            pass
    try:
        with open(SECRETS_PATH, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return None


@app.post("/api/procesar")
async def procesar(archivo: UploadFile):
    if not (archivo.filename or "").lower().endswith(".xlsx"):
        raise HTTPException(400, "El archivo debe ser .xlsx (reporte GeoVictoria).")
    contenido = await archivo.read()
    try:
        df = cargar_geovictoria(io.BytesIO(contenido))
        odf = construir_filas_oasis(df)
        periodo = detectar_periodo(df)
    except Exception as exc:
        raise HTTPException(422, f"No se pudo procesar el archivo: {exc}")

    totales = {
        c: float(pd.to_numeric(odf[c], errors="coerce").fillna(0).sum()) if len(odf) else 0.0
        for c in ["RN", "RDF", "RNF", "HED", "HEN", "HEFD", "HEFN"]
    }
    hea_total = float(df["HEA_dec"].sum())
    he_oasis = totales["HED"] + totales["HEN"] + totales["HEFD"] + totales["HEFN"]
    diferencia = abs(hea_total - he_oasis)
    concilia_ok = diferencia < 0.01

    caso3 = df[(df["HEA_dec"] == 0) & (df["HEC_dec"] > 0)]
    he_dia = (
        df["HEDO_Dec"] + df["HENO_Dec"] + df["HEDD_Dec"]
        + df["HEND_Dec"] + df["HEDF_Dec"] + df["HENF_Dec"]
    )
    exceso_diario = df[he_dia > 2]
    marco = df["Entro1"].astype(str).str.match(r"\d{2}:\d{2}")
    sin_marca = df[(df["HEA_dec"] > 0) & (~marco)]
    ajustes = int(odf["_es_ajuste"].sum()) if len(odf) else 0
    empleados_pago = int(odf["IDENTIFICACION"].nunique()) if len(odf) else 0

    alertas = []
    if len(caso3):
        ej = " · ".join(
            f"{r['Apellidos']} {r['Nombres']} ({r['Fecha']}): {co(r['HEC_dec'])} h"
            for _, r in caso3.head(3).iterrows()
        )
        alertas.append({
            "text": f"Caso 3: HEC mayor a 0 sin HEA en {len(caso3)} filas — no se paga",
            "detail": f"{co(float(caso3['HEC_dec'].sum()))} h sin aprobar · {ej}"
                      + (f" · y {len(caso3) - 3} más" if len(caso3) > 3 else ""),
            "severity": "review",
        })
    if len(exceso_diario):
        alertas.append({
            "text": f"HE diaria supera 2 h en {len(exceso_diario)} registros",
            "detail": "Art. 22, Ley 50 de 1990",
            "severity": "review",
        })
    if len(sin_marca):
        alertas.append({
            "text": f"HEA aprobada sin marcación en {len(sin_marca)} filas",
            "detail": f"{co(float(sin_marca['HEA_dec'].sum()))} h aprobadas sin registro de entrada",
            "severity": "review",
        })

    # Excel en memoria + token de descarga
    buf = io.BytesIO()
    escribir_excel(odf, buf)
    periodo_slug = re.sub(r"[^0-9]", "-", f"{periodo[0]}_a_{periodo[1]}").strip("-")
    nombre_salida = f"Oasis_Liquidacion_{periodo_slug}.xlsx"
    token = pysecrets.token_urlsafe(12)
    _DESCARGAS[token] = (nombre_salida, buf.getvalue())
    while len(_DESCARGAS) > _DESCARGAS_MAX:
        _DESCARGAS.popitem(last=False)

    # Log best-effort en LogsOasis
    cfg = _leer_secrets()
    if cfg and cfg.get("gcp_service_account") and cfg.get("sheet_id"):
        try:
            logs_oasis.registrar(cfg["gcp_service_account"], cfg["sheet_id"], {
                "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "periodo": f"{periodo[0]} a {periodo[1]}",
                "archivo": archivo.filename,
                "filas_oasis": len(odf),
                "empleados_pago": empleados_pago,
                "total_horas": round(sum(totales.values()), 2),
                "hea_geo": round(hea_total, 2),
                "he_oasis": round(he_oasis, 2),
                "diferencia": round(diferencia, 4),
                "caso3_filas": len(caso3),
                "caso3_horas": round(float(caso3["HEC_dec"].sum()), 2),
                "version": APP_VERSION,
            })
        except Exception:
            pass

    total_h = sum(totales.values())
    total_eq = sum(totales[c] * FACTORES[c] for c in totales)
    return {
        "token": token,
        "archivo": archivo.filename,
        "procesado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "metricas": {
            "periodo_ini": periodo[0],
            "periodo_fin": periodo[1],
            "filas_geo": co(len(df), 0),
            "filas_oasis": co(len(odf), 0),
            "empleados_pago": empleados_pago,
            "empleados_total": int(df["Identificador"].nunique()),
            "ajustes": ajustes,
        },
        "conceptos": [
            {"concepto": c, "horas": co(totales[c]), "factor": co(FACTORES[c]), "equ": co(totales[c] * FACTORES[c])}
            for c in totales if totales[c] > 0
        ],
        "total": {"concepto": "Total liquidado", "horas": co(total_h), "factor": "—", "equ": co(total_eq)},
        "conciliacion": {
            "hea": co(hea_total),
            "he_oasis": co(he_oasis),
            "diferencia": co(diferencia, 4),
            "ok": concilia_ok,
            "n_alertas": len(alertas),
        },
        "alertas": alertas,
        "descarga": nombre_salida,
    }


@app.get("/api/descargar/{token}")
def descargar(token: str):
    item = _DESCARGAS.get(token)
    if not item:
        raise HTTPException(404, "Descarga no disponible — vuelve a procesar el archivo.")
    nombre, data = item
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'},
    )


@app.get("/api/historial")
def historial():
    cfg = _leer_secrets()
    if not (cfg and cfg.get("gcp_service_account") and cfg.get("sheet_id")):
        return {"items": []}
    try:
        rows = logs_oasis.leer(cfg["gcp_service_account"], cfg["sheet_id"], limit=6)
        items = [
            {
                "periodo": r.get("periodo", "—"),
                "empleados": str(r.get("empleados_pago", "—")),
                "total": f"{r.get('total_horas', '—')} h",
                "estado": "ok" if str(r.get("caso3_filas", "0")) in ("0", "") and float(r.get("diferencia", 0) or 0) < 0.01 else "review",
            }
            for r in rows
        ]
        return {"items": items}
    except Exception:
        return {"items": []}


@app.get("/")
def index():
    return FileResponse(FRONT_DIR / "index.html")


# Estáticos: el design system tal cual + el frontend cableado
app.mount("/ds", StaticFiles(directory=DS_DIR), name="ds")
app.mount("/frontend", StaticFiles(directory=FRONT_DIR), name="frontend")

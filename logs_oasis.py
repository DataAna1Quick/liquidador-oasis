# -*- coding: utf-8 -*-
"""Registro de ejecuciones del Liquidador en la pestaña LogsOasis (Google Sheets).

No importa streamlit: recibe las credenciales del service account como dict
para poder usarse también desde scripts o tests locales.
"""
from __future__ import annotations

from typing import Any

import gspread
from google.oauth2.service_account import Credentials

# El ID del spreadsheet llega por parámetro (en la app viene de st.secrets).
TAB = "LogsOasis"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADERS = [
    "fecha_ejecucion",
    "periodo",
    "archivo",
    "filas_oasis",
    "empleados_pago",
    "total_horas",
    "hea_geo",
    "he_oasis",
    "diferencia",
    "caso3_filas",
    "caso3_horas",
    "version",
]


def _worksheet(creds_info: dict, sheet_id: str) -> gspread.Worksheet:
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).worksheet(TAB)


def _asegurar_headers(ws: gspread.Worksheet) -> None:
    """Garantiza que la fila 1 tenga exactamente los HEADERS del Liquidador."""
    fila1 = ws.row_values(1)
    if fila1 != HEADERS:
        ws.update(values=[HEADERS], range_name="A1:L1")


def asegurar_headers(creds_info: dict, sheet_id: str) -> None:
    _asegurar_headers(_worksheet(creds_info, sheet_id))


def registrar(creds_info: dict, sheet_id: str, fila: dict[str, Any]) -> None:
    """Agrega una fila de ejecución. Las claves faltantes quedan vacías."""
    ws = _worksheet(creds_info, sheet_id)
    _asegurar_headers(ws)
    ws.append_row([str(fila.get(h, "")) for h in HEADERS], value_input_option="USER_ENTERED")


def leer(creds_info: dict, sheet_id: str, limit: int = 20) -> list[dict]:
    """Últimas `limit` ejecuciones, más reciente primero."""
    ws = _worksheet(creds_info, sheet_id)
    # expected_headers: la grilla puede tener columnas vacías a la derecha
    rows = ws.get_all_records(expected_headers=HEADERS)
    return list(reversed(rows[-limit:]))

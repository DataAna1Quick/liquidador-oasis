# -*- coding: utf-8 -*-
"""Smoke test local del pipeline Liquidador (sin Streamlit).

Genera un xlsx GeoVictoria sintético (51 columnas, header en fila 2) con los
4 escenarios de la matriz HEA x HEC, lo procesa y valida el resultado.
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd
from openpyxl import Workbook

from procesador_geovictoria_oasis import (
    GEOVICTORIA_COLS,
    cargar_geovictoria,
    construir_filas_oasis,
    detectar_periodo,
    escribir_excel,
)


def fila_base(**kw):
    base = {c: "" for c in GEOVICTORIA_COLS}
    base.update({
        "Apellidos": "PEREZ", "Nombres": "JUAN", "Identificador": "111",
        "Grupo": "2003 - 191 NESTLE COLOMBIA FM BOGOTA",
        "Fecha": "Lun 01-06-2026", "Turno": "08:00 - 17:00",
        "Entro1": "08:01", "Salio1": "19:30", "Cargo": "AUXILIAR",
    })
    base.update(kw)
    return base


filas = [
    # Escenario 1: HEA>0, HEC>0 con desglose (2h aprobadas, desglose 1.5 diurna + 0.5 nocturna)
    fila_base(HEA="02:00", HEC="02:00", HEDO_Dec="1,5", HENO_Dec="0,5"),
    # Escenario 2: HEA>0, HEC=0 (aprobada sin marcar) en festivo nocturno
    fila_base(Apellidos="GOMEZ", Nombres="ANA", Identificador="222",
              Fecha="Lun 29-06-2026", Turno="19:00 - 23:00", HEA="01:30", HEC="00:00"),
    # Escenario 3: HEC>0 sin HEA (NO se paga, se alerta)
    fila_base(Apellidos="DIAZ", Nombres="LUIS", Identificador="333",
              Fecha="Mar 02-06-2026", HEA="00:00", HEC="01:00", HEDO_Dec="1,0"),
    # Escenario 4: sin extras, con recargo nocturno
    fila_base(Apellidos="RIOS", Nombres="EVA", Identificador="444",
              Fecha="Mie 03-06-2026", Turno="19:00 - 06:00", RNO_Dec="2,0"),
    # Sin pago: no debe aparecer
    fila_base(Apellidos="SOTO", Nombres="MAX", Identificador="555",
              Fecha="Jue 04-06-2026"),
]

wb = Workbook()
ws = wb.active
ws.append([""] * len(GEOVICTORIA_COLS))      # fila 1 vacía
ws.append(GEOVICTORIA_COLS)                   # header en fila 2
for f in filas:
    ws.append([f[c] for c in GEOVICTORIA_COLS])
buf = io.BytesIO()
wb.save(buf)
buf.seek(0)

df = cargar_geovictoria(buf)
odf = construir_filas_oasis(df)
periodo = detectar_periodo(df)

print(f"Periodo: {periodo[0]} -> {periodo[1]}")
print(f"Filas Oasis: {len(odf)} (esperadas 3: esc.1, esc.2, esc.4)")
for _, r in odf.iterrows():
    pagos = {k: r[k] for k in ["RN", "RDF", "RNF", "HED", "HEN", "HEFD", "HEFN"] if pd.notna(r[k])}
    print(f"  {r['COLABORADOR']:12s} {r['FECHA']}  {pagos}  ciudad={r['CIUDAD']} cco={r['CODIGO CENTRO DE COSTO']}")

# Validaciones (Identificador puede venir como int por inferencia de pandas)
ids = odf["IDENTIFICACION"].astype(str)
assert len(odf) == 3, f"esperaba 3 filas, hay {len(odf)}"
r1 = odf[ids == "111"].iloc[0]
assert abs(r1["HED"] - 1.5) < 0.01 and abs(r1["HEN"] - 0.5) < 0.01, "esc.1 distribución proporcional"
r2 = odf[ids == "222"].iloc[0]
assert abs(r2["HEFN"] - 1.5) < 0.01, "esc.2 festivo nocturno (29-06 San Pedro) -> HEFN"
r4 = odf[ids == "444"].iloc[0]
assert abs(r4["RN"] - 2.0) < 0.01, "esc.4 recargo nocturno -> RN"
assert "333" not in set(ids), "esc.3 NO debe pagarse"

out = io.BytesIO()
escribir_excel(odf, out)
assert len(out.getvalue()) > 5000, "excel generado"
print("\nTODOS LOS ASSERTS OK — pipeline integro (carga, mapeo v6.0, excel en memoria)")

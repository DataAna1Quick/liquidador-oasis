# -*- coding: utf-8 -*-
"""Liquidador Oasis FM — Quick Help SAS.

Sube el reporte de asistencia de GeoVictoria (xlsx, 51 columnas) y descarga
el archivo de liquidación Oasis. Reglas operativas v6.0.
"""
import io
import re
from datetime import datetime

import pandas as pd
import streamlit as st

import logs_oasis
from procesador_geovictoria_oasis import (
    FACTORES,
    cargar_geovictoria,
    construir_filas_oasis,
    detectar_periodo,
    escribir_excel,
)

APP_VERSION = "1.0"
CONCEPTOS = ["RN", "RDF", "RNF", "HED", "HEN", "HEFD", "HEFN"]

st.set_page_config(page_title="Liquidador Oasis — Quick Help", page_icon="🧾", layout="centered")

st.title("🧾 Liquidador Oasis")
st.caption(
    "Sube el reporte de asistencia de GeoVictoria y descarga el formato de "
    "liquidación para Oasis. Reglas operativas v6.0."
)

archivo = st.file_uploader("Reporte GeoVictoria (.xlsx)", type=["xlsx"])

if archivo is not None:
    try:
        df = cargar_geovictoria(archivo)
    except Exception as exc:
        st.error(f"No se pudo procesar el archivo: {exc}")
        st.stop()

    odf = construir_filas_oasis(df)
    periodo = detectar_periodo(df)

    # ----- totales y conciliación -----
    totales = {
        c: float(pd.to_numeric(odf[c], errors="coerce").fillna(0).sum()) if len(odf) else 0.0
        for c in CONCEPTOS
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

    # ----- resumen -----
    st.subheader("📊 Resumen")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Periodo", f"{periodo[0]} → {periodo[1]}")
    c2.metric("Filas Oasis", len(odf))
    c3.metric(
        "Empleados con pago",
        f"{odf['IDENTIFICACION'].nunique() if len(odf) else 0} / {df['Identificador'].nunique()}",
    )
    c4.metric("Ajustes HEA>HEC", ajustes)

    tabla = pd.DataFrame(
        [
            {
                "Concepto": c,
                "Horas": round(totales[c], 2),
                "Factor": FACTORES[c],
                "Equivalente": round(totales[c] * FACTORES[c], 2),
            }
            for c in CONCEPTOS
            if totales[c] > 0
        ]
    )
    if len(tabla):
        st.dataframe(tabla, hide_index=True, use_container_width=True)

    if concilia_ok:
        st.success(
            f"🔍 Conciliación OK — HEA aprobadas: {hea_total:.2f} h · "
            f"HE en Oasis: {he_oasis:.2f} h · diferencia {diferencia:.4f} h"
        )
    else:
        st.warning(
            f"🔍 Revisar conciliación — HEA aprobadas: {hea_total:.2f} h · "
            f"HE en Oasis: {he_oasis:.2f} h · diferencia {diferencia:.2f} h"
        )

    # ----- alertas -----
    alertas = []
    if len(caso3):
        alertas.append(
            f"**Caso 3 (HEC>0 sin HEA — NO se paga):** {len(caso3)} filas, "
            f"{caso3['HEC_dec'].sum():.2f} h. Posible olvido del supervisor."
        )
    if len(exceso_diario):
        alertas.append(f"**Días con HE > 2 h** (Art. 22 Ley 50/1990): {len(exceso_diario)} casos.")
    if len(sin_marca):
        alertas.append(
            f"**HEA aprobada sin marcación:** {len(sin_marca)} filas, "
            f"{sin_marca['HEA_dec'].sum():.2f} h."
        )
    if alertas:
        with st.expander(f"⚠️ Alertas ({len(alertas)})", expanded=True):
            for a in alertas:
                st.markdown(f"- {a}")
            if len(caso3):
                st.markdown("**Detalle caso 3:**")
                detalle = caso3[["Apellidos", "Nombres", "Fecha", "HEC_dec"]].copy()
                detalle.columns = ["Apellidos", "Nombres", "Fecha", "HEC (h)"]
                st.dataframe(detalle.head(20), hide_index=True, use_container_width=True)

    # ----- descarga -----
    buf = io.BytesIO()
    escribir_excel(odf, buf)
    periodo_slug = re.sub(r"[^0-9]", "-", f"{periodo[0]}_a_{periodo[1]}").strip("-")
    nombre_salida = f"Oasis_Liquidacion_{periodo_slug}.xlsx"
    st.download_button(
        f"⬇️ Descargar {nombre_salida}",
        data=buf.getvalue(),
        file_name=nombre_salida,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )

    # ----- log en LogsOasis (una vez por archivo procesado) -----
    if "gcp_service_account" in st.secrets and st.secrets.get("sheet_id"):
        run_key = f"{archivo.name}|{periodo[0]}|{periodo[1]}|{len(odf)}"
        if st.session_state.get("logged_key") != run_key:
            try:
                logs_oasis.registrar(
                    dict(st.secrets["gcp_service_account"]),
                    st.secrets["sheet_id"],
                    {
                        "fecha_ejecucion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "periodo": f"{periodo[0]} a {periodo[1]}",
                        "archivo": archivo.name,
                        "filas_oasis": len(odf),
                        "empleados_pago": odf["IDENTIFICACION"].nunique() if len(odf) else 0,
                        "total_horas": round(sum(totales.values()), 2),
                        "hea_geo": round(hea_total, 2),
                        "he_oasis": round(he_oasis, 2),
                        "diferencia": round(diferencia, 4),
                        "caso3_filas": len(caso3),
                        "caso3_horas": round(float(caso3["HEC_dec"].sum()), 2),
                        "version": APP_VERSION,
                    },
                )
                st.session_state["logged_key"] = run_key
                st.caption("📝 Ejecución registrada en LogsOasis.")
            except Exception as exc:
                st.caption(f"⚠️ No se pudo registrar el log: {exc}")
    else:
        st.caption("ℹ️ Logs desactivados (sin credenciales configuradas).")

# ----- historial -----
if "gcp_service_account" in st.secrets and st.secrets.get("sheet_id"):
    with st.expander("📜 Historial de liquidaciones"):
        try:
            historial = logs_oasis.leer(dict(st.secrets["gcp_service_account"]), st.secrets["sheet_id"])
            if historial:
                st.dataframe(pd.DataFrame(historial), hide_index=True, use_container_width=True)
            else:
                st.write("Sin ejecuciones registradas todavía.")
        except Exception as exc:
            st.write(f"No se pudo leer el historial: {exc}")

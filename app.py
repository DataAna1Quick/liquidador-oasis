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

# Logo Quick estándar (SVG oficial del manual de identidad — no modificar)
QUICK_LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 250" role="img" aria-label="Quick">'
    '<circle cx="130" cy="125" r="62.5" fill="none" stroke="#FFFFFF" stroke-width="25"/>'
    '<circle cx="130" cy="125" r="50" fill="#000000"/>'
    '<polygon points="82,78 150,145 130,150 210,230 165,185 172,175" fill="#FDD402"/>'
    '<text x="215" y="190" font-family="Arial Black, Arial, sans-serif" font-weight="900" '
    'font-size="100" fill="#FFFFFF" stroke="#000000" stroke-width="14" stroke-linejoin="round" '
    'paint-order="stroke fill" letter-spacing="-3">uick</text>'
    "</svg>"
)

# Identidad corporativa Quick: solo #FDD402 / #000000 / #FFFFFF / #F5F5F5, Roboto + Arial
BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;700&display=swap');

html, body, .stApp, .stApp * { font-family: 'Roboto', Arial, sans-serif; }
.stApp { background: #FFFFFF; }
h1, h2, h3 { color: #000000; font-weight: 700; }

.quick-header {
  background: #000000; border-radius: 8px;
  padding: 18px 26px; margin-bottom: 6px;
  display: flex; align-items: center; gap: 22px;
}
.quick-header svg { height: 58px; width: auto; flex: 0 0 auto; }
.quick-header .qh-title { color: #FFFFFF; font-size: 1.6rem; font-weight: 700; margin: 0; line-height: 1.2; }
.quick-header .qh-sub { color: #FDD402; font-size: 0.85rem; font-weight: 300; margin: 4px 0 0; }

[data-testid="stMetric"] {
  background: #F5F5F5; border: 2px solid #000000; border-radius: 8px;
  padding: 10px 14px;
}
[data-testid="stMetricLabel"] { color: #000000; font-weight: 700; }
[data-testid="stMetricValue"] { color: #000000; }

[data-testid="stFileUploader"] section {
  background: #F5F5F5; border: 2px dashed #000000; border-radius: 8px;
}
[data-testid="stFileUploader"] section button {
  background: #FFFFFF; color: #000000; border: 2px solid #000000; font-weight: 700;
}

[data-testid="stDownloadButton"] button {
  background: #FDD402; color: #000000; border: 2px solid #000000;
  font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;
  border-radius: 4px;
}
[data-testid="stDownloadButton"] button:hover {
  background: #000000; color: #FDD402; border-color: #FDD402;
}

[data-testid="stExpander"] details {
  border: 2px solid #000000; border-radius: 8px; background: #FFFFFF;
}
[data-testid="stExpander"] summary { font-weight: 700; color: #000000; }

.quick-badge-ok, .quick-badge-warn {
  border-radius: 4px; padding: 12px 16px; font-weight: 700;
  margin: 8px 0 4px;
}
.quick-badge-ok   { background: #FDD402; color: #000000; border: 2px solid #000000; }
.quick-badge-warn { background: #000000; color: #FDD402; border: 2px solid #FDD402; }

[data-testid="stDataFrame"] { border: 2px solid #000000; border-radius: 8px; }
</style>
"""

st.set_page_config(page_title="Liquidador Oasis | Quick", page_icon="⚡", layout="centered")
st.markdown(BRAND_CSS, unsafe_allow_html=True)
st.markdown(
    f"""
<div class="quick-header">
  {QUICK_LOGO_SVG}
  <div>
    <p class="qh-title">Liquidador Oasis</p>
    <p class="qh-sub">GeoVictoria → Oasis · Reglas operativas v6.0 · v{APP_VERSION}</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
st.caption(
    "Sube el reporte de asistencia de GeoVictoria y descarga el formato de "
    "liquidación para Oasis."
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
        st.markdown(
            f'<div class="quick-badge-ok">✅ Conciliación OK — HEA aprobadas: {hea_total:.2f} h · '
            f"HE en Oasis: {he_oasis:.2f} h · diferencia {diferencia:.4f} h</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="quick-badge-warn">⚠️ Revisar conciliación — HEA aprobadas: {hea_total:.2f} h · '
            f"HE en Oasis: {he_oasis:.2f} h · diferencia {diferencia:.2f} h</div>",
            unsafe_allow_html=True,
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

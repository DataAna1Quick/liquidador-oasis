# -*- coding: utf-8 -*-
"""Liquidador Oasis FM — Quick Help SAS.

Sube el reporte de asistencia de GeoVictoria (xlsx, 51 columnas) y descarga
el archivo de liquidación Oasis. Reglas operativas v6.0.

Capa visual: Quick Design System (tokens y componentes del export de Claude
Design — paleta exclusiva, estatus sin color, cinta de seguridad, sin emojis).
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


def co(v, dec=2):
    """Formato numérico colombiano: punto de miles, coma decimal."""
    s = f"{float(v):,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


# Quick Design System — tokens y componentes (export Claude Design, adaptado a Streamlit)
BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;700&display=swap');

:root {
  /* Brand primitives */
  --quick-yellow: #FDD402; --quick-black: #000000;
  --quick-white: #FFFFFF;  --quick-grey: #F5F5F5;
  /* Derived neutrals (tintas de negro, no nuevos matices) */
  --ink-900: #000000; --ink-700: #2B2B2B; --ink-500: #5C5C5C; --ink-300: #9A9A9A;
  --line-200: #E4E4E4; --line-100: #EDEDED;
  --yellow-wash: #FFF7CC; --yellow-deep: #C9A800;
  /* Type */
  --font-sans: 'Roboto', Arial, Helvetica, sans-serif;
  --fs-display: 2.2rem; --fs-h2: 1.25rem; --fs-h3: 1rem;
  --fs-body: 0.9375rem; --fs-label: 0.8125rem; --fs-micro: 0.6875rem;
  --ls-overline: 0.14em;
  /* Shape & motion */
  --radius-sm: 4px; --radius-md: 6px; --radius-lg: 10px;
  --tape: repeating-linear-gradient(-45deg,
      var(--quick-black) 0, var(--quick-black) 12px,
      var(--quick-yellow) 12px, var(--quick-yellow) 24px);
  --ease: cubic-bezier(0.2, 0, 0, 1); --dur: 200ms;
}

html, body, .stApp, .stApp * { font-family: var(--font-sans); }
.stApp { background: var(--quick-grey); }
.block-container { max-width: 1080px; padding-top: 1.1rem; }
#MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }

/* ---- Overline / step labels ---- */
.q-step { display: flex; align-items: center; gap: 10px; margin: 4px 0 12px; }
.q-step .n {
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; border-radius: var(--radius-sm);
  background: var(--quick-black); color: var(--quick-yellow);
  font-size: 12px; font-weight: 700; flex: 0 0 auto;
}
.q-step .t {
  font-size: var(--fs-label); font-weight: 700; color: var(--ink-900);
  text-transform: uppercase; letter-spacing: 0.12em;
}

/* ---- Header + cinta ---- */
.quick-header {
  background: var(--quick-black); border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  padding: 18px 26px; display: flex; align-items: center; gap: 22px;
  animation: q-fade var(--dur) var(--ease) both;
}
.quick-header svg { height: 54px; width: auto; flex: 0 0 auto; }
.quick-header .qh-title { color: var(--quick-white); font-size: 1.55rem; font-weight: 700; margin: 0; line-height: 1.15; }
.quick-header .qh-sub {
  color: var(--ink-300); font-size: var(--fs-micro); font-weight: 400;
  letter-spacing: var(--ls-overline); text-transform: uppercase; margin: 5px 0 0;
}
.quick-header .qh-right { margin-left: auto; display: flex; align-items: center; gap: 12px; }
.quick-header .qh-avatar {
  width: 34px; height: 34px; border-radius: 50%; background: var(--quick-yellow);
  color: var(--quick-black); font-weight: 700; font-size: 13px;
  display: inline-flex; align-items: center; justify-content: center;
}
.quick-tape { height: 8px; background: var(--tape); margin-bottom: 1.6rem; }

/* ---- Dropzone ---- */
[data-testid="stFileUploader"] section {
  background: var(--quick-white); border: 2px dashed var(--ink-300);
  border-radius: var(--radius-lg); padding: 26px 22px;
  transition: border-color var(--dur) var(--ease);
}
[data-testid="stFileUploader"] section:hover { border-color: var(--ink-900); }
[data-testid="stFileUploader"] section button {
  background: var(--quick-white); color: var(--ink-900);
  border: 1px solid var(--ink-900); border-radius: var(--radius-sm); font-weight: 700;
}
[data-testid="stFileUploader"] section button:hover {
  background: var(--quick-yellow); color: var(--quick-black); border-color: var(--quick-black);
}

/* ---- Strip de archivo procesado ---- */
.q-strip {
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  margin-top: 10px; padding: 11px 16px;
  background: var(--quick-white); border: 1px solid var(--line-200); border-radius: var(--radius-md);
  font-size: var(--fs-label); color: var(--ink-500);
}
.q-strip b { color: var(--ink-900); font-weight: 700; }

/* ---- Métricas ---- */
.q-metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
@media (max-width: 760px) { .q-metrics { grid-template-columns: repeat(2, 1fr); } }
.q-tile {
  background: var(--quick-white); border: 1px solid var(--line-200);
  border-radius: var(--radius-md); padding: 14px 16px;
  animation: q-rise var(--dur) var(--ease) both;
}
.q-tile.accent { border-top: 3px solid var(--quick-yellow); }
.q-tile .l {
  font-size: var(--fs-micro); font-weight: 700; color: var(--ink-500);
  text-transform: uppercase; letter-spacing: var(--ls-overline);
}
.q-tile .v {
  font-size: clamp(1.25rem, 2.6vw, var(--fs-display)); font-weight: 300;
  color: var(--ink-900); line-height: 1.15; margin-top: 6px;
  font-variant-numeric: tabular-nums; letter-spacing: -0.01em;
}
.q-tile .h { font-size: var(--fs-micro); color: var(--ink-300); margin-top: 4px; }

/* ---- Cards ---- */
.q-card {
  background: var(--quick-white); border: 1px solid var(--line-200);
  border-radius: var(--radius-lg); overflow: hidden;
  animation: q-rise var(--dur) var(--ease) both;
}
.q-card.tape { border-top: 6px solid transparent; border-image: var(--tape) 6; border-radius: 0 0 var(--radius-lg) var(--radius-lg); }
.q-card .q-card-head {
  display: flex; align-items: baseline; justify-content: space-between; gap: 10px;
  padding: 14px 18px 10px;
}
.q-card .q-card-title { font-size: var(--fs-h3); font-weight: 700; color: var(--ink-900); }
.q-card .q-card-action { font-size: var(--fs-label); color: var(--ink-500); }
.q-card .q-card-body { padding: 4px 18px 16px; }

/* ---- Tabla de conceptos ---- */
.q-table { width: 100%; border-collapse: collapse; font-size: var(--fs-body); }
.q-table th {
  text-align: left; font-size: var(--fs-micro); font-weight: 700; color: var(--ink-500);
  text-transform: uppercase; letter-spacing: 0.12em;
  padding: 8px 6px; border-bottom: 1px solid var(--line-200);
}
.q-table th.num, .q-table td.num { text-align: right; font-variant-numeric: tabular-nums; }
.q-table td { padding: 9px 6px; border-bottom: 1px solid var(--line-100); color: var(--ink-700); }
.q-table tr.total td {
  border-top: 2px solid var(--ink-900); border-bottom: none;
  font-weight: 700; color: var(--ink-900);
}

/* ---- Badges de estado (sin color: forma + peso) ---- */
.q-badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: var(--fs-micro); font-weight: 700; letter-spacing: 0.06em;
  text-transform: uppercase; padding: 4px 10px; border-radius: var(--radius-sm);
  white-space: nowrap;
}
.q-badge.ok { background: var(--quick-black); color: var(--quick-white); }
.q-badge.review { background: var(--yellow-wash); color: var(--quick-black); border: 1px solid var(--quick-yellow); }

/* ---- Conciliación ---- */
.q-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 7px 0; }
.q-row .k { font-size: var(--fs-label); color: var(--ink-500); }
.q-div { height: 1px; background: var(--line-200); margin: 8px 0; }
.q-big { font-size: var(--fs-h2); font-weight: 300; color: var(--ink-900); font-variant-numeric: tabular-nums; }

/* ---- Alertas ---- */
.q-alert { display: flex; gap: 10px; padding: 9px 0; border-top: 1px solid var(--line-100); }
.q-alert:first-child { border-top: none; }
.q-alert .mark {
  flex: 0 0 auto; width: 20px; height: 20px; border-radius: var(--radius-sm);
  background: var(--yellow-wash); border: 1px solid var(--quick-yellow);
  color: var(--quick-black); font-weight: 700; font-size: 12px;
  display: inline-flex; align-items: center; justify-content: center;
}
.q-alert .tx { font-size: var(--fs-label); color: var(--ink-900); font-weight: 700; }
.q-alert .dt { font-size: var(--fs-micro); color: var(--ink-500); margin-top: 2px; font-weight: 400; }

/* ---- Expanders ---- */
[data-testid="stExpander"] details {
  border: 1px solid var(--line-200); border-radius: var(--radius-lg); background: var(--quick-white);
}
[data-testid="stExpander"] summary {
  font-weight: 700; color: var(--ink-900);
  text-transform: uppercase; letter-spacing: 0.08em; font-size: var(--fs-label);
}
[data-testid="stExpander"] summary:hover { background: var(--quick-grey); color: var(--ink-900); }

/* ---- Banda CTA de descarga ---- */
.st-key-cta_descarga {
  background: var(--quick-black); border-radius: var(--radius-lg);
  padding: 22px 24px; margin-top: 4px;
}
.st-key-cta_descarga .q-cta-title { color: var(--quick-white); font-size: var(--fs-h3); font-weight: 700; margin: 0; }
.st-key-cta_descarga .q-cta-sub { color: var(--ink-300); font-size: var(--fs-label); margin: 3px 0 12px; }
[data-testid="stDownloadButton"] { width: 100%; }
[data-testid="stDownloadButton"] button {
  width: 100%; background: var(--quick-yellow); color: var(--quick-black);
  border: none; border-radius: var(--radius-md);
  font-weight: 700; font-size: var(--fs-body);
  text-transform: uppercase; letter-spacing: 0.06em;
  padding: 0.85rem 1.2rem;
  transition: background var(--dur) var(--ease);
}
[data-testid="stDownloadButton"] button:hover { background: var(--yellow-deep); color: var(--quick-black); }
[data-testid="stDownloadButton"] button:focus-visible { outline: 3px solid var(--quick-white); outline-offset: 2px; }

/* ---- Mensajes nativos re-encuadrados a la paleta ---- */
[data-testid="stAlert"] {
  background: var(--yellow-wash); border: 1px solid var(--quick-yellow);
  border-radius: var(--radius-md); color: var(--ink-900);
}

/* ---- Footer ---- */
.quick-footer {
  margin-top: 2.4rem; padding: 14px 2px;
  border-top: 1px solid var(--line-200);
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;
  font-size: var(--fs-micro); color: var(--ink-500);
  letter-spacing: 0.08em; text-transform: uppercase;
}

@keyframes q-fade { from { opacity: 0; } to { opacity: 1; } }
@keyframes q-rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
@media (prefers-reduced-motion: reduce) {
  .stApp * { animation: none !important; transition: none !important; }
}
</style>
"""


def paso(n, texto):
    st.markdown(
        f'<div class="q-step"><span class="n">{n}</span><span class="t">{texto}</span></div>',
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="Liquidador Oasis | Quick", page_icon="⚡", layout="centered")
st.markdown(BRAND_CSS, unsafe_allow_html=True)
st.markdown(
    f"""
<div class="quick-header">
  {QUICK_LOGO_SVG}
  <div>
    <p class="qh-title">Liquidador Oasis</p>
    <p class="qh-sub">GeoVictoria → Oasis · Reglas v6.0</p>
  </div>
  <div class="qh-right">
    <span style="font-size:var(--fs-micro);color:var(--ink-300);letter-spacing:0.1em;text-transform:uppercase;">Dirección de Operaciones</span>
    <span class="qh-avatar">DO</span>
  </div>
</div>
<div class="quick-tape"></div>
""",
    unsafe_allow_html=True,
)

# ----- 1 · Carga -----
paso(1, "Cargar el reporte de asistencia")
archivo = st.file_uploader(
    "Reporte GeoVictoria (.xlsx)", type=["xlsx"], label_visibility="collapsed"
)

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
    empleados_pago = odf["IDENTIFICACION"].nunique() if len(odf) else 0

    st.markdown(
        f'<div class="q-strip"><span><b>{archivo.name}</b> · {len(df)} filas leídas · '
        f"{df['Identificador'].nunique()} empleados</span>"
        f"<span>Procesado {datetime.now().strftime('%d/%m/%Y %H:%M')}</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    # ----- 2 · Resumen -----
    paso(2, "Resumen del periodo")
    tile_aj = ' accent' if ajustes else ''
    st.markdown(
        f"""
<div class="q-metrics">
  <div class="q-tile"><div class="l">Periodo</div><div class="v">{periodo[0]}</div><div class="h">hasta {periodo[1]}</div></div>
  <div class="q-tile"><div class="l">Filas Oasis</div><div class="v">{co(len(odf), 0)}</div><div class="h">días con pago</div></div>
  <div class="q-tile"><div class="l">Empleados</div><div class="v">{empleados_pago} / {df['Identificador'].nunique()}</div><div class="h">con pago / total</div></div>
  <div class="q-tile{tile_aj}"><div class="l">Ajustes</div><div class="v">{ajustes}</div><div class="h">HEA &gt; HEC (filas verdes)</div></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    # ----- 3 · Totales + conciliación -----
    paso(3, "Totales y conciliación")
    col_t, col_c = st.columns([1.6, 1], gap="medium")

    with col_t:
        filas_html = "".join(
            f"<tr><td>{c}</td><td class='num'>{co(totales[c])}</td>"
            f"<td class='num'>{co(FACTORES[c])}</td>"
            f"<td class='num'>{co(totales[c] * FACTORES[c])}</td></tr>"
            for c in CONCEPTOS
            if totales[c] > 0
        ) or "<tr><td colspan='4'>Sin conceptos con pago en el periodo.</td></tr>"
        total_h = sum(v for v in totales.values())
        total_eq = sum(totales[c] * FACTORES[c] for c in CONCEPTOS)
        st.markdown(
            f"""
<div class="q-card tape">
  <div class="q-card-head">
    <span class="q-card-title">Totales por concepto</span>
    <span class="q-card-action">{periodo[0]} – {periodo[1]}</span>
  </div>
  <div class="q-card-body">
    <table class="q-table">
      <thead><tr><th>Concepto</th><th class="num">Horas</th><th class="num">Factor</th><th class="num">Equivalente</th></tr></thead>
      <tbody>{filas_html}
        <tr class="total"><td>Total</td><td class="num">{co(total_h)}</td><td class="num">—</td><td class="num">{co(total_eq)}</td></tr>
      </tbody>
    </table>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_c:
        badge_conc = (
            '<span class="q-badge ok">✓ Cuadra</span>'
            if concilia_ok
            else '<span class="q-badge review">! Revisar</span>'
        )
        n_alertas = (1 if len(caso3) else 0) + (1 if len(exceso_diario) else 0) + (1 if len(sin_marca) else 0)
        badge_alertas = (
            f'<span class="q-badge review">! {n_alertas}</span>'
            if n_alertas
            else '<span class="q-badge ok">✓ 0</span>'
        )
        st.markdown(
            f"""
<div class="q-card">
  <div class="q-card-head"><span class="q-card-title">Conciliación</span></div>
  <div class="q-card-body">
    <div class="q-row"><span class="k">HEA aprobadas (Geo)</span><span class="q-big">{co(hea_total)} h</span></div>
    <div class="q-row"><span class="k">HE en Oasis</span><span class="q-big">{co(he_oasis)} h</span></div>
    <div class="q-div"></div>
    <div class="q-row"><span class="k">Cobertura</span>{badge_conc}</div>
    <div class="q-row"><span class="k">Alertas</span>{badge_alertas}</div>
    <div class="q-div"></div>
    <div class="q-row"><span class="k">Diferencia</span><span class="q-big">{co(diferencia, 4)} h</span></div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ----- alertas -----
    alertas = []
    if len(caso3):
        alertas.append((
            f"Caso 3: HEC mayor a 0 sin HEA en {len(caso3)} filas — no se paga",
            f"{co(float(caso3['HEC_dec'].sum()))} h calculadas sin aprobar · posible olvido del supervisor",
        ))
    if len(exceso_diario):
        alertas.append((
            f"HE diaria supera 2 h en {len(exceso_diario)} registros",
            "Art. 22, Ley 50 de 1990",
        ))
    if len(sin_marca):
        alertas.append((
            f"HEA aprobada sin marcación en {len(sin_marca)} filas",
            f"{co(float(sin_marca['HEA_dec'].sum()))} h aprobadas sin registro de entrada",
        ))
    if alertas:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        with st.expander(f"Alertas · {len(alertas)}", expanded=True):
            items = "".join(
                f'<div class="q-alert"><span class="mark">!</span>'
                f'<div><div class="tx">{t}</div><div class="dt">{d}</div></div></div>'
                for t, d in alertas
            )
            st.markdown(items, unsafe_allow_html=True)
            if len(caso3):
                detalle = caso3[["Apellidos", "Nombres", "Fecha", "HEC_dec"]].copy()
                detalle.columns = ["Apellidos", "Nombres", "Fecha", "HEC (h)"]
                st.dataframe(detalle.head(20), hide_index=True, use_container_width=True)

    # ----- 4 · Descarga -----
    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)
    paso(4, "Exportar a Oasis")
    buf = io.BytesIO()
    escribir_excel(odf, buf)
    periodo_slug = re.sub(r"[^0-9]", "-", f"{periodo[0]}_a_{periodo[1]}").strip("-")
    nombre_salida = f"Oasis_Liquidacion_{periodo_slug}.xlsx"
    with st.container(key="cta_descarga"):
        st.markdown(
            f'<p class="q-cta-title">Liquidación lista para exportar</p>'
            f'<p class="q-cta-sub">{co(len(odf), 0)} filas · una por empleado y día con pago · '
            "ajustes HEA &gt; HEC marcados en verde</p>",
            unsafe_allow_html=True,
        )
        st.download_button(
            f"↓ Descargar {nombre_salida}",
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
                st.caption("Ejecución registrada en LogsOasis.")
            except Exception as exc:
                st.caption(f"No se pudo registrar el log: {exc}")
    else:
        st.caption("Logs desactivados (sin credenciales configuradas).")

# ----- historial -----
if "gcp_service_account" in st.secrets and st.secrets.get("sheet_id"):
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    with st.expander("Historial de liquidaciones"):
        try:
            historial = logs_oasis.leer(dict(st.secrets["gcp_service_account"]), st.secrets["sheet_id"])
            if historial:
                st.dataframe(pd.DataFrame(historial), hide_index=True, use_container_width=True)
            else:
                st.write("Sin ejecuciones registradas todavía.")
        except Exception as exc:
            st.write(f"No se pudo leer el historial: {exc}")

st.markdown(
    '<div class="quick-footer"><span>Herramienta interna de liquidación · Quick</span>'
    f"<span>v{APP_VERSION} · GeoVictoria → Oasis</span></div>",
    unsafe_allow_html=True,
)

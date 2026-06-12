# -*- coding: utf-8 -*-
"""Liquidador Oasis FM — Quick Help SAS.

Sube el reporte de asistencia de GeoVictoria (xlsx, 51 columnas) y descarga
el archivo de liquidación Oasis. Reglas operativas v6.0.

Arquitectura híbrida (hosting: Streamlit Cloud):
- Streamlit aloja la app y maneja la carga del archivo.
- Los resultados se renderizan con el Quick Design System REAL (export de
  Claude Design, carpeta "Quick Design System/"): tokens + bundle React
  incrustados vía components.html, con los datos inyectados como JSON y la
  descarga del Excel embebida como data URI en el Button del DS.
"""
import base64
import io
import json
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import logs_oasis
from procesador_geovictoria_oasis import (
    FACTORES,
    cargar_geovictoria,
    construir_filas_oasis,
    detectar_periodo,
    escribir_excel,
)

APP_VERSION = "2.1"
CONCEPTOS = ["RN", "RDF", "RNF", "HED", "HEN", "HEFD", "HEFN"]
DS_DIR = Path(__file__).parent / "Quick Design System"

# Logo Quick estándar (SVG oficial del manual — para el header nativo)
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


@st.cache_resource
def _ds_inline():
    """CSS de tokens + bundle del design system, listos para incrustar."""
    css = "\n".join(
        (DS_DIR / f).read_text(encoding="utf-8")
        for f in [
            "tokens/fonts.css",
            "tokens/colors.css",
            "tokens/typography.css",
            "tokens/spacing.css",
            "tokens/base.css",
        ]
    )
    bundle = (DS_DIR / "_ds_bundle.js").read_text(encoding="utf-8")
    return css, bundle


# CSS nativo mínimo: página, header, cinta, paso 1 y dropzone (lo único
# que NO vive dentro del iframe del design system).
BRAND_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;700&display=swap');
:root {
  --quick-yellow: #FDD402; --quick-black: #000000; --quick-white: #FFFFFF; --quick-grey: #F5F5F5;
  --ink-300: #9A9A9A; --ink-500: #5C5C5C; --ink-900: #000000;
  --line-200: #E4E4E4; --yellow-wash: #FFF7CC;
  --radius-sm: 4px; --radius-md: 6px; --radius-lg: 10px;
  --tape: repeating-linear-gradient(-45deg, #000 0, #000 12px, #FDD402 12px, #FDD402 24px);
}
html, body, .stApp, .stApp * { font-family: 'Roboto', Arial, Helvetica, sans-serif; }
.stApp { background: var(--quick-grey); }
.block-container { max-width: 1080px; padding-top: 1.1rem; }
#MainMenu, footer, header[data-testid="stHeader"] { display: none !important; }
::selection { background: var(--quick-yellow); color: var(--quick-black); }

.quick-header {
  background: var(--quick-black); border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  min-height: 64px; padding: 10px 32px; display: flex; align-items: center; gap: 16px;
}
.quick-header svg { height: 55px; width: auto; flex: 0 0 auto; display: block; }
.quick-header .qh-title { color: #FFF; font-size: 1.25rem; font-weight: 700; margin: 0; line-height: 1.15; }
.quick-header .qh-sub { color: var(--ink-300); font-size: 0.8125rem; font-weight: 300; margin: 1px 0 0; }
.quick-header .qh-sub .v { color: var(--quick-yellow); font-weight: 400; }
.quick-header .qh-right { margin-left: auto; display: flex; align-items: center; gap: 12px; }
.quick-header .qh-dept { font-size: 0.8125rem; color: var(--ink-300); }
.quick-header .qh-avatar {
  width: 34px; height: 34px; border-radius: 50%; background: var(--quick-yellow);
  color: #000; font-weight: 700; font-size: 14px;
  display: inline-flex; align-items: center; justify-content: center;
}
.quick-tape { height: 8px; background: var(--tape); background-size: 33.94px 33.94px; margin-bottom: 1.7rem; }

.q-step { display: flex; align-items: center; gap: 10px; margin: 4px 0 12px; }
.q-step .n {
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; border-radius: var(--radius-sm);
  background: #000; color: var(--quick-yellow); font-size: 12px; font-weight: 700;
}
.q-step .t { font-size: 0.8125rem; font-weight: 700; color: #000; text-transform: uppercase; letter-spacing: 0.12em; }

[data-testid="stFileUploaderDropzoneInstructions"] { display: none; }
[data-testid="stFileUploader"] section {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 12px; text-align: center; padding: 56px 24px;
  background: #FFF; border: 2px dashed var(--ink-300); border-radius: var(--radius-lg);
  transition: background 0.2s, border-color 0.2s;
}
[data-testid="stFileUploader"] section:hover { border-color: var(--quick-yellow); background: var(--yellow-wash); }
[data-testid="stFileUploader"] section::before {
  content: "↑"; display: inline-flex; align-items: center; justify-content: center;
  width: 56px; height: 56px; border-radius: var(--radius-md);
  background: #000; color: var(--quick-yellow); font-size: 26px; font-weight: 700; line-height: 1;
}
[data-testid="stFileUploader"] section::after {
  content: "Arrastra el reporte de GeoVictoria o haz clic para seleccionar";
  font-size: 1rem; font-weight: 700; color: #000;
}
[data-testid="stFileUploader"] section button {
  background: #FFF; color: #000; border: 1px solid #000; border-radius: var(--radius-md);
  font-weight: 700; padding: 6px 14px; order: 2;
}
[data-testid="stFileUploader"] section button:hover { background: var(--quick-yellow); border-color: #000; color: #000; }

.q-strip {
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  margin-top: 12px; padding: 12px 16px;
  background: #FFF; border: 1px solid var(--line-200); border-radius: var(--radius-md);
  font-size: 0.8125rem; color: var(--ink-500);
}
.q-strip b { color: #000; font-weight: 700; }

[data-testid="stAlert"] { background: var(--yellow-wash); border: 1px solid var(--quick-yellow); border-radius: var(--radius-md); color: #000; }

.quick-footer {
  margin-top: 2rem; padding: 16px 2px; border-top: 1px solid var(--line-200);
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;
}
.quick-footer .fl { font-size: 0.8125rem; color: var(--ink-500); }
.quick-footer .fr { font-size: 0.6875rem; color: var(--ink-300); }
</style>
"""

# Pantalla de resultados: el PayrollScreen del design system (secciones 2-5),
# alimentado con DATA. Corre DENTRO del iframe con el bundle real del DS.
RESULTS_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8" />
<style>__CSS__
body { margin: 0; background: var(--quick-grey); }
</style>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" crossorigin="anonymous"></script>
<script>__BUNDLE__</script>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const DATA = __DATA__;

function SectionLabel({ children, step }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, margin: '0 0 12px' }}>
      {step && (
        <span style={{
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
          width: 22, height: 22, borderRadius: 'var(--radius-sm)',
          background: 'var(--quick-black)', color: 'var(--quick-yellow)',
          fontSize: 12, fontWeight: 700, flex: '0 0 auto',
        }}>{step}</span>
      )}
      <span className="q-overline" style={{ fontSize: 'var(--fs-label)', letterSpacing: '0.12em' }}>{children}</span>
    </div>
  );
}

function ResultScreen() {
  const { MetricTile, Card, Badge, DataTable, AlertPanel, Expander, Button } =
    window.QuickDesignSystem_adff9f;
  const m = DATA.metricas;
  const conc = DATA.conciliacion;
  return (
    <div style={{ width: '100%', maxWidth: 'var(--page-max)', margin: '0 auto' }}>

      <section style={{ marginBottom: 'var(--space-6)' }}>
        <SectionLabel step="2">Resumen del periodo</SectionLabel>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-4)' }}>
          <MetricTile label="Periodo" value={m.periodo_ini} hint={'hasta ' + m.periodo_fin} />
          <MetricTile label="Filas Oasis" value={m.filas_oasis} hint="días con pago" />
          <MetricTile label="Empleados" value={m.empleados_pago + ' / ' + m.empleados_total} hint="con pago / total" />
          <MetricTile label="Ajustes" value={String(m.ajustes)} accent={m.ajustes > 0} hint="HEA > HEC (filas verdes)" />
        </div>
      </section>

      <section style={{ marginBottom: 'var(--space-6)', display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: 'var(--space-5)', alignItems: 'start' }}>
        <Card tape padded={false}
          title="Totales por concepto"
          action={<span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>{m.periodo_ini} – {m.periodo_fin}</span>}>
          <DataTable
            columns={[
              { key: 'concepto', label: 'CONCEPTO' },
              { key: 'horas', label: 'HORAS', align: 'right', width: '110px' },
              { key: 'factor', label: 'FACTOR', align: 'right', width: '90px' },
              { key: 'equ', label: 'EQUIVALENTE', align: 'right', width: '150px' },
            ]}
            rows={DATA.conceptos}
            totals={DATA.total}
          />
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          <Card title="Conciliación">
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>HEA aprobadas (Geo)</span>
                <span style={{ fontSize: 'var(--fs-h2)', fontWeight: 'var(--fw-light)', fontVariantNumeric: 'tabular-nums' }}>{conc.hea} h</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>HE en Oasis</span>
                <span style={{ fontSize: 'var(--fs-h2)', fontWeight: 'var(--fw-light)', fontVariantNumeric: 'tabular-nums' }}>{conc.he_oasis} h</span>
              </div>
              <div style={{ height: 1, background: 'var(--line-200)' }} />
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>Cobertura</span>
                {conc.ok ? <Badge status="ok">Cuadra</Badge> : <Badge status="review">Revisar</Badge>}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>Topes y novedades</span>
                {conc.n_alertas ? <Badge status="review">Revisar · {conc.n_alertas}</Badge> : <Badge status="ok">Sin alertas</Badge>}
              </div>
              <div style={{ height: 1, background: 'var(--line-200)' }} />
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>Diferencia</span>
                <span style={{ fontSize: 'var(--fs-h2)', fontWeight: 'var(--fw-light)', fontVariantNumeric: 'tabular-nums' }}>{conc.diferencia} h</span>
              </div>
            </div>
          </Card>

          <AlertPanel title="Alertas" items={DATA.alertas} defaultOpen={true} />
        </div>
      </section>

      <section style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16,
        padding: 'var(--space-5)', background: 'var(--quick-black)', borderRadius: 'var(--radius-lg)',
        marginBottom: 'var(--space-6)',
      }}>
        <div>
          <div style={{ color: 'var(--quick-white)', fontSize: 'var(--fs-h3)', fontWeight: 'var(--fw-bold)' }}>
            Liquidación lista para exportar
          </div>
          <div style={{ color: 'var(--ink-300)', fontSize: 'var(--fs-label)', marginTop: 2 }}>
            {m.filas_oasis} filas · una por empleado y día con pago · ajustes HEA &gt; HEC en verde.
          </div>
        </div>
        <a href={DATA.xlsx} download={DATA.nombre} style={{ textDecoration: 'none' }}>
          <Button variant="primary" size="lg"
            iconLeft={<span aria-hidden="true" style={{ fontSize: 16 }}>↓</span>}>
            Descargar Excel
          </Button>
        </a>
      </section>

      {DATA.historial.length > 0 && (
        <section>
          <Expander title="Historial de liquidaciones" subtitle="Últimos periodos procesados" defaultOpen={false}>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              {DATA.historial.map((h, i) => (
                <div key={i} style={{
                  display: 'grid', gridTemplateColumns: '1.4fr 1fr 1fr auto', alignItems: 'center', gap: 12,
                  padding: '12px 4px', borderTop: i === 0 ? 'none' : '1px solid var(--line-100)',
                }}>
                  <span style={{ fontWeight: 'var(--fw-bold)', color: 'var(--text-strong)', fontSize: 'var(--fs-body)' }}>{h.periodo}</span>
                  <span style={{ color: 'var(--text-muted)', fontSize: 'var(--fs-label)' }}>{h.empleados} empleados</span>
                  <span style={{ color: 'var(--text-body)', fontVariantNumeric: 'tabular-nums', fontSize: 'var(--fs-body)' }}>{h.total}</span>
                  <span style={{ justifySelf: 'end' }}>
                    {h.estado === 'ok' ? <Badge status="ok">Conciliado</Badge> : <Badge status="review">Con ajustes</Badge>}
                  </span>
                </div>
              ))}
            </div>
          </Expander>
        </section>
      )}
    </div>
  );
}

(function mount() {
  if (window.QuickDesignSystem_adff9f && window.ReactDOM) {
    ReactDOM.createRoot(document.getElementById('root')).render(<ResultScreen />);
  } else {
    setTimeout(mount, 30);
  }
})();
</script>
</body>
</html>"""


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
    <p class="qh-sub">Herramienta interna · <span class="v">v{APP_VERSION}</span> · GeoVictoria → Oasis</p>
  </div>
  <div class="qh-right">
    <span class="qh-dept">Dirección de Operaciones</span>
    <span class="qh-avatar">DO</span>
  </div>
</div>
<div class="quick-tape"></div>
""",
    unsafe_allow_html=True,
)

# ----- 1 · Carga (Streamlit nativo, estilizado como el FileDropzone del DS) -----
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
    empleados_pago = int(odf["IDENTIFICACION"].nunique()) if len(odf) else 0

    st.markdown(
        f'<div class="q-strip"><span><b>{archivo.name}</b> · {co(len(df), 0)} filas leídas · '
        f"{df['Identificador'].nunique()} empleados</span>"
        f"<span>Procesado {datetime.now().strftime('%d/%m/%Y %H:%M')}</span></div>",
        unsafe_allow_html=True,
    )

    # ----- alertas -----
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

    # ----- Excel embebido como data URI (lo descarga el Button del DS) -----
    buf = io.BytesIO()
    escribir_excel(odf, buf)
    periodo_slug = re.sub(r"[^0-9]", "-", f"{periodo[0]}_a_{periodo[1]}").strip("-")
    nombre_salida = f"Oasis_Liquidacion_{periodo_slug}.xlsx"
    xlsx_b64 = base64.b64encode(buf.getvalue()).decode()
    xlsx_uri = (
        "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,"
        + xlsx_b64
    )

    # ----- historial (se inyecta al iframe) -----
    historial = []
    if "gcp_service_account" in st.secrets and st.secrets.get("sheet_id"):
        try:
            rows = logs_oasis.leer(dict(st.secrets["gcp_service_account"]), st.secrets["sheet_id"], limit=6)
            historial = [
                {
                    "periodo": r.get("periodo", "—"),
                    "empleados": str(r.get("empleados_pago", "—")),
                    "total": f"{r.get('total_horas', '—')} h",
                    "estado": "ok"
                    if str(r.get("caso3_filas", "0")) in ("0", "")
                    and float(r.get("diferencia", 0) or 0) < 0.01
                    else "review",
                }
                for r in rows
            ]
        except Exception:
            historial = []

    total_h = sum(totales.values())
    total_eq = sum(totales[c] * FACTORES[c] for c in CONCEPTOS)
    data = {
        "metricas": {
            "periodo_ini": periodo[0],
            "periodo_fin": periodo[1],
            "filas_oasis": co(len(odf), 0),
            "empleados_pago": empleados_pago,
            "empleados_total": int(df["Identificador"].nunique()),
            "ajustes": ajustes,
        },
        "conceptos": [
            {"concepto": c, "horas": co(totales[c]), "factor": co(FACTORES[c]), "equ": co(totales[c] * FACTORES[c])}
            for c in CONCEPTOS if totales[c] > 0
        ],
        "total": {"concepto": "Total liquidado", "horas": co(total_h), "factor": "—", "equ": co(total_eq)},
        "conciliacion": {
            "hea": co(hea_total), "he_oasis": co(he_oasis),
            "diferencia": co(diferencia, 4), "ok": concilia_ok, "n_alertas": len(alertas),
        },
        "alertas": alertas,
        "historial": historial,
        "xlsx": xlsx_uri,
        "nombre": nombre_salida,
    }

    # ----- render con el design system real -----
    css, bundle = _ds_inline()
    html = (
        RESULTS_HTML
        .replace("__CSS__", css)
        .replace("__BUNDLE__", bundle)
        .replace("__DATA__", json.dumps(data, ensure_ascii=False))
    )
    n_conceptos = len(data["conceptos"]) + 1
    alto_tabla = 220 + n_conceptos * 46
    alto_conc = 460 + sum(90 if a.get("detail") else 64 for a in alertas)
    alto = 240 + max(alto_tabla, alto_conc) + 150 + (90 if historial else 0) + 60
    components.html(html, height=alto, scrolling=False)

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
                        "empleados_pago": empleados_pago,
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
    st.markdown(
        '<p style="color:#5C5C5C;font-size:0.8125rem;text-align:center;margin-top:40px;">'
        "Carga el reporte de asistencia para ver el resumen de liquidación.</p>",
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="quick-footer"><span class="fl">Herramienta interna de liquidación · Quick</span>'
    f'<span class="fr">v{APP_VERSION} · GeoVictoria → Oasis</span></div>',
    unsafe_allow_html=True,
)

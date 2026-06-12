/* PayrollScreen — Liquidador Oasis con datos REALES.
   Misma composición del template del Quick Design System
   (templates/liquidacion/PayrollScreen.jsx); lo único que cambia es la
   fuente de datos: la API del backend (servidor.py) en vez de constantes. */

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

function PayrollScreen() {
  const { Header, FileDropzone, MetricTile, Card, Badge, DataTable, AlertPanel, Expander, Button } =
    window.QuickDesignSystem_adff9f;

  const [data, setData] = React.useState(null);
  const [fileName, setFileName] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const [hist, setHist] = React.useState([]);

  React.useEffect(() => {
    fetch('/api/historial').then(r => r.json()).then(j => setHist(j.items || [])).catch(() => {});
  }, [data]);

  const procesar = async (f) => {
    if (!f) return;
    setLoading(true); setError(''); setFileName(f.name);
    try {
      const fd = new FormData();
      fd.append('archivo', f);
      const r = await fetch('/api/procesar', { method: 'POST', body: fd });
      const j = await r.json();
      if (!r.ok) throw new Error(j.detail || 'Error procesando el archivo');
      setData(j);
    } catch (e) {
      setError(String(e.message || e));
      setData(null);
    }
    setLoading(false);
  };

  const reset = () => { setData(null); setFileName(null); setError(''); };
  const processed = !!data;
  const m = data ? data.metricas : null;
  const conc = data ? data.conciliacion : null;

  return (
    <div style={{ minHeight: '100vh', background: 'var(--surface-page)', display: 'flex', flexDirection: 'column' }}>
      <Header
        logoSrc="/ds/assets/quick-logo-inverse.png"
        title="Liquidador Oasis"
        version="v2.0"
        right={
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <span style={{ fontSize: 'var(--fs-label)', color: 'var(--ink-300)' }}>Dirección de Operaciones</span>
            <span style={{
              width: 34, height: 34, borderRadius: '50%', background: 'var(--quick-yellow)',
              color: 'var(--quick-black)', fontWeight: 700, fontSize: 14,
              display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
            }}>DO</span>
          </div>
        }
      />
      <div className="q-tape" />

      <main style={{ width: '100%', maxWidth: 'var(--page-max)', margin: '0 auto', padding: 'var(--space-6) var(--space-5) var(--space-7)', flex: 1 }}>

        {/* 1 · Carga */}
        <section style={{ marginBottom: 'var(--space-6)' }}>
          <SectionLabel step="1">Cargar el reporte de asistencia</SectionLabel>
          <FileDropzone
            accept=".xlsx"
            hint="Arrastra el reporte de GeoVictoria o haz clic para seleccionar"
            fileName={fileName}
            onFile={procesar}
          />
          {loading && (
            <div style={{
              marginTop: 12, padding: '12px 16px', background: 'var(--surface-wash)',
              border: '1px solid var(--quick-yellow)', borderRadius: 'var(--radius-md)',
              fontSize: 'var(--fs-label)', color: 'var(--text-strong)', fontWeight: 700,
            }}>
              Procesando {fileName}…
            </div>
          )}
          {error && (
            <div style={{
              marginTop: 12, padding: '12px 16px', background: 'var(--surface-wash)',
              border: '1px solid var(--quick-yellow)', borderRadius: 'var(--radius-md)',
              fontSize: 'var(--fs-label)', color: 'var(--text-strong)',
            }}>
              <b>!</b> {error}
            </div>
          )}
          {processed && !loading && (
            <div style={{
              display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12,
              marginTop: 12, padding: '12px 16px', background: 'var(--quick-white)',
              border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)',
            }}>
              <span style={{ fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>
                Procesado el {data.procesado} · {m.filas_geo} filas leídas · {m.empleados_total} empleados
              </span>
              <Button variant="ghost" size="sm" onClick={reset}>Cambiar archivo</Button>
            </div>
          )}
        </section>

        {!processed && !loading && (
          <p style={{ color: 'var(--text-muted)', fontSize: 'var(--fs-label)', textAlign: 'center', marginTop: 40 }}>
            Carga el reporte de asistencia para ver el resumen de liquidación.
          </p>
        )}

        {processed && (
          <>
            {/* 2 · Métricas */}
            <section style={{ marginBottom: 'var(--space-6)' }}>
              <SectionLabel step="2">Resumen del periodo</SectionLabel>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-4)' }}>
                <MetricTile label="Periodo" value={m.periodo_ini} hint={`hasta ${m.periodo_fin}`} />
                <MetricTile label="Filas Oasis" value={m.filas_oasis} hint="días con pago" />
                <MetricTile label="Empleados" value={`${m.empleados_pago} / ${m.empleados_total}`} hint="con pago / total" />
                <MetricTile label="Ajustes" value={String(m.ajustes)} accent={m.ajustes > 0} hint="HEA > HEC (filas verdes)" />
              </div>
            </section>

            {/* 3 · Totales + conciliación */}
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
                  rows={data.conceptos}
                  totals={data.total}
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

                <AlertPanel title="Alertas" items={data.alertas} defaultOpen={true} />
              </div>
            </section>

            {/* 4 · CTA descarga */}
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
              <Button variant="primary" size="lg"
                iconLeft={<span aria-hidden="true" style={{ fontSize: 16 }}>↓</span>}
                onClick={() => { window.location.href = `/api/descargar/${data.token}`; }}>
                Descargar Excel
              </Button>
            </section>
          </>
        )}

        {/* 5 · Historial */}
        {hist.length > 0 && (
          <section>
            <Expander title="Historial de liquidaciones" subtitle="Últimos periodos procesados" defaultOpen={false}>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                {hist.map((h, i) => (
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
      </main>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--border-default)', background: 'var(--quick-white)' }}>
        <div style={{
          maxWidth: 'var(--page-max)', margin: '0 auto', padding: '18px var(--space-5)',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 10,
        }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 10, fontSize: 'var(--fs-label)', color: 'var(--text-muted)' }}>
            <img src="/ds/assets/quick-logo.png" alt="Quick" style={{ height: 22 }} />
            Herramienta interna de liquidación · Quick
          </span>
          <span style={{ fontSize: 'var(--fs-micro)', color: 'var(--text-subtle)' }}>v2.0 · GeoVictoria → Oasis</span>
        </div>
      </footer>
    </div>
  );
}

(function mount() {
  if (window.QuickDesignSystem_adff9f && window.ReactDOM) {
    ReactDOM.createRoot(document.getElementById('root')).render(<PayrollScreen />);
  } else {
    setTimeout(mount, 30);
  }
})();

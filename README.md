# Liquidador Oasis

Aplicación Streamlit que convierte el reporte de asistencia de GeoVictoria
(xlsx, 51 columnas) al formato de carga del sistema Oasis (xlsx, 24 columnas),
aplicando reglas de liquidación de horas extras y recargos (Colombia).

## Uso

1. Abrir la app.
2. Subir el archivo `GestióndeAsistencia...xlsx`.
3. Revisar resumen, conciliación y alertas.
4. Descargar `Oasis_Liquidacion_<periodo>.xlsx`.

## Ejecución local

```bash
pip install -r requirements.txt
streamlit run app.py
```

También funciona por línea de comandos sin Streamlit:

```bash
python procesador_geovictoria_oasis.py entrada.xlsx -o salida.xlsx
```

## Configuración (opcional — registro de ejecuciones)

Sin configuración la app funciona completa, solo que no registra logs.
Para activar el registro en Google Sheets, definir en
`.streamlit/secrets.toml` (o en los Secrets de Streamlit Cloud):

```toml
sheet_id = "<ID del spreadsheet>"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
# ... resto del JSON del service account
```

El spreadsheet debe tener una pestaña `LogsOasis` y estar compartido como
Editor con el `client_email` del service account.

## Test

```bash
python _test_pipeline.py
```

Genera un archivo de entrada sintético con los 4 escenarios de la matriz
HEA × HEC y valida la distribución de horas, las exclusiones y el Excel.

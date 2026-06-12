---
title: Liquidador Oasis
emoji: ⚡
colorFrom: yellow
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Liquidador Oasis

Herramienta web que convierte el reporte de asistencia de GeoVictoria
(xlsx, 51 columnas) al formato de carga del sistema Oasis (xlsx, 24 columnas),
aplicando reglas de liquidación de horas extras y recargos (Colombia).

Frontend: **Quick Design System** (React, export de Claude Design) servido
tal cual. Backend: **FastAPI** + procesador de reglas v6.0.

## Uso

1. Abrir la app.
2. Arrastrar el archivo `GestióndeAsistencia...xlsx`.
3. Revisar resumen, totales, conciliación y alertas.
4. Descargar `Oasis_Liquidacion_<periodo>.xlsx`.

## Ejecución local

```bash
pip install -r requirements.txt
uvicorn servidor:app --port 8400
# abrir http://localhost:8400
```

El procesador también funciona por línea de comandos sin servidor:

```bash
python procesador_geovictoria_oasis.py entrada.xlsx -o salida.xlsx
```

## Despliegue (Hugging Face Spaces · Docker)

Este repo está listo para un Space tipo Docker: el front-matter de este
README configura el Space y el `Dockerfile` arranca uvicorn en el puerto 7860.

Registro de ejecuciones (opcional): definir en los **Secrets** del Space

| Variable | Contenido |
|---|---|
| `GCP_SA_JSON` | JSON completo del service account de Google (una línea) |
| `SHEET_ID` | ID del spreadsheet con la pestaña `LogsOasis` |

Sin estas variables la app funciona completa, solo que no registra historial.

## Estructura

| Ruta | Rol |
|---|---|
| `servidor.py` | API FastAPI + servido de estáticos |
| `frontend/` | Pantalla (React vía Babel) cableada a la API |
| `Quick Design System/` | Tokens, bundle de componentes y logos |
| `procesador_geovictoria_oasis.py` | Reglas de liquidación v6.0 |
| `logs_oasis.py` | Registro de ejecuciones en Google Sheets |
| `_test_pipeline.py` | Smoke test del pipeline (4 escenarios HEA × HEC) |

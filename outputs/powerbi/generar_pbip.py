"""
Genera proyecto PBIP (Power BI Project) — compatible Power BI May 2026 (v2.154+)
Formato moderno basado en carpetas JSON, no ZIP binario.
"""
import json, shutil, uuid
from pathlib import Path

BASE  = Path(r"C:\Users\mpere\Documents\hse-oilgas-predictive-analytics\outputs\powerbi")
PBIP  = BASE / "HSE_Dashboard_PBIP"
EXCEL = r"C:\Users\mpere\Documents\hse-oilgas-predictive-analytics\outputs\powerbi\HSE_PowerBI_Ready.xlsx"

# Limpiar y crear
if PBIP.exists():
    shutil.rmtree(PBIP)
PBIP.mkdir(parents=True)

def w(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding='utf-8')

def wraw(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding='utf-8')

# ── helpers para visual JSON (Enhanced Report Format) ──────────────────────

def proj_measure(table, measure):
    return {"field": {"Measure": {"Expression": {"SourceRef": {"Entity": table}}, "Property": measure}},
            "queryRef": f"{table}.{measure}"}

def proj_column(table, col):
    return {"field": {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": col}},
            "queryRef": f"{table}.{col}"}

def visual_card(name, x, y, w, h, table, measure, z=2000, tab=0):
    return {
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab},
        "visual": {
            "visualType": "card",
            "query": {"queryState": {"Values": {"projections": [proj_measure(table, measure)]}}},
            "objects": {
                "labels": [{"properties": {
                    "fontSize": {"expr": {"Literal": {"Value": "26D"}}},
                    "bold": {"expr": {"Literal": {"Value": "true L"}}}
                }}]
            }
        }
    }

def visual_bar(name, x, y, w, h, table, cat_col, measure, horizontal=True, z=2000, tab=0):
    vtype = "barChart" if horizontal else "columnChart"
    return {
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab},
        "visual": {
            "visualType": vtype,
            "query": {"queryState": {
                "Category": {"projections": [proj_column(table, cat_col)]},
                "Y": {"projections": [proj_measure(table, measure)]}
            }},
            "objects": {}
        }
    }

def visual_line(name, x, y, w, h, table, x_col, measures, z=2000, tab=0):
    return {
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab},
        "visual": {
            "visualType": "lineChart",
            "query": {"queryState": {
                "Category": {"projections": [proj_column(table, x_col)]},
                "Y": {"projections": [proj_measure(table, m) for m in measures]}
            }},
            "objects": {}
        }
    }

def visual_text(name, x, y, w, h, text, font_size=18, bold=True, color="#1B4F72", z=500, tab=0):
    return {
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab},
        "visual": {
            "visualType": "textbox",
            "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [{
                "value": text,
                "textStyle": {
                    "fontFamily": "Segoe UI",
                    "fontSize": f"{font_size}pt",
                    "bold": bold,
                    "color": {"solid": {"color": color}}
                }
            }], "horizontalTextAlignment": "left"}]}}]}
        }
    }

# ── 1. Archivo principal .pbip ──────────────────────────────────────────────
w(PBIP / "HSE_Dashboard.pbip", {
    "version": "1.0",
    "artifacts": [{"report": {"path": "HSE_Dashboard.Report"}}],
    "settings": {"enableAutoRecovery": True}
})

# ── 2. Semantic Model ───────────────────────────────────────────────────────
SEM = PBIP / "HSE_Dashboard.SemanticModel"
SEM.mkdir()
(SEM / ".pbi").mkdir()
w(SEM / ".pbi" / "localSettings.json", {"version": "1.0"})

# definition.pbism — requerido por Power BI May 2026 con PBI_tmdlInDataset
w(SEM / "definition.pbism", {"version": "4.0", "settings": {}})

def m_expr(sheet):
    return [
        "let",
        f'    Source = Excel.Workbook(File.Contents("{EXCEL}"), null, true),',
        f'    Hoja = Source{{[Item="{sheet}",Kind="Sheet"]}}[Data],',
        f'    Headers = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true])',
        "in",
        "    Headers"
    ]

model_bim = {
    "name": "SemanticModel",
    "compatibilityLevel": 1567,
    "model": {
        "culture": "es-AR",
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "es-AR",
        "tables": [
            {
                "name": "KPIs_Mensuales",
                "columns": [
                    {"name": "fecha",               "dataType": "dateTime", "sourceColumn": "fecha"},
                    {"name": "mes",                 "dataType": "int64",    "sourceColumn": "mes"},
                    {"name": "anio",                "dataType": "int64",    "sourceColumn": "anio"},
                    {"name": "trimestre",           "dataType": "string",   "sourceColumn": "trimestre"},
                    {"name": "horas_hombre",        "dataType": "int64",    "sourceColumn": "horas_hombre"},
                    {"name": "near_misses",         "dataType": "int64",    "sourceColumn": "near_misses"},
                    {"name": "registrables",        "dataType": "int64",    "sourceColumn": "registrables"},
                    {"name": "lti",                 "dataType": "int64",    "sourceColumn": "lti"},
                    {"name": "dias_perdidos",       "dataType": "int64",    "sourceColumn": "dias_perdidos"},
                    {"name": "dias_ausencia_total", "dataType": "int64",    "sourceColumn": "dias_ausencia_total"},
                    {"name": "tasa_ausentismo_pct", "dataType": "double",   "sourceColumn": "tasa_ausentismo_pct"},
                    {"name": "ltifr",               "dataType": "double",   "sourceColumn": "ltifr"},
                    {"name": "trifr",               "dataType": "double",   "sourceColumn": "trifr"},
                    {"name": "ratio_nm_a_lti",      "dataType": "double",   "sourceColumn": "ratio_nm_a_lti"},
                ],
                "measures": [
                    {"name": "LTIFR Promedio",      "expression": "AVERAGE(KPIs_Mensuales[ltifr])",               "formatString": "0.00"},
                    {"name": "TRIFR Promedio",      "expression": "AVERAGE(KPIs_Mensuales[trifr])",               "formatString": "0.00"},
                    {"name": "Tasa Ausentismo %",   "expression": "AVERAGE(KPIs_Mensuales[tasa_ausentismo_pct])", "formatString": "0.00"},
                    {"name": "Total LTI",           "expression": "SUM(KPIs_Mensuales[lti])",                     "formatString": "0"},
                    {"name": "Total Near Misses",   "expression": "SUM(KPIs_Mensuales[near_misses])",             "formatString": "0"},
                    {"name": "Total Dias Perdidos", "expression": "SUM(KPIs_Mensuales[dias_perdidos])",           "formatString": "0"},
                    {"name": "Ratio NM LTI",        "expression": "DIVIDE(SUM(KPIs_Mensuales[near_misses]),SUM(KPIs_Mensuales[lti]),0)", "formatString": "0.0"},
                    {"name": "Estado LTIFR",        "expression": 'IF(AVERAGE(KPIs_Mensuales[ltifr])<=1.5,"CLASE MUNDIAL",IF(AVERAGE(KPIs_Mensuales[ltifr])<=5,"EN MEJORA","REQUIERE ACCION"))', "formatString": ""},
                ],
                "partitions": [{"name": "KPIs_Mensuales", "source": {"type": "m", "expression": m_expr("KPIs_Mensuales")}}]
            },
            {
                "name": "Empleados",
                "columns": [
                    {"name": "empleado_id",         "dataType": "int64",  "sourceColumn": "empleado_id"},
                    {"name": "departamento",        "dataType": "string", "sourceColumn": "departamento"},
                    {"name": "cargo",               "dataType": "string", "sourceColumn": "cargo"},
                    {"name": "edad",                "dataType": "int64",  "sourceColumn": "edad"},
                    {"name": "antiguedad_anios",    "dataType": "int64",  "sourceColumn": "antiguedad_anios"},
                    {"name": "turno",               "dataType": "string", "sourceColumn": "turno"},
                    {"name": "ubicacion",           "dataType": "string", "sourceColumn": "ubicacion"},
                    {"name": "capacitacion_hs_a",   "dataType": "int64",  "sourceColumn": "capacitacion_hs_año"},
                    {"name": "condicion_cronica",   "dataType": "string", "sourceColumn": "condicion_cronica"},
                    {"name": "riesgo_score",        "dataType": "double", "sourceColumn": "riesgo_score"},
                    {"name": "categoria_riesgo",    "dataType": "string", "sourceColumn": "categoria_riesgo"},
                ],
                "measures": [
                    {"name": "Total Empleados",       "expression": "COUNTROWS(Empleados)",                                                                          "formatString": "0"},
                    {"name": "Empleados Riesgo Alto", "expression": 'CALCULATE(COUNTROWS(Empleados),Empleados[categoria_riesgo]="Alto")',                            "formatString": "0"},
                    {"name": "% Riesgo Alto",         "expression": 'DIVIDE(CALCULATE(COUNTROWS(Empleados),Empleados[categoria_riesgo]="Alto"),COUNTROWS(Empleados),0)', "formatString": "0.0%"},
                    {"name": "Score Riesgo Prom",     "expression": "AVERAGE(Empleados[riesgo_score])",                                                              "formatString": "0.00"},
                    {"name": "Horas Cap Promedio",    "expression": "AVERAGE(Empleados[capacitacion_hs_a])",                                                         "formatString": "0"},
                ],
                "partitions": [{"name": "Empleados", "source": {"type": "m", "expression": m_expr("Empleados")}}]
            },
            {
                "name": "Incidentes",
                "columns": [
                    {"name": "empleado_id",    "dataType": "int64",    "sourceColumn": "empleado_id"},
                    {"name": "departamento",   "dataType": "string",   "sourceColumn": "departamento"},
                    {"name": "turno",          "dataType": "string",   "sourceColumn": "turno"},
                    {"name": "tipo_incidente", "dataType": "string",   "sourceColumn": "tipo_incidente"},
                    {"name": "gravedad",       "dataType": "int64",    "sourceColumn": "gravedad"},
                    {"name": "causa_raiz",     "dataType": "string",   "sourceColumn": "causa_raiz"},
                    {"name": "area",           "dataType": "string",   "sourceColumn": "area"},
                    {"name": "fecha",          "dataType": "dateTime", "sourceColumn": "fecha"},
                    {"name": "hora",           "dataType": "int64",    "sourceColumn": "hora"},
                    {"name": "anio",           "dataType": "int64",    "sourceColumn": "anio"},
                    {"name": "dias_perdidos",  "dataType": "int64",    "sourceColumn": "dias_perdidos"},
                    {"name": "es_registrable", "dataType": "int64",    "sourceColumn": "es_registrable"},
                    {"name": "es_lti",         "dataType": "int64",    "sourceColumn": "es_lti"},
                ],
                "measures": [
                    {"name": "Total Incidentes",        "expression": "COUNTROWS(Incidentes)",              "formatString": "0"},
                    {"name": "Incidentes Registrables", "expression": "SUM(Incidentes[es_registrable])",    "formatString": "0"},
                    {"name": "Total LTI Inc",           "expression": "SUM(Incidentes[es_lti])",            "formatString": "0"},
                    {"name": "Dias Perdidos Inc",       "expression": "SUM(Incidentes[dias_perdidos])",     "formatString": "0"},
                ],
                "partitions": [{"name": "Incidentes", "source": {"type": "m", "expression": m_expr("Incidentes")}}]
            },
            {
                "name": "Ausentismo",
                "columns": [
                    {"name": "empleado_id",   "dataType": "int64",    "sourceColumn": "empleado_id"},
                    {"name": "departamento",  "dataType": "string",   "sourceColumn": "departamento"},
                    {"name": "turno",         "dataType": "string",   "sourceColumn": "turno"},
                    {"name": "causa",         "dataType": "string",   "sourceColumn": "causa"},
                    {"name": "fecha_inicio",  "dataType": "dateTime", "sourceColumn": "fecha_inicio"},
                    {"name": "dias_ausencia", "dataType": "int64",    "sourceColumn": "dias_ausencia"},
                    {"name": "anio",          "dataType": "int64",    "sourceColumn": "anio"},
                    {"name": "es_accidente",  "dataType": "int64",    "sourceColumn": "es_accidente"},
                ],
                "measures": [
                    {"name": "Total Dias Ausencia",  "expression": "SUM(Ausentismo[dias_ausencia])",                                                           "formatString": "0"},
                    {"name": "Total Ausencias",      "expression": "COUNTROWS(Ausentismo)",                                                                    "formatString": "0"},
                    {"name": "Prom Dias Evento",     "expression": "AVERAGE(Ausentismo[dias_ausencia])",                                                       "formatString": "0.0"},
                    {"name": "% Origen Laboral",     "expression": "DIVIDE(CALCULATE(SUM(Ausentismo[dias_ausencia]),Ausentismo[es_accidente]=1),SUM(Ausentismo[dias_ausencia]),0)", "formatString": "0.0%"},
                ],
                "partitions": [{"name": "Ausentismo", "source": {"type": "m", "expression": m_expr("Ausentismo")}}]
            },
        ],
        "relationships": [
            {"name": "Emp_Inc", "fromTable": "Incidentes", "fromColumn": "empleado_id", "toTable": "Empleados", "toColumn": "empleado_id"},
            {"name": "Emp_Aus", "fromTable": "Ausentismo", "fromColumn": "empleado_id", "toTable": "Empleados", "toColumn": "empleado_id"},
        ],
        "annotations": [
            {"name": "PBIDesktopVersion", "value": "2.154.1260.0"},
            {"name": "PBI_QueryOrder",    "value": json.dumps(["KPIs_Mensuales","Empleados","Incidentes","Ausentismo"])},
        ]
    }
}

w(SEM / "model.bim", model_bim)

# ── 3. Report definition ────────────────────────────────────────────────────
REP = PBIP / "HSE_Dashboard.Report"
REP.mkdir()
w(REP / "definition.pbir", {
    "version": "4.0",
    "datasetReference": {"byPath": {"path": "../HSE_Dashboard.SemanticModel"}}
})

# ── 4. Páginas ──────────────────────────────────────────────────────────────
G = 14    # gap
CW, CH = 270, 100  # card width/height
W, H   = 1280, 720

pages = [
    # ── Página 1: Dashboard Ejecutivo ──────────────────────────────────────
    {
        "meta": {"name": "Page1", "displayName": "Dashboard Ejecutivo", "ordinal": 0, "width": W, "height": H},
        "visuals": [
            visual_text("titulo",    0, 0, W, 55, "YPF-Patagonia S.A. — Dashboard HSE  |  2022–2024", 18, True, "#1B4F72"),
            visual_text("subtitulo", 0, 52, W, 28, "Health, Safety & Environment Analytics  |  Cuenca Neuquina, Argentina", 10, False, "#4A4E69"),

            visual_card("kpi1", G,              90, CW, CH, "KPIs_Mensuales", "LTIFR Promedio",     tab=1),
            visual_card("kpi2", G*2+CW,         90, CW, CH, "KPIs_Mensuales", "TRIFR Promedio",     tab=2),
            visual_card("kpi3", G*3+CW*2,       90, CW, CH, "KPIs_Mensuales", "Tasa Ausentismo %",  tab=3),
            visual_card("kpi4", G*4+CW*3,       90, CW, CH, "Empleados",      "Empleados Riesgo Alto", tab=4),

            visual_line("lineas",   G,        205, 615, 255, "KPIs_Mensuales", "fecha", ["LTIFR Promedio","TRIFR Promedio"], tab=5),
            visual_bar("aus_bar",   G*2+615,  205, 605, 255, "KPIs_Mensuales", "fecha",        "Tasa Ausentismo %",   horizontal=False, tab=6),
            visual_bar("inc_dep",   G,        475, 615, 220, "Incidentes",     "departamento", "Total Incidentes",    tab=7),
            visual_bar("aus_causa", G*2+615,  475, 605, 220, "Ausentismo",     "causa",        "Total Dias Ausencia", tab=8),
        ]
    },
    # ── Página 2: Análisis de Incidentes ───────────────────────────────────
    {
        "meta": {"name": "Page2", "displayName": "Analisis de Incidentes", "ordinal": 1, "width": W, "height": H},
        "visuals": [
            visual_text("tit2", 0, 0, W, 50, "Análisis de Incidentes — YPF-Patagonia | 2022–2024", 16, True, "#1B4F72"),

            visual_card("k21", G,         60, 280, 90, "Incidentes", "Total Incidentes",        tab=1),
            visual_card("k22", G*2+280,   60, 280, 90, "Incidentes", "Incidentes Registrables", tab=2),
            visual_card("k23", G*3+560,   60, 280, 90, "Incidentes", "Total LTI Inc",            tab=3),
            visual_card("k24", G*4+840,   60, 280, 90, "Incidentes", "Dias Perdidos Inc",        tab=4),

            visual_bar("tipo",      G,        165, 615, 250, "Incidentes", "tipo_incidente", "Total Incidentes",    tab=5),
            visual_bar("causa",     G*2+615,  165, 610, 250, "Incidentes", "causa_raiz",     "Total Incidentes",    tab=6),
            visual_bar("area",      G,        430, 615, 255, "Incidentes", "area",           "Total Incidentes",    tab=7),
            visual_bar("turno_inc", G*2+615,  430, 610, 255, "Incidentes", "turno",          "Incidentes Registrables", tab=8),
        ]
    },
    # ── Página 3: Análisis de Ausentismo ───────────────────────────────────
    {
        "meta": {"name": "Page3", "displayName": "Analisis de Ausentismo", "ordinal": 2, "width": W, "height": H},
        "visuals": [
            visual_text("tit3", 0, 0, W, 50, "Análisis de Ausentismo — YPF-Patagonia | 2022–2024", 16, True, "#1B4F72"),

            visual_card("k31", G,         60, 270, 90, "Ausentismo", "Total Dias Ausencia",  tab=1),
            visual_card("k32", G*2+270,   60, 270, 90, "Ausentismo", "Total Ausencias",      tab=2),
            visual_card("k33", G*3+540,   60, 270, 90, "Ausentismo", "Prom Dias Evento",     tab=3),
            visual_card("k34", G*4+810,   60, 270, 90, "Ausentismo", "% Origen Laboral",     tab=4),

            visual_bar("aus_cau",   G,        165, 615, 255, "Ausentismo", "causa",         "Total Dias Ausencia", tab=5),
            visual_bar("aus_dep",   G*2+615,  165, 610, 255, "Ausentismo", "departamento",  "Total Dias Ausencia", tab=6),
            visual_bar("aus_anio",  G,        435, 615, 250, "Ausentismo", "anio",           "Total Dias Ausencia", horizontal=False, tab=7),
            visual_bar("aus_turn",  G*2+615,  435, 610, 250, "Ausentismo", "turno",          "Total Dias Ausencia", tab=8),
        ]
    },
    # ── Página 4: Perfil de Riesgo ─────────────────────────────────────────
    {
        "meta": {"name": "Page4", "displayName": "Perfil de Riesgo", "ordinal": 3, "width": W, "height": H},
        "visuals": [
            visual_text("tit4", 0, 0, W, 50, "Perfil de Riesgo Individual — Modelo GBM Classifier", 16, True, "#1B4F72"),

            visual_card("k41", G,         60, 270, 90, "Empleados", "Total Empleados",        tab=1),
            visual_card("k42", G*2+270,   60, 270, 90, "Empleados", "Empleados Riesgo Alto",  tab=2),
            visual_card("k43", G*3+540,   60, 270, 90, "Empleados", "% Riesgo Alto",          tab=3),
            visual_card("k44", G*4+810,   60, 270, 90, "Empleados", "Score Riesgo Prom",      tab=4),

            visual_bar("risg_dep",  G,        165, 615, 255, "Empleados", "departamento",     "Empleados Riesgo Alto", tab=5),
            visual_bar("risg_turn", G*2+615,  165, 610, 255, "Empleados", "turno",            "Empleados Riesgo Alto", tab=6),
            visual_bar("risg_ubic", G,        435, 615, 255, "Empleados", "ubicacion",        "Score Riesgo Prom",     tab=7),
            visual_bar("risg_cat",  G*2+615,  435, 610, 255, "Empleados", "categoria_riesgo", "Total Empleados",       tab=8),
        ]
    },
]

# Escribir páginas y visuales
PAGES = REP / "pages"
PAGES.mkdir()
for page in pages:
    pdir = PAGES / page["meta"]["name"]
    pdir.mkdir()
    w(pdir / "page.json", page["meta"])
    vdir = pdir / "visuals"
    vdir.mkdir()
    for vis in page["visuals"]:
        vname = vis["name"]
        vpath = vdir / vname
        vpath.mkdir()
        w(vpath / "visual.json", vis)

# ── 5. Resumen ──────────────────────────────────────────────────────────────
total_vis = sum(len(p["visuals"]) for p in pages)
all_files = list(PBIP.rglob("*"))
total_files = len([f for f in all_files if f.is_file()])

print(f"Proyecto PBIP generado:")
print(f"  Carpeta: {PBIP}")
print(f"  Archivo a abrir: HSE_Dashboard.pbip")
print(f"  Paginas: {len(pages)}")
print(f"  Visuales: {total_vis}")
print(f"  Archivos JSON: {total_files}")
print(f"  Medidas DAX: 23")
print()
print("Para abrir: doble clic en")
print(f"  {PBIP / 'HSE_Dashboard.pbip'}")

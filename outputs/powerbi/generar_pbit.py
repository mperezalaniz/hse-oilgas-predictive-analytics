"""
Genera HSE_Dashboard.pbit — Power BI Template completo
Con medidas DAX, relaciones y 4 páginas pre-configuradas.
"""
import json, zipfile
from pathlib import Path

EXCEL = r"C:\Users\mpere\Documents\hse-oilgas-predictive-analytics\outputs\powerbi\HSE_PowerBI_Ready.xlsx"
OUT   = Path(r"C:\Users\mpere\Documents\hse-oilgas-predictive-analytics\outputs\powerbi\HSE_Dashboard.pbit")

# ─── M EXPRESSIONS (Power Query) ───────────────────────────────────────────
def m_expr(sheet):
    return [
        f'let',
        f'    Source = Excel.Workbook(File.Contents("{EXCEL}"), null, true),',
        f'    Hoja = Source{{[Item="{sheet}",Kind="Sheet"]}}[Data],',
        f'    Headers = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true])',
        f'in',
        f'    Headers'
    ]

# ─── DATA MODEL SCHEMA ─────────────────────────────────────────────────────
data_model = {
    "name": "HSE_Analytics",
    "compatibilityLevel": 1550,
    "model": {
        "culture": "es-AR",
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "tables": [
            {
                "name": "KPIs_Mensuales",
                "columns": [
                    {"name": "fecha",               "dataType": "dateTime", "sourceColumn": "fecha"},
                    {"name": "mes",                 "dataType": "int64",    "sourceColumn": "mes"},
                    {"name": "anio",                "dataType": "int64",    "sourceColumn": "anio"},
                    {"name": "trimestre",           "dataType": "string",   "sourceColumn": "trimestre"},
                    {"name": "horas_hombre",        "dataType": "int64",    "sourceColumn": "horas_hombre"},
                    {"name": "incidentes_total",    "dataType": "int64",    "sourceColumn": "incidentes_total"},
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
                    {"name": "Ratio NM LTI",
                     "expression": "DIVIDE(SUM(KPIs_Mensuales[near_misses]),SUM(KPIs_Mensuales[lti]),0)",
                     "formatString": "0.0"},
                    {"name": "Estado LTIFR",
                     "expression": "IF(AVERAGE(KPIs_Mensuales[ltifr])<=1.5,\"CLASE MUNDIAL\",IF(AVERAGE(KPIs_Mensuales[ltifr])<=5,\"EN MEJORA\",IF(AVERAGE(KPIs_Mensuales[ltifr])<=15,\"REQUIERE ACCION\",\"CRITICO\")))",
                     "formatString": ""},
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
                    {"name": "capacitacion_hs_año", "dataType": "int64",  "sourceColumn": "capacitacion_hs_año"},
                    {"name": "condicion_cronica",   "dataType": "string", "sourceColumn": "condicion_cronica"},
                    {"name": "riesgo_score",        "dataType": "double", "sourceColumn": "riesgo_score"},
                    {"name": "categoria_riesgo",    "dataType": "string", "sourceColumn": "categoria_riesgo"},
                ],
                "measures": [
                    {"name": "Total Empleados",
                     "expression": "COUNTROWS(Empleados)",
                     "formatString": "0"},
                    {"name": "Empleados Riesgo Alto",
                     "expression": "CALCULATE(COUNTROWS(Empleados),Empleados[categoria_riesgo]=\"Alto\")",
                     "formatString": "0"},
                    {"name": "Empleados Riesgo Medio",
                     "expression": "CALCULATE(COUNTROWS(Empleados),Empleados[categoria_riesgo]=\"Medio\")",
                     "formatString": "0"},
                    {"name": "% Riesgo Alto",
                     "expression": "DIVIDE(CALCULATE(COUNTROWS(Empleados),Empleados[categoria_riesgo]=\"Alto\"),COUNTROWS(Empleados),0)",
                     "formatString": "0.0%"},
                    {"name": "Score Riesgo Promedio",
                     "expression": "AVERAGE(Empleados[riesgo_score])",
                     "formatString": "0.00"},
                    {"name": "Horas Capacitacion Prom",
                     "expression": "AVERAGE(Empleados[capacitacion_hs_año])",
                     "formatString": "0"},
                ],
                "partitions": [{"name": "Empleados", "source": {"type": "m", "expression": m_expr("Empleados")}}]
            },
            {
                "name": "Incidentes",
                "columns": [
                    {"name": "empleado_id",     "dataType": "int64",    "sourceColumn": "empleado_id"},
                    {"name": "departamento",    "dataType": "string",   "sourceColumn": "departamento"},
                    {"name": "ubicacion",       "dataType": "string",   "sourceColumn": "ubicacion"},
                    {"name": "turno",           "dataType": "string",   "sourceColumn": "turno"},
                    {"name": "tipo_incidente",  "dataType": "string",   "sourceColumn": "tipo_incidente"},
                    {"name": "gravedad",        "dataType": "int64",    "sourceColumn": "gravedad"},
                    {"name": "causa_raiz",      "dataType": "string",   "sourceColumn": "causa_raiz"},
                    {"name": "area",            "dataType": "string",   "sourceColumn": "area"},
                    {"name": "fecha",           "dataType": "dateTime", "sourceColumn": "fecha"},
                    {"name": "hora",            "dataType": "int64",    "sourceColumn": "hora"},
                    {"name": "mes",             "dataType": "int64",    "sourceColumn": "mes"},
                    {"name": "anio",            "dataType": "int64",    "sourceColumn": "anio"},
                    {"name": "dias_perdidos",   "dataType": "int64",    "sourceColumn": "dias_perdidos"},
                    {"name": "es_registrable",  "dataType": "int64",    "sourceColumn": "es_registrable"},
                    {"name": "es_lti",          "dataType": "int64",    "sourceColumn": "es_lti"},
                ],
                "measures": [
                    {"name": "Total Incidentes",
                     "expression": "COUNTROWS(Incidentes)",
                     "formatString": "0"},
                    {"name": "Incidentes Registrables",
                     "expression": "SUM(Incidentes[es_registrable])",
                     "formatString": "0"},
                    {"name": "Total LTI Inc",
                     "expression": "SUM(Incidentes[es_lti])",
                     "formatString": "0"},
                    {"name": "Dias Perdidos Inc",
                     "expression": "SUM(Incidentes[dias_perdidos])",
                     "formatString": "0"},
                ],
                "partitions": [{"name": "Incidentes", "source": {"type": "m", "expression": m_expr("Incidentes")}}]
            },
            {
                "name": "Ausentismo",
                "columns": [
                    {"name": "empleado_id",     "dataType": "int64",    "sourceColumn": "empleado_id"},
                    {"name": "departamento",    "dataType": "string",   "sourceColumn": "departamento"},
                    {"name": "ubicacion",       "dataType": "string",   "sourceColumn": "ubicacion"},
                    {"name": "turno",           "dataType": "string",   "sourceColumn": "turno"},
                    {"name": "causa",           "dataType": "string",   "sourceColumn": "causa"},
                    {"name": "fecha_inicio",    "dataType": "dateTime", "sourceColumn": "fecha_inicio"},
                    {"name": "dias_ausencia",   "dataType": "int64",    "sourceColumn": "dias_ausencia"},
                    {"name": "mes",             "dataType": "int64",    "sourceColumn": "mes"},
                    {"name": "anio",            "dataType": "int64",    "sourceColumn": "anio"},
                    {"name": "es_accidente",    "dataType": "int64",    "sourceColumn": "es_accidente"},
                ],
                "measures": [
                    {"name": "Total Dias Ausencia",
                     "expression": "SUM(Ausentismo[dias_ausencia])",
                     "formatString": "0"},
                    {"name": "Total Eventos Ausentismo",
                     "expression": "COUNTROWS(Ausentismo)",
                     "formatString": "0"},
                    {"name": "Promedio Dias Evento",
                     "expression": "AVERAGE(Ausentismo[dias_ausencia])",
                     "formatString": "0.0"},
                    {"name": "Dias Perdidos Laboral",
                     "expression": "CALCULATE(SUM(Ausentismo[dias_ausencia]),Ausentismo[es_accidente]=1)",
                     "formatString": "0"},
                    {"name": "% Origen Laboral",
                     "expression": "DIVIDE(CALCULATE(SUM(Ausentismo[dias_ausencia]),Ausentismo[es_accidente]=1),SUM(Ausentismo[dias_ausencia]),0)",
                     "formatString": "0.0%"},
                ],
                "partitions": [{"name": "Ausentismo", "source": {"type": "m", "expression": m_expr("Ausentismo")}}]
            },
        ],
        "relationships": [
            {
                "name": "Emp_Inc",
                "fromTable": "Incidentes", "fromColumn": "empleado_id",
                "toTable": "Empleados",   "toColumn": "empleado_id",
                "crossFilteringBehavior": "oneDirection"
            },
            {
                "name": "Emp_Aus",
                "fromTable": "Ausentismo", "fromColumn": "empleado_id",
                "toTable": "Empleados",    "toColumn": "empleado_id",
                "crossFilteringBehavior": "oneDirection"
            },
        ],
        "annotations": [
            {"name": "PBIDesktopVersion",   "value": "2.136.1202.0"},
            {"name": "PBI_QueryOrder",      "value": json.dumps(["KPIs_Mensuales","Empleados","Incidentes","Ausentismo"])},
        ]
    }
}

# ─── REPORT LAYOUT ─────────────────────────────────────────────────────────
THEME_CONFIG = json.dumps({
    "version": "5.1.0",
    "themeCollection": {
        "baseTheme": {"name": "CY24SU06", "version": "5.1.0", "type": 2}
    },
    "activeSectionIndex": 0
})

SECTION_CONFIG = json.dumps({"visibility": 0})

def vc_card(x, y, w, h, table, measure, label_color="#1B4F72", z=2000):
    """Visual container — Tarjeta KPI."""
    query = json.dumps({
        "Version": 2,
        "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": table, "Type": 0}],
                "Select": [{"Measure": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": measure},
                            "Name": f"{table}.{measure}"}]
            },
            "Binding": {"Primary": {"Groupings": [{"Projections": [0]}]},
                        "DataReduction": {"DataVolume": 3, "Primary": {"Top": {}}}, "Version": 1}
        }}]}
    })
    config = json.dumps({
        "version": "5.1.0", "themeCollection": {},
        "visualType": "card",
        "objects": {
            "labels": [{"properties": {
                "fontSize":   {"expr": {"Literal": {"Value": "26D"}}},
                "bold":       {"expr": {"Literal": {"Value": "true L"}}},
                "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI'"}}},
                "color":      {"solid": {"color": {"expr": {"Literal": {"Value": f"'{label_color}'"}}}}}
            }}],
            "categoryLabels": [{"properties": {
                "show":       {"expr": {"Literal": {"Value": "true L"}}},
                "fontSize":   {"expr": {"Literal": {"Value": "11D"}}},
                "fontFamily": {"expr": {"Literal": {"Value": "'Segoe UI'"}}}
            }}],
            "background": [{"properties": {
                "show":  {"expr": {"Literal": {"Value": "true L"}}},
                "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FFFFFF'"}}}}}
            }}]
        }
    })
    transforms = json.dumps({"queryMetadata": {"Select": [{"Restatement": measure, "Name": f"{table}.{measure}"}]}})
    return {"x": x, "y": y, "z": z, "width": w, "height": h,
            "config": config, "filters": "[]", "query": query,
            "dataTransforms": transforms, "howCreated": 3}

def vc_line(x, y, w, h, table, x_col, measures_list, z=2000):
    """Visual container — Gráfico de líneas."""
    frm = [{"Name": "t", "Entity": table, "Type": 0}]
    sel = [{"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": x_col},
            "Name": f"{table}.{x_col}"}]
    for m in measures_list:
        sel.append({"Measure": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": m},
                    "Name": f"{table}.{m}"})
    query = json.dumps({
        "Version": 2,
        "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
            "Query": {"Version": 2, "From": frm, "Select": sel},
            "Binding": {
                "Primary": {"Groupings": [{"Projections": [0]}]},
                "Secondary": {"Groupings": [{"Projections": list(range(1, len(measures_list)+1))}]},
                "DataReduction": {"DataVolume": 4, "Primary": {"Top": {"Count": 1000}}},
                "Version": 1
            }
        }}]}
    })
    config = json.dumps({
        "version": "5.1.0", "themeCollection": {},
        "visualType": "lineChart",
        "objects": {
            "dataPoint": [{"properties": {"defaultColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#C1121F'"}}}}}}}],
            "lineStyles": [{"properties": {"strokeWidth": {"expr": {"Literal": {"Value": "2D"}}}}}]
        }
    })
    transforms = json.dumps({"queryMetadata": {"Select":
        [{"Restatement": x_col, "Name": f"{table}.{x_col}"}] +
        [{"Restatement": m, "Name": f"{table}.{m}"} for m in measures_list]
    }})
    return {"x": x, "y": y, "z": z, "width": w, "height": h,
            "config": config, "filters": "[]", "query": query,
            "dataTransforms": transforms, "howCreated": 3}

def vc_bar(x, y, w, h, table, cat_col, measure, z=2000):
    """Visual container — Gráfico de barras."""
    query = json.dumps({
        "Version": 2,
        "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
            "Query": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": table, "Type": 0}],
                "Select": [
                    {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": cat_col},
                     "Name": f"{table}.{cat_col}"},
                    {"Measure": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": measure},
                     "Name": f"{table}.{measure}"}
                ],
                "OrderBy": [{"Direction": 2, "Expression": {"Measure": {
                    "Expression": {"SourceRef": {"Source": "t"}}, "Property": measure}}}]
            },
            "Binding": {
                "Primary": {"Groupings": [{"Projections": [0, 1]}]},
                "DataReduction": {"DataVolume": 4, "Primary": {"Top": {"Count": 1000}}},
                "Version": 1
            }
        }}]}
    })
    config = json.dumps({
        "version": "5.1.0", "themeCollection": {},
        "visualType": "barChart",
        "objects": {"dataPoint": [{"properties": {
            "defaultColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#1B4F72'"}}}}}
        }}]}
    })
    transforms = json.dumps({"queryMetadata": {"Select": [
        {"Restatement": cat_col, "Name": f"{table}.{cat_col}"},
        {"Restatement": measure, "Name": f"{table}.{measure}"}
    ]}})
    return {"x": x, "y": y, "z": z, "width": w, "height": h,
            "config": config, "filters": "[]", "query": query,
            "dataTransforms": transforms, "howCreated": 3}

def text_box(x, y, w, h, text, font_size=20, color="#1B4F72", bold=True, z=1000):
    """Cuadro de texto — título o subtítulo."""
    config = json.dumps({
        "version": "5.1.0", "themeCollection": {},
        "visualType": "textbox",
        "objects": {"general": [{"properties": {
            "paragraphs": [{"textRuns": [{"value": text, "textStyle": {
                "fontFamily": "Segoe UI",
                "fontSize": f"{font_size}pt",
                "bold": bold,
                "color": {"solid": {"color": color}}
            }}], "horizontalTextAlignment": "left"}]
        }}]}
    })
    return {"x": x, "y": y, "z": z, "width": w, "height": h,
            "config": config, "filters": "[]", "query": "{}",
            "dataTransforms": "{}", "howCreated": 3}

# ─── PÁGINAS DEL REPORTE ───────────────────────────────────────────────────
W, H = 1280, 720   # dimensiones del lienzo (px)
CARD_W, CARD_H = 270, 100
GAP = 14
CARD_Y = 90

sections = [
    # ── PÁGINA 1: Dashboard Ejecutivo ──────────────────────────────────────
    {
        "id": 0, "name": "ReportSection1",
        "displayName": "Dashboard Ejecutivo",
        "filters": "[]", "ordinal": 0,
        "config": SECTION_CONFIG,
        "width": W, "height": H,
        "visualContainers": [
            text_box(0, 0, W, 60,
                     "YPF-Patagonia S.A. — Dashboard HSE | 2022–2024",
                     font_size=18, color="#1B4F72", bold=True, z=500),
            text_box(0, 55, W, 30,
                     "Health, Safety & Environment Analytics  |  Cuenca Neuquina, Argentina",
                     font_size=10, color="#4A4E69", bold=False, z=500),

            # 4 tarjetas KPI
            vc_card(GAP,                    CARD_Y, CARD_W, CARD_H, "KPIs_Mensuales", "LTIFR Promedio",    "#C1121F"),
            vc_card(GAP*2+CARD_W,           CARD_Y, CARD_W, CARD_H, "KPIs_Mensuales", "TRIFR Promedio",    "#E85D04"),
            vc_card(GAP*3+CARD_W*2,         CARD_Y, CARD_W, CARD_H, "KPIs_Mensuales", "Tasa Ausentismo %", "#1B4F72"),
            vc_card(GAP*4+CARD_W*3,         CARD_Y, CARD_W, CARD_H, "Empleados",      "Empleados Riesgo Alto", "#4A4E69"),

            # Líneas LTIFR/TRIFR
            vc_line(GAP, CARD_Y+CARD_H+GAP, 620, 260,
                    "KPIs_Mensuales", "fecha", ["LTIFR Promedio", "TRIFR Promedio"]),

            # Barras tasa ausentismo
            vc_bar(GAP*2+620, CARD_Y+CARD_H+GAP, 610, 260,
                   "KPIs_Mensuales", "fecha", "Tasa Ausentismo %"),

            # Barras incidentes por departamento
            vc_bar(GAP, CARD_Y+CARD_H+GAP*2+260, 620, 220,
                   "Incidentes", "departamento", "Total Incidentes"),

            # Barras ausencia por causa
            vc_bar(GAP*2+620, CARD_Y+CARD_H+GAP*2+260, 610, 220,
                   "Ausentismo", "causa", "Total Dias Ausencia"),
        ]
    },
    # ── PÁGINA 2: Análisis de Incidentes ───────────────────────────────────
    {
        "id": 1, "name": "ReportSection2",
        "displayName": "Analisis de Incidentes",
        "filters": "[]", "ordinal": 1,
        "config": SECTION_CONFIG,
        "width": W, "height": H,
        "visualContainers": [
            text_box(0, 0, W, 50, "Análisis de Incidentes — YPF-Patagonia | 2022–2024",
                     font_size=16, color="#1B4F72", bold=True, z=500),

            vc_card(GAP,           60, 280, 90, "Incidentes", "Total Incidentes",         "#1B4F72"),
            vc_card(GAP*2+280,     60, 280, 90, "Incidentes", "Incidentes Registrables",  "#E85D04"),
            vc_card(GAP*3+560,     60, 280, 90, "Incidentes", "Total LTI Inc",             "#C1121F"),
            vc_card(GAP*4+840,     60, 280, 90, "Incidentes", "Dias Perdidos Inc",         "#4A4E69"),

            vc_bar(GAP, 165, 605, 240, "Incidentes", "tipo_incidente", "Total Incidentes"),
            vc_bar(GAP*2+605, 165, 605, 240, "Incidentes", "causa_raiz", "Total Incidentes"),
            vc_bar(GAP, 420, 605, 240, "Incidentes", "area", "Total Incidentes"),
            vc_bar(GAP*2+605, 420, 605, 240, "Incidentes", "turno", "Total Incidentes"),
        ]
    },
    # ── PÁGINA 3: Análisis de Ausentismo ───────────────────────────────────
    {
        "id": 2, "name": "ReportSection3",
        "displayName": "Analisis de Ausentismo",
        "filters": "[]", "ordinal": 2,
        "config": SECTION_CONFIG,
        "width": W, "height": H,
        "visualContainers": [
            text_box(0, 0, W, 50, "Análisis de Ausentismo — YPF-Patagonia | 2022–2024",
                     font_size=16, color="#1B4F72", bold=True, z=500),

            vc_card(GAP,         60, 270, 90, "Ausentismo", "Total Dias Ausencia",      "#C1121F"),
            vc_card(GAP*2+270,   60, 270, 90, "Ausentismo", "Total Eventos Ausentismo", "#E85D04"),
            vc_card(GAP*3+540,   60, 270, 90, "Ausentismo", "Promedio Dias Evento",     "#1B4F72"),
            vc_card(GAP*4+810,   60, 270, 90, "Ausentismo", "% Origen Laboral",         "#2D6A4F"),

            vc_bar(GAP, 165, 620, 260, "Ausentismo", "causa", "Total Dias Ausencia"),
            vc_bar(GAP*2+620, 165, 610, 260, "Ausentismo", "departamento", "Total Dias Ausencia"),
            vc_bar(GAP, 440, 620, 240, "Ausentismo", "anio", "Total Dias Ausencia"),
            vc_bar(GAP*2+620, 440, 610, 240, "Ausentismo", "turno", "Total Dias Ausencia"),
        ]
    },
    # ── PÁGINA 4: Perfil de Riesgo ─────────────────────────────────────────
    {
        "id": 3, "name": "ReportSection4",
        "displayName": "Perfil de Riesgo",
        "filters": "[]", "ordinal": 3,
        "config": SECTION_CONFIG,
        "width": W, "height": H,
        "visualContainers": [
            text_box(0, 0, W, 50, "Perfil de Riesgo por Empleado — GBM Classifier",
                     font_size=16, color="#1B4F72", bold=True, z=500),

            vc_card(GAP,         60, 270, 90, "Empleados", "Total Empleados",         "#1B4F72"),
            vc_card(GAP*2+270,   60, 270, 90, "Empleados", "Empleados Riesgo Alto",   "#C1121F"),
            vc_card(GAP*3+540,   60, 270, 90, "Empleados", "% Riesgo Alto",           "#E85D04"),
            vc_card(GAP*4+810,   60, 270, 90, "Empleados", "Score Riesgo Promedio",   "#4A4E69"),

            vc_bar(GAP, 165, 620, 260, "Empleados", "departamento",     "Empleados Riesgo Alto"),
            vc_bar(GAP*2+620, 165, 610, 260, "Empleados", "turno",      "Empleados Riesgo Alto"),
            vc_bar(GAP, 440, 620, 240, "Empleados", "ubicacion",        "Score Riesgo Promedio"),
            vc_bar(GAP*2+620, 440, 610, 240, "Empleados", "categoria_riesgo", "Total Empleados"),
        ]
    },
]

report_layout = {
    "id": 0,
    "resourcePackages": [],
    "sections": sections,
    "config": THEME_CONFIG,
    "layoutOptimization": 0
}

# ─── ARMAR EL ZIP (.pbit) ─────────────────────────────────────────────────
content_types = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json; charset=utf-8"/>
  <Override PartName="/DataModelSchema" ContentType="application/json; charset=utf-8"/>
  <Override PartName="/Report/Layout"   ContentType="application/json; charset=utf-8"/>
  <Override PartName="/Metadata"        ContentType="application/json; charset=utf-8"/>
</Types>'''

metadata = {"version": "3.0", "createdFrom": "Report"}

OUT.parent.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("[Content_Types].xml",   content_types)
    zf.writestr("Version",              "2.0")
    zf.writestr("Metadata",             json.dumps(metadata, ensure_ascii=False))
    zf.writestr("DataModelSchema",      json.dumps(data_model, ensure_ascii=False, indent=2))
    zf.writestr("Report/Layout",        json.dumps(report_layout, ensure_ascii=False, indent=2))

size_kb = OUT.stat().st_size / 1024
print(f"Archivo generado: {OUT}")
print(f"Tamanio: {size_kb:.1f} KB")
print(f"Paginas: {len(sections)}")
total_vis = sum(len(s['visualContainers']) for s in sections)
print(f"Visuales totales: {total_vis}")
print(f"Medidas DAX: {sum(len(t.get('measures',[])) for t in data_model['model']['tables'])}")
print(f"\nPara abrir: doble clic en {OUT.name}")
print("Power BI te pedira conectar el Excel — confirmalo y el dashboard aparece completo.")

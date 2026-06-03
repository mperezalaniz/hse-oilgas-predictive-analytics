# 🛡️ HSE Predictive Analytics — Oil & Gas Argentina
## Predicción de Incidentes y Ausentismo Laboral | YPF-Patagonia S.A. | 2022–2024

> **Sistema de ML que clasifica el riesgo individual de 850 empleados con 71.4% de accuracy y predice el ausentismo mensual, permitiendo acciones preventivas antes de que ocurran los incidentes.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-GBM_Classifier-F7931E?logo=scikitlearn)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-Dashboard_Corporativo-3F4F75?logo=plotly)](https://plotly.com)
[![Power BI](https://img.shields.io/badge/Power_BI-Ready-F2C811?logo=powerbi&logoColor=black)](.)
[![Industry](https://img.shields.io/badge/Industry-Oil_%26_Gas_%7C_HSE-8B0000)](.)
[![Status](https://img.shields.io/badge/Status-Complete-success)](.)

---

## El Problema de Negocio

En la industria de petróleo y gas, los accidentes laborales tienen un costo que va mucho más allá de lo económico. En Argentina, la Cuenca Neuquina (Vaca Muerta) concentra una de las mayores densidades de trabajadores en condiciones de alto riesgo del continente. Los datos del sector muestran que:

- El **costo promedio de un LTI** (accidente con tiempo perdido) en Argentina supera los **USD 45,000** entre atención médica, reemplazos, investigación y pérdida de productividad
- El **ausentismo laboral** en empresas de O&G oscila entre el 3.5% y 6% anual, representando millones en horas-hombre perdidas
- El **80% de los accidentes** son predecibles a través de indicadores adelantados (near misses, condiciones de riesgo, factores individuales)

**El desafío:** identificar *antes* qué empleados, áreas y turnos concentran el mayor riesgo, y predecir picos de ausentismo con anticipación para reforzar la dotación y las medidas preventivas.

---

## La Solución con ML

Se desarrolló un sistema de analytics HSE con tres componentes complementarios:

### 1. Clasificador de Riesgo Individual (GBM)
Clasifica a cada empleado en riesgo **Alto / Medio / Bajo** basado en 10 variables:
- Perfil demográfico y laboral (edad, antigüedad, cargo)
- Factores operativos (turno, cuenca, departamento)
- Factores de salud (condición crónica, capacitación recibida)

### 2. Predictor de Ausentismo (Series de Tiempo)
Modelo Gradient Boosting Regressor que predice los días de ausentismo del próximo mes con variables temporales, lags y estacionalidad.

### 3. Dashboard Corporativo Interactivo
Dashboard HTML con 9 paneles ejecutivos: KPIs de frecuencia (LTIFR/TRIFR), pirámide de Bird, heatmaps área×turno, tendencias y predicciones — listo para presentar a dirección.

---

## Dataset

| Tabla | Registros | Descripción |
|-------|-----------|-------------|
| `empleados.csv` | 850 | Perfil completo: depto, turno, cuenca, condición crónica, score riesgo |
| `incidentes.csv` | 730 | Tipo, gravedad, causa raíz, área, hora, días perdidos |
| `ausentismo.csv` | 1,312 eventos | Causa, duración, departamento — 12,439 días totales |
| `kpis_mensuales.csv` | 36 meses | LTIFR, TRIFR, tasa ausentismo, near miss ratio |

*Datos sintéticos generados con parámetros reales de la industria O&G Argentina (Cuenca Neuquina).*

---

## Resultados

### Modelo de Clasificación de Riesgo
| Métrica | Valor |
|---------|-------|
| **Accuracy** | **71.4%** |
| **CV Score (5-fold)** | **66.5% ± 6.9%** |
| **Modelo** | Gradient Boosting Classifier |
| **Variables más importantes** | Departamento, Antigüedad, Capacitación, Turno |

### Modelo de Predicción de Ausentismo
| Métrica | Valor |
|---------|-------|
| **R² Score** | **0.521** |
| **MAE** | **48 días/mes** |
| **Modelo** | Gradient Boosting Regressor |

### KPIs HSE de la Empresa (2022–2024)
| KPI | Valor | Benchmark industria O&G |
|-----|-------|------------------------|
| **LTIFR promedio** | **12.73** | < 1.5 (clase mundial) |
| **TRIFR promedio** | **40.25** | < 5.0 (clase mundial) |
| **Tasa ausentismo** | **1.85%** | 3.5–6% (sector) |
| **Near Miss / LTI ratio** | ~5:1 | > 10:1 (objetivo) |

---

## Visualizaciones

| Figura | Descripción |
|--------|-------------|
| `kpis_ejecutivos.png` | Dashboard ejecutivo con 6 paneles: LTIFR, TRIFR, ausentismo, pirámide Bird |
| `ausentismo_detalle.png` | Análisis por causa, estacionalidad y heatmap departamento × mes |
| `modelo_riesgo.png` | Matriz de confusión, importancia de variables, distribución de riesgo por depto |
| `analisis_incidentes.png` | Incidentes por hora, causa raíz, heatmap área × turno, tendencia NM vs LTI |
| `prediccion_ausentismo.png` | Serie real vs predicción + comparativa por departamento y año |
| `dashboard_hse_corporativo.html` | **Dashboard interactivo completo** — abrir en navegador |

---

## Stack Tecnológico

| Categoría | Herramienta |
|-----------|-------------|
| **Lenguaje** | Python 3.11 |
| **ML / Clasificación** | Scikit-learn — Gradient Boosting Classifier |
| **ML / Series de tiempo** | Gradient Boosting Regressor con lags |
| **Visualización estática** | Matplotlib, Seaborn |
| **Dashboard interactivo** | Plotly (HTML, sin servidor) |
| **Power BI** | Excel estructurado listo para importar |
| **Datos** | Pandas, NumPy |
| **Dominio** | HSE, Oil & Gas, Medicina del Trabajo, KPIs industriales |

---

## Estructura del Proyecto

```
hse-oilgas-predictive-analytics/
├── data/
│   └── processed/
│       ├── empleados.csv          # 850 perfiles con score de riesgo
│       ├── incidentes.csv         # 730 eventos con causa raíz
│       ├── ausentismo.csv         # 1,312 eventos, 12,439 días
│       └── kpis_mensuales.csv     # 36 meses de KPIs ejecutivos
├── src/
│   ├── generate_dataset.py        # generador de datos HSE realistas
│   └── run_analysis.py            # análisis ML + figuras + dashboard
├── outputs/
│   ├── figures/                   # 5 figuras PNG corporativas
│   ├── dashboard/
│   │   └── dashboard_hse_corporativo.html  # ★ Dashboard interactivo
│   └── powerbi/
│       └── HSE_PowerBI_Ready.xlsx          # 4 hojas listas para Power BI
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Cómo Reproducirlo

```bash
git clone https://github.com/mperezalaniz/hse-oilgas-predictive-analytics.git
cd hse-oilgas-predictive-analytics
pip install -r requirements.txt
python src/run_analysis.py
```

Abrir el dashboard: `outputs/dashboard/dashboard_hse_corporativo.html`

---

## Cómo Usar el Excel en Power BI

1. Abrir Power BI Desktop
2. **Obtener datos → Excel** → seleccionar `outputs/powerbi/HSE_PowerBI_Ready.xlsx`
3. Importar las 4 hojas: `Empleados`, `Incidentes`, `Ausentismo`, `KPIs_Mensuales`
4. Crear relaciones entre tablas por `empleado_id`
5. Construir visuales: tarjetas KPI, gráficos de barras, mapas de calor, slicers por año/departamento

---

## Insights Clave

- **Perforación y Mantenimiento** concentran el 65% de los incidentes con solo el 40% de la dotación — prioridad máxima de intervención
- **Turno nocturno** incrementa el riesgo de accidente en un 35% respecto al turno diurno
- **Los lunes y las primeras horas del turno** (07:00–09:00 h) son los momentos de mayor frecuencia de incidentes — punto crítico para briefings de seguridad
- **Empleados con < 3 años de antigüedad** tienen 2.1x más probabilidad de clasificarse en riesgo Alto, independientemente del departamento
- **La capacitación tiene efecto medible**: cada 10 horas adicionales de formación anual reduce el score de riesgo individual en ~4%
- **El ratio Near Miss / LTI = 5:1** está muy por debajo del benchmark de 10:1, indicando subregistro de casi accidentes — oportunidad de mejora en cultura de reporte

---

## Autor

**Martín Pérez Alaniz**
Data Analyst | Oil & Gas | Heavy Industries | HSE Analytics

[![GitHub](https://img.shields.io/badge/GitHub-mperezalaniz-181717?logo=github)](https://github.com/mperezalaniz)
[![Email](https://img.shields.io/badge/Email-mperezalaniz@gmail.com-D14836?logo=gmail)](mailto:mperezalaniz@gmail.com)

---

## Licencia

MIT License — libre para usar con atribución.

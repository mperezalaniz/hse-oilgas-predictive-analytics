"""
Análisis completo HSE: clasificación de riesgo, predicción de ausentismo,
clustering de perfiles y dashboard corporativo HTML.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import subprocess, sys
from pathlib import Path

BASE = Path(__file__).parent.parent
FIGS = BASE / 'outputs' / 'figures'
DASH = BASE / 'outputs' / 'dashboard'
FIGS.mkdir(exist_ok=True, parents=True)
DASH.mkdir(exist_ok=True, parents=True)

# ── Paleta corporativa oil & gas ──
C = {
    'rojo':     '#C1121F',
    'naranja':  '#E85D04',
    'amarillo': '#F48C06',
    'verde':    '#2D6A4F',
    'azul':     '#1B4F72',
    'gris':     '#4A4E69',
    'bg':       '#F8F9FA',
    'blanco':   '#FFFFFF',
}
plt.rcParams.update({
    'figure.facecolor': C['bg'],
    'axes.facecolor':   C['bg'],
    'font.family':      'DejaVu Sans',
    'font.size':        11,
    'axes.titlesize':   14,
    'axes.titleweight': 'bold',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'figure.dpi':       130,
})

# ── Generar dataset si no existe ──
if not (BASE / 'data' / 'processed' / 'empleados.csv').exists():
    print("Generando dataset HSE...")
    subprocess.run([sys.executable, str(BASE / 'src' / 'generate_dataset.py')], check=True)

print("Cargando datasets...")
df_emp = pd.read_csv(BASE / 'data' / 'processed' / 'empleados.csv')
df_aus = pd.read_csv(BASE / 'data' / 'processed' / 'ausentismo.csv', parse_dates=['fecha_inicio'])
df_inc = pd.read_csv(BASE / 'data' / 'processed' / 'incidentes.csv', parse_dates=['fecha'])
df_kpi = pd.read_csv(BASE / 'data' / 'processed' / 'kpis_mensuales.csv', parse_dates=['fecha'])

print(f"  {len(df_emp):,} empleados | {len(df_aus):,} ausencias | {len(df_inc):,} incidentes")

# ══════════════════════════════════════════
# FIGURA 1 — KPIs ejecutivos (4 paneles)
# ══════════════════════════════════════════
print("Figura 1: KPIs ejecutivos...")
fig = plt.figure(figsize=(18, 10))
fig.patch.set_facecolor(C['bg'])

# Tendencia LTIFR y TRIFR
ax1 = fig.add_subplot(2, 3, (1, 2))
ax1.fill_between(df_kpi['fecha'], df_kpi['trifr'], alpha=0.25, color=C['naranja'])
ax1.plot(df_kpi['fecha'], df_kpi['trifr'], '-o', color=C['naranja'], linewidth=2,
         markersize=4, label='TRIFR (Registrables × 10⁶ HH)')
ax1.fill_between(df_kpi['fecha'], df_kpi['ltifr'], alpha=0.35, color=C['rojo'])
ax1.plot(df_kpi['fecha'], df_kpi['ltifr'], '-s', color=C['rojo'], linewidth=2.5,
         markersize=5, label='LTIFR (LTI × 10⁶ HH)')
ax1.set_title('Evolución de Indicadores de Frecuencia — 2022 a 2024', pad=10)
ax1.set_ylabel('Frecuencia por millón HH')
ax1.legend(loc='upper right', fontsize=9)
ax1.set_facecolor(C['bg'])

# Tasa de ausentismo mensual
ax2 = fig.add_subplot(2, 3, 3)
colores_bar = [C['rojo'] if v > 4.5 else C['amarillo'] if v > 3.0 else C['verde']
               for v in df_kpi['tasa_ausentismo_pct']]
ax2.bar(range(len(df_kpi)), df_kpi['tasa_ausentismo_pct'], color=colores_bar, alpha=0.85)
ax2.axhline(df_kpi['tasa_ausentismo_pct'].mean(), color=C['azul'], linestyle='--',
            linewidth=1.5, label=f"Promedio: {df_kpi['tasa_ausentismo_pct'].mean():.1f}%")
ax2.axhline(3.5, color=C['rojo'], linestyle=':', linewidth=1.5, label='Límite objetivo: 3.5%')
ax2.set_title('Tasa de Ausentismo Mensual (%)')
ax2.set_ylabel('%')
ax2.legend(fontsize=8)
ax2.set_facecolor(C['bg'])
ax2.set_xticks([])

# Pirámide de Bird (incidentes por tipo)
ax3 = fig.add_subplot(2, 3, 4)
piramide = df_inc.groupby('tipo_incidente').size().sort_values()
colores_p = [C['verde'], C['amarillo'], C['amarillo'], C['naranja'], C['naranja'], C['rojo'], C['rojo']][:len(piramide)]
bars = ax3.barh(piramide.index, piramide.values, color=colores_p[::-1], alpha=0.85, height=0.6)
for bar, val in zip(bars, piramide.values):
    ax3.text(val + 1, bar.get_y() + bar.get_height()/2, str(val), va='center', fontsize=9)
ax3.set_title('Pirámide de Incidentes (Bird)')
ax3.set_xlabel('Cantidad')
ax3.set_facecolor(C['bg'])

# Incidentes por departamento
ax4 = fig.add_subplot(2, 3, 5)
inc_depto = df_inc.groupby('departamento').size().sort_values(ascending=True)
colores_d = [C['rojo'] if d in ['Perforación','Mantenimiento'] else C['naranja'] if d == 'Producción'
             else C['azul'] for d in inc_depto.index]
ax4.barh(inc_depto.index, inc_depto.values, color=colores_d, alpha=0.85, height=0.6)
ax4.set_title('Incidentes por Departamento')
ax4.set_xlabel('Cantidad')
ax4.set_facecolor(C['bg'])

# Near Miss vs LTI ratio
ax5 = fig.add_subplot(2, 3, 6)
ratio = df_kpi.groupby('anio')['ratio_nm_a_lti'].mean()
bars = ax5.bar(ratio.index.astype(str), ratio.values,
               color=[C['verde'], C['amarillo'], C['naranja']][:len(ratio)], alpha=0.85, width=0.5)
ax5.axhline(10, color=C['azul'], linestyle='--', linewidth=1.5, label='Benchmark: 10:1')
for bar, val in zip(bars, ratio.values):
    ax5.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.1f}:1',
             ha='center', va='bottom', fontweight='bold')
ax5.set_title('Ratio Near Miss / LTI por Año')
ax5.set_ylabel('Ratio')
ax5.legend(fontsize=9)
ax5.set_facecolor(C['bg'])

plt.suptitle('YPF-Patagonia S.A. — Dashboard Ejecutivo HSE | 2022–2024',
             fontsize=16, fontweight='bold', color=C['azul'], y=1.01)
plt.tight_layout()
plt.savefig(FIGS / 'kpis_ejecutivos.png', dpi=150, bbox_inches='tight', facecolor=C['bg'])
plt.close()

# ══════════════════════════════════════════
# FIGURA 2 — Ausentismo por causa y departamento
# ══════════════════════════════════════════
print("Figura 2: Ausentismo detallado...")
fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(C['bg'])

# Días perdidos por causa
causa_dias = df_aus.groupby('causa')['dias_ausencia'].sum().sort_values(ascending=True)
colores_c  = [C['rojo'] if 'Accidente' in c or 'profesional' in c or 'mental' in c
              else C['naranja'] if 'médica' in c or 'Cirugía' in c
              else C['azul'] for c in causa_dias.index]
axes[0].barh(causa_dias.index, causa_dias.values, color=colores_c, alpha=0.85, height=0.65)
axes[0].set_title('Días Perdidos por Causa')
axes[0].set_xlabel('Días totales (2022–2024)')
axes[0].set_facecolor(C['bg'])
for i, (val, name) in enumerate(zip(causa_dias.values, causa_dias.index)):
    axes[0].text(val + 10, i, f'{val:,}', va='center', fontsize=9)

# Ausentismo mensual por año
for anio, col in zip([2022, 2023, 2024], [C['azul'], C['naranja'], C['rojo']]):
    d = df_aus[df_aus['fecha_inicio'].dt.year == anio].groupby(
        df_aus['fecha_inicio'].dt.month)['dias_ausencia'].sum()
    axes[1].plot(d.index, d.values, '-o', color=col, label=str(anio), linewidth=2, markersize=5)
axes[1].set_title('Ausentismo Mensual por Año (días)')
axes[1].set_xlabel('Mes')
axes[1].set_ylabel('Días de ausencia')
axes[1].set_xticks(range(1, 13))
axes[1].set_xticklabels(['E','F','M','A','M','J','J','A','S','O','N','D'])
axes[1].legend()
axes[1].set_facecolor(C['bg'])

# Heatmap ausentismo: depto × mes
pivot = df_aus.pivot_table(index='departamento', columns='mes',
                           values='dias_ausencia', aggfunc='sum', fill_value=0)
sns.heatmap(pivot, ax=axes[2], cmap='YlOrRd', annot=True, fmt='.0f',
            linewidths=0.5, cbar_kws={'label': 'Días perdidos'})
axes[2].set_title('Heatmap: Días Perdidos Depto × Mes')
axes[2].set_xlabel('Mes')
axes[2].set_ylabel('')
axes[2].set_facecolor(C['bg'])

plt.suptitle('Análisis de Ausentismo — YPF-Patagonia | 2022–2024',
             fontsize=14, fontweight='bold', color=C['azul'])
plt.tight_layout()
plt.savefig(FIGS / 'ausentismo_detalle.png', dpi=150, bbox_inches='tight', facecolor=C['bg'])
plt.close()

# ══════════════════════════════════════════
# FIGURA 3 — Modelo ML: Clasificación de Riesgo
# ══════════════════════════════════════════
print("Figura 3: Modelo de clasificación de riesgo...")
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder

# Preparar features
df_model = df_emp.copy()
le_depto = LabelEncoder()
le_turno = LabelEncoder()
le_ubic  = LabelEncoder()
le_cond  = LabelEncoder()

df_model['depto_enc'] = le_depto.fit_transform(df_model['departamento'])
df_model['turno_enc'] = le_turno.fit_transform(df_model['turno'])
df_model['ubic_enc']  = le_ubic.fit_transform(df_model['ubicacion'])
df_model['cond_enc']  = le_cond.fit_transform(df_model['condicion_cronica'])
df_model['turno_nocturno'] = (df_model['turno'] == 'Nocturno').astype(int)
df_model['turno_rotativo'] = df_model['turno'].str.contains('Rotativo').astype(int)
df_model['exp_cat'] = pd.cut(df_model['antiguedad_anios'], bins=[-1, 2, 7, 15, 50],
                              labels=[0, 1, 2, 3]).astype(int)

features_ml = ['edad', 'antiguedad_anios', 'capacitacion_hs_año',
                'depto_enc', 'turno_enc', 'ubic_enc', 'cond_enc',
                'turno_nocturno', 'turno_rotativo', 'exp_cat']
target_ml   = 'categoria_riesgo'

X = df_model[features_ml]
y = df_model[target_ml]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

model = GradientBoostingClassifier(n_estimators=300, learning_rate=0.05,
                                   max_depth=4, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

acc = (y_pred == y_test).mean()
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"  Accuracy: {acc:.4f} | CV: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor(C['bg'])

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred, labels=['Alto', 'Medio', 'Bajo'])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Alto', 'Medio', 'Bajo'],
            yticklabels=['Alto', 'Medio', 'Bajo'],
            ax=axes[0], linewidths=0.5)
axes[0].set_title(f'Matriz de Confusión\nAccuracy: {acc:.1%} | CV: {cv_scores.mean():.1%}')
axes[0].set_ylabel('Real')
axes[0].set_xlabel('Predicho')
axes[0].set_facecolor(C['bg'])

# Feature importance
importances = pd.DataFrame({'feature': features_ml, 'importance': model.feature_importances_}
                          ).sort_values('importance', ascending=True)
feat_labels = {
    'edad': 'Edad del empleado',
    'antiguedad_anios': 'Antigüedad (años)',
    'capacitacion_hs_año': 'Horas capacitación/año',
    'depto_enc': 'Departamento',
    'turno_enc': 'Tipo de turno',
    'ubic_enc': 'Ubicación/Cuenca',
    'cond_enc': 'Condición crónica',
    'turno_nocturno': 'Turno nocturno',
    'turno_rotativo': 'Turno rotativo',
    'exp_cat': 'Categoría experiencia',
}
importances['label'] = importances['feature'].map(feat_labels)
colors_imp = [C['rojo'] if v > 0.20 else C['naranja'] if v > 0.10 else C['azul']
              for v in importances['importance']]
axes[1].barh(importances['label'], importances['importance'], color=colors_imp, alpha=0.85, height=0.65)
axes[1].set_title('Importancia de Variables\n(Gradient Boosting)')
axes[1].set_xlabel('Importancia')
axes[1].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
axes[1].set_facecolor(C['bg'])

# Distribución de riesgo por departamento
risk_counts = df_emp.groupby(['departamento', 'categoria_riesgo']).size().unstack(fill_value=0)
risk_pct    = risk_counts.div(risk_counts.sum(axis=1), axis=0) * 100
risk_pct    = risk_pct.reindex(columns=['Alto', 'Medio', 'Bajo'], fill_value=0)
risk_pct.plot(kind='barh', ax=axes[2], color=[C['rojo'], C['amarillo'], C['verde']],
              alpha=0.85, width=0.65)
axes[2].set_title('Distribución de Riesgo por Departamento (%)')
axes[2].set_xlabel('%')
axes[2].xaxis.set_major_formatter(mtick.PercentFormatter())
axes[2].legend(title='Riesgo', loc='lower right', fontsize=9)
axes[2].set_facecolor(C['bg'])

plt.suptitle('Modelo Predictivo de Riesgo Individual — GBM Classifier',
             fontsize=14, fontweight='bold', color=C['azul'])
plt.tight_layout()
plt.savefig(FIGS / 'modelo_riesgo.png', dpi=150, bbox_inches='tight', facecolor=C['bg'])
plt.close()

# ══════════════════════════════════════════
# FIGURA 4 — Análisis de incidentes
# ══════════════════════════════════════════
print("Figura 4: Análisis de incidentes...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor(C['bg'])

# Incidentes por hora del día
inc_hora = df_inc.groupby('hora').size()
colores_h = [C['rojo'] if h in range(22, 24) or h in range(0, 6)
             else C['naranja'] if h in [6, 7, 14, 15]
             else C['azul'] for h in range(24)]
axes[0,0].bar(range(24), [inc_hora.get(h, 0) for h in range(24)], color=colores_h, alpha=0.85)
axes[0,0].set_title('Incidentes por Hora del Día')
axes[0,0].set_xlabel('Hora')
axes[0,0].set_ylabel('Cantidad')
axes[0,0].set_xticks(range(0, 24, 2))
axes[0,0].axvspan(22, 24, alpha=0.08, color='red', label='Riesgo nocturno')
axes[0,0].axvspan(0, 6, alpha=0.08, color='red')
axes[0,0].legend(fontsize=9)
axes[0,0].set_facecolor(C['bg'])

# Causas raíz
causa_raiz = df_inc.groupby('causa_raiz').size().sort_values(ascending=True)
colores_cr = [C['rojo'] if v == causa_raiz.max() else C['naranja'] if v > causa_raiz.median()
              else C['azul'] for v in causa_raiz.values]
axes[0,1].barh(causa_raiz.index, causa_raiz.values, color=colores_cr, alpha=0.85, height=0.65)
axes[0,1].set_title('Incidentes por Causa Raíz')
axes[0,1].set_xlabel('Cantidad')
axes[0,1].set_facecolor(C['bg'])

# Tendencia mensual incidentes graves vs near miss
df_kpi['fecha'] = pd.to_datetime(df_kpi['fecha'])
ax_twin = axes[1,0].twinx()
axes[1,0].bar(df_kpi['fecha'], df_kpi['near_misses'], color=C['verde'], alpha=0.5,
              width=20, label='Near Misses')
ax_twin.plot(df_kpi['fecha'], df_kpi['registrables'], '-o', color=C['rojo'],
             linewidth=2, markersize=5, label='Registrables')
ax_twin.plot(df_kpi['fecha'], df_kpi['lti'], '--s', color=C['naranja'],
             linewidth=1.5, markersize=4, label='LTI')
axes[1,0].set_title('Near Misses vs Incidentes Registrables')
axes[1,0].set_ylabel('Near Misses (barras)')
ax_twin.set_ylabel('Incidentes registrables / LTI')
axes[1,0].set_facecolor(C['bg'])
lines1, labels1 = axes[1,0].get_legend_handles_labels()
lines2, labels2 = ax_twin.get_legend_handles_labels()
axes[1,0].legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')

# Mapa de calor: área × turno
heatmap_data = df_inc.pivot_table(index='area', columns='turno',
                                   values='es_registrable', aggfunc='sum', fill_value=0)
sns.heatmap(heatmap_data, ax=axes[1,1], cmap='Reds', annot=True, fmt='.0f',
            linewidths=0.5, cbar_kws={'label': 'Incidentes registrables'})
axes[1,1].set_title('Incidentes Registrables: Área × Turno')
axes[1,1].set_xlabel('Turno')
axes[1,1].set_ylabel('')
axes[1,1].set_facecolor(C['bg'])

plt.suptitle('Análisis Detallado de Incidentes — YPF-Patagonia | 2022–2024',
             fontsize=14, fontweight='bold', color=C['azul'])
plt.tight_layout()
plt.savefig(FIGS / 'analisis_incidentes.png', dpi=150, bbox_inches='tight', facecolor=C['bg'])
plt.close()

# ══════════════════════════════════════════
# FIGURA 5 — Predicción de ausentismo (series de tiempo)
# ══════════════════════════════════════════
print("Figura 5: Predicción de ausentismo...")
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Agregar por mes
aus_ts = df_aus.copy()
aus_ts['anio'] = aus_ts['fecha_inicio'].dt.year
aus_ts['mes']  = aus_ts['fecha_inicio'].dt.month
ts = aus_ts.groupby(['anio', 'mes'])['dias_ausencia'].sum().reset_index()
ts = ts.sort_values(['anio', 'mes']).reset_index(drop=True)
ts['t'] = range(len(ts))

# Features temporales
ts['mes_sin'] = np.sin(2 * np.pi * ts['mes'] / 12)
ts['mes_cos'] = np.cos(2 * np.pi * ts['mes'] / 12)
ts['lag_1']   = ts['dias_ausencia'].shift(1)
ts['lag_3']   = ts['dias_ausencia'].shift(3)
ts['lag_12']  = ts['dias_ausencia'].shift(12)
ts['rolling_3'] = ts['dias_ausencia'].rolling(3, min_periods=1).mean()
ts = ts.dropna()

feat_ts = ['t', 'mes', 'mes_sin', 'mes_cos', 'lag_1', 'lag_3', 'lag_12', 'rolling_3']
X_ts = ts[feat_ts]
y_ts = ts['dias_ausencia']

split = int(len(ts) * 0.75)
X_tr, X_te = X_ts.iloc[:split], X_ts.iloc[split:]
y_tr, y_te = y_ts.iloc[:split], y_ts.iloc[split:]

reg = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=3, random_state=42)
reg.fit(X_tr, y_tr)
y_hat = reg.predict(X_te)

r2_ts  = r2_score(y_te, y_hat)
mae_ts = mean_absolute_error(y_te, y_hat)
print(f"  Ausentismo TS — R2: {r2_ts:.3f} | MAE: {mae_ts:.0f} dias")

fig, axes = plt.subplots(1, 2, figsize=(18, 6))
fig.patch.set_facecolor(C['bg'])

# Serie completa + prediccion
n_total = len(ts)
all_pred = np.concatenate([reg.predict(X_tr), y_hat])
axes[0].fill_between(range(n_total), ts['dias_ausencia'], alpha=0.3, color=C['azul'])
axes[0].plot(range(n_total), ts['dias_ausencia'], '-o', color=C['azul'],
             linewidth=2, markersize=4, label='Real')
axes[0].plot(range(split, n_total), y_hat, '--o', color=C['rojo'],
             linewidth=2.5, markersize=5, label=f'Prediccion GBR (R2={r2_ts:.3f})')
axes[0].axvline(split, color='gray', linestyle=':', linewidth=1.5, label='Train / Test')
axes[0].set_title(f'Prediccion de Dias de Ausentismo Mensual\nMAE: {mae_ts:.0f} dias/mes')
axes[0].set_xlabel('Mes (t)')
axes[0].set_ylabel('Dias de ausencia')
axes[0].legend(fontsize=9)
axes[0].set_facecolor(C['bg'])

# Ausentismo por departamento y año
aus_depto_anio = df_aus.copy()
aus_depto_anio['anio'] = aus_depto_anio['fecha_inicio'].dt.year
pivot_d = aus_depto_anio.groupby(['departamento', 'anio'])['dias_ausencia'].sum().unstack(fill_value=0)
x = np.arange(len(pivot_d))
w = 0.25
cols_anio = [C['azul'], C['naranja'], C['rojo']]
for i, (anio, col) in enumerate(zip(pivot_d.columns, cols_anio)):
    axes[1].bar(x + i*w, pivot_d[anio], width=w, color=col, alpha=0.85, label=str(anio))
axes[1].set_xticks(x + w)
axes[1].set_xticklabels(pivot_d.index, rotation=15, ha='right')
axes[1].set_title('Dias de Ausentismo por Departamento y Año')
axes[1].set_ylabel('Dias totales')
axes[1].legend(title='Año')
axes[1].set_facecolor(C['bg'])

plt.suptitle('Modelo de Predicción de Ausentismo — Gradient Boosting Regressor',
             fontsize=14, fontweight='bold', color=C['azul'])
plt.tight_layout()
plt.savefig(FIGS / 'prediccion_ausentismo.png', dpi=150, bbox_inches='tight', facecolor=C['bg'])
plt.close()

# ══════════════════════════════════════════
# DASHBOARD HTML CORPORATIVO
# ══════════════════════════════════════════
print("Generando dashboard HTML corporativo...")
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

fig_dash = make_subplots(
    rows=3, cols=3,
    subplot_titles=[
        'LTIFR & TRIFR Mensual', 'Tasa de Ausentismo (%)', 'Distribución de Incidentes',
        'Días Perdidos por Causa', 'Incidentes por Área y Turno', 'Riesgo por Departamento',
        'Near Miss vs LTI (Indicadores Adelantados)', 'Predicción Ausentismo Mensual', 'Causas Raíz',
    ],
    specs=[[{}, {}, {}], [{}, {'type': 'heatmap'}, {}], [{}, {}, {}]],
    vertical_spacing=0.10,
    horizontal_spacing=0.08,
)

# 1. LTIFR / TRIFR
fig_dash.add_trace(go.Scatter(x=df_kpi['fecha'], y=df_kpi['trifr'], name='TRIFR',
    fill='tozeroy', fillcolor='rgba(232,93,4,0.15)',
    line=dict(color='#E85D04', width=2)), row=1, col=1)
fig_dash.add_trace(go.Scatter(x=df_kpi['fecha'], y=df_kpi['ltifr'], name='LTIFR',
    line=dict(color='#C1121F', width=2.5, dash='dot')), row=1, col=1)

# 2. Tasa ausentismo
colores_aus = ['#C1121F' if v > 4.5 else '#F48C06' if v > 3.0 else '#2D6A4F'
               for v in df_kpi['tasa_ausentismo_pct']]
fig_dash.add_trace(go.Bar(x=df_kpi['fecha'], y=df_kpi['tasa_ausentismo_pct'],
    name='Ausentismo %', marker_color=colores_aus,
    hovertemplate='%{x|%b %Y}: %{y:.2f}%<extra></extra>'), row=1, col=2)
fig_dash.add_hline(y=3.5, line_dash='dash', line_color='#C1121F',
                   annotation_text='Objetivo 3.5%', row=1, col=2)

# 3. Pirámide incidentes
tipo_counts = df_inc.groupby('tipo_incidente').size().reset_index(name='n')
fig_dash.add_trace(go.Bar(x=tipo_counts['tipo_incidente'], y=tipo_counts['n'],
    name='Incidentes', marker_color=['#2D6A4F','#2D6A4F','#F48C06','#F48C06','#E85D04','#C1121F','#C1121F'],
    hovertemplate='%{x}: %{y}<extra></extra>'), row=1, col=3)

# 4. Días perdidos por causa
causa_dias2 = df_aus.groupby('causa')['dias_ausencia'].sum().reset_index()
fig_dash.add_trace(go.Bar(x=causa_dias2['dias_ausencia'], y=causa_dias2['causa'],
    orientation='h', name='Días perdidos',
    marker_color='#1B4F72',
    hovertemplate='%{y}: %{x:,} días<extra></extra>'), row=2, col=1)

# 5. Heatmap área × turno
hm_data = df_inc.pivot_table(index='area', columns='turno', values='es_registrable',
                              aggfunc='sum', fill_value=0)
fig_dash.add_trace(go.Heatmap(
    z=hm_data.values, x=hm_data.columns.tolist(), y=hm_data.index.tolist(),
    colorscale='Reds', name='Registrables',
    hovertemplate='%{y}<br>%{x}: %{z} incidentes<extra></extra>',
    showscale=False), row=2, col=2)

# 6. Riesgo por departamento
risk_pct2 = risk_pct.reset_index()
for nivel, col in zip(['Alto','Medio','Bajo'], ['#C1121F','#F48C06','#2D6A4F']):
    if nivel in risk_pct2.columns:
        fig_dash.add_trace(go.Bar(
            x=risk_pct2['departamento'], y=risk_pct2[nivel],
            name=f'Riesgo {nivel}', marker_color=col,
            hovertemplate=f'%{{x}}<br>Riesgo {nivel}: %{{y:.1f}}%<extra></extra>'), row=2, col=3)

# 7. Near Miss vs LTI
fig_dash.add_trace(go.Bar(x=df_kpi['fecha'], y=df_kpi['near_misses'],
    name='Near Misses', marker_color='rgba(45,106,79,0.6)',
    hovertemplate='%{x|%b %Y}: %{y} NM<extra></extra>'), row=3, col=1)
fig_dash.add_trace(go.Scatter(x=df_kpi['fecha'], y=df_kpi['lti'],
    name='LTI', line=dict(color='#C1121F', width=2),
    hovertemplate='%{x|%b %Y}: %{y} LTI<extra></extra>'), row=3, col=1)

# 8. Predicción ausentismo
x_total = list(range(len(ts)))
fig_dash.add_trace(go.Scatter(x=x_total, y=ts['dias_ausencia'].tolist(),
    name='Real', line=dict(color='#1B4F72', width=2),
    hovertemplate='Mes %{x}: %{y:.0f} días<extra></extra>'), row=3, col=2)
fig_dash.add_trace(go.Scatter(x=list(range(split, len(ts))), y=y_hat.tolist(),
    name='Predicción GBR', line=dict(color='#C1121F', width=2, dash='dash'),
    hovertemplate='Mes %{x}: %{y:.0f} días<extra></extra>'), row=3, col=2)

# 9. Causas raíz
fig_dash.add_trace(go.Bar(
    x=causa_raiz.values, y=causa_raiz.index, orientation='h',
    name='Causa raíz', marker_color='#4A4E69',
    hovertemplate='%{y}: %{x}<extra></extra>'), row=3, col=3)

# Layout corporativo
fig_dash.update_layout(
    height=1100,
    title=dict(
        text='<b>YPF-Patagonia S.A. — Dashboard HSE Predictivo | 2022–2024</b><br>'
             '<sup>Health, Safety & Environment Analytics | Data Analyst: Martín Pérez Alaniz</sup>',
        font=dict(size=18, color='#1B4F72'),
        x=0.5, xanchor='center',
    ),
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='#FFFFFF',
    font=dict(family='Arial', size=11),
    showlegend=False,
    barmode='stack',
    hovermode='closest',
    margin=dict(t=100, b=40, l=40, r=40),
)
fig_dash.write_html(DASH / 'dashboard_hse_corporativo.html')
print("  Dashboard guardado: outputs/dashboard/dashboard_hse_corporativo.html")

# ══════════════════════════════════════════
# RESUMEN FINAL
# ══════════════════════════════════════════
print("\n" + "="*55)
print("  ANALISIS HSE COMPLETADO")
print("="*55)
print(f"  Empleados analizados:  {len(df_emp):,}")
print(f"  Eventos de ausentismo: {len(df_aus):,} | {df_aus['dias_ausencia'].sum():,} dias")
print(f"  Incidentes registrados:{len(df_inc):,}")
print(f"  LTIFR promedio:        {df_kpi['ltifr'].mean():.2f}")
print(f"  TRIFR promedio:        {df_kpi['trifr'].mean():.2f}")
print(f"  Tasa ausentismo prom:  {df_kpi['tasa_ausentismo_pct'].mean():.2f}%")
print(f"  Modelo riesgo:         Accuracy {acc:.1%} | CV {cv_scores.mean():.1%}")
print(f"  Modelo ausentismo:     R2={r2_ts:.3f} | MAE={mae_ts:.0f} dias/mes")
figuras = list(FIGS.glob('*.png'))
print(f"\n  Figuras generadas: {len(figuras)}")
for f in sorted(figuras):
    print(f"    {f.name}")
print(f"\n  Dashboard HTML: outputs/dashboard/dashboard_hse_corporativo.html")
print(f"  Excel Power BI: outputs/powerbi/HSE_PowerBI_Ready.xlsx")

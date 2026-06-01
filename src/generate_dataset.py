"""
Dataset sintético realista de HSE (Health, Safety & Environment) para empresa
de petróleo y gas en Argentina (basado en parámetros reales de la industria).
Empresa ficticia: YPF-Patagonia S.A. — Cuenca Neuquina, Argentina.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

np.random.seed(42)
BASE = Path(__file__).parent.parent

# ─────────────────────────────────────────────
# 1. EMPLEADOS
# ─────────────────────────────────────────────
N_EMP = 850

departamentos = {
    'Perforación':       {'n': 180, 'riesgo_base': 0.72, 'color': '#E63946'},
    'Producción':        {'n': 220, 'riesgo_base': 0.58, 'color': '#F4A261'},
    'Mantenimiento':     {'n': 160, 'riesgo_base': 0.65, 'color': '#E9C46A'},
    'Transporte':        {'n': 110, 'riesgo_base': 0.55, 'color': '#2A9D8F'},
    'HSE':              {'n':  40, 'riesgo_base': 0.20, 'color': '#264653'},
    'Administración':    {'n':  80, 'riesgo_base': 0.10, 'color': '#6D6875'},
    'Ingeniería':        {'n':  60, 'riesgo_base': 0.30, 'color': '#457B9D'},
}

turnos = ['Diurno', 'Nocturno', 'Rotativo 14x14', 'Rotativo 7x7']
ubicaciones = ['Neuquén - Vaca Muerta', 'Mendoza - Cuyo', 'Chubut - San Jorge', 'Salta - NOA', 'Oficina Central BA']
cargos_campo = ['Operador de Campo', 'Técnico Senior', 'Supervisor', 'Ingeniero de Pozo', 'Mecánico Industrial',
                'Electricista', 'Soldador', 'Maquinista', 'Operador Grúa', 'Técnico HSE']
cargos_adm   = ['Analista', 'Coordinador', 'Gerente de Área', 'Asistente', 'Especialista']

empleados = []
emp_id = 1000
for depto, cfg in departamentos.items():
    for _ in range(cfg['n']):
        edad = int(np.random.normal(38, 9))
        edad = max(22, min(62, edad))
        antiguedad = min(edad - 22, int(np.random.exponential(7)))
        antiguedad = max(0, antiguedad)

        es_campo = depto not in ['Administración', 'Ingeniería', 'HSE']
        cargo = np.random.choice(cargos_campo if es_campo else cargos_adm)
        turno = np.random.choice(turnos, p=[0.25, 0.15, 0.40, 0.20]) if es_campo else 'Diurno'

        if depto in ['Perforación', 'Mantenimiento']:
            ubicacion = np.random.choice(ubicaciones[:4], p=[0.50, 0.20, 0.20, 0.10])
        elif depto == 'Administración':
            ubicacion = 'Oficina Central BA'
        else:
            ubicacion = np.random.choice(ubicaciones, p=[0.35, 0.20, 0.20, 0.15, 0.10])

        # Factores de riesgo individuales
        factor_edad        = 1 + max(0, (edad - 45) * 0.015)
        factor_antiguedad  = max(0.7, 1 - antiguedad * 0.02)  # más exp = menos riesgo
        factor_turno       = {'Diurno': 1.0, 'Nocturno': 1.35, 'Rotativo 14x14': 1.20, 'Rotativo 7x7': 1.15}[turno]
        capacitacion_horas = max(0, int(np.random.normal(32, 15)))  # horas anuales
        factor_cap         = max(0.6, 1 - capacitacion_horas / 200)

        riesgo_individual = (cfg['riesgo_base'] * factor_edad * factor_antiguedad *
                            factor_turno * factor_cap * np.random.uniform(0.7, 1.3))
        riesgo_individual = min(1.0, max(0.02, riesgo_individual))

        condicion_cronica = np.random.choice(['Ninguna', 'Hipertensión', 'Lumbalgia', 'Estrés crónico',
                                              'Diabetes tipo 2', 'Hipoacusia'],
                                             p=[0.60, 0.12, 0.10, 0.10, 0.05, 0.03])

        empleados.append({
            'empleado_id':         emp_id,
            'departamento':        depto,
            'cargo':               cargo,
            'edad':                edad,
            'antiguedad_anios':    antiguedad,
            'turno':               turno,
            'ubicacion':           ubicacion,
            'capacitacion_hs_año': capacitacion_horas,
            'condicion_cronica':   condicion_cronica,
            'riesgo_score':        round(riesgo_individual, 4),
            'categoria_riesgo':    'Alto' if riesgo_individual > 0.60 else 'Medio' if riesgo_individual > 0.30 else 'Bajo',
        })
        emp_id += 1

df_emp = pd.DataFrame(empleados)

# ─────────────────────────────────────────────
# 2. REGISTROS DE AUSENTISMO (2022-2024)
# ─────────────────────────────────────────────
causas_ausentismo = {
    'Enfermedad común':        {'prob': 0.42, 'dias_media': 4.5,  'dias_std': 3.0},
    'Accidente laboral':       {'prob': 0.12, 'dias_media': 12.0, 'dias_std': 8.0},
    'Enfermedad profesional':  {'prob': 0.08, 'dias_media': 18.0, 'dias_std': 10.0},
    'Licencia médica':         {'prob': 0.15, 'dias_media': 8.0,  'dias_std': 5.0},
    'Salud mental / burnout':  {'prob': 0.10, 'dias_media': 22.0, 'dias_std': 12.0},
    'Cirugía / recuperación':  {'prob': 0.05, 'dias_media': 30.0, 'dias_std': 15.0},
    'Permiso gremial':         {'prob': 0.05, 'dias_media': 2.0,  'dias_std': 1.0},
    'Otro':                    {'prob': 0.03, 'dias_media': 3.0,  'dias_std': 2.0},
}
causas_list = list(causas_ausentismo.keys())
causas_probs = [causas_ausentismo[c]['prob'] for c in causas_list]

ausencias = []
fecha_inicio = datetime(2022, 1, 1)
fecha_fin    = datetime(2024, 12, 31)

for _, emp in df_emp.iterrows():
    # Número de eventos de ausentismo según riesgo
    n_eventos = np.random.poisson(emp['riesgo_score'] * 3.5)
    for _ in range(n_eventos):
        causa = np.random.choice(causas_list, p=causas_probs)
        cfg   = causas_ausentismo[causa]
        dias  = max(1, int(np.random.normal(cfg['dias_media'], cfg['dias_std'])))
        dias  = min(dias, 90)
        dias_random = (fecha_fin - fecha_inicio).days
        fecha_inicio_aus = fecha_inicio + timedelta(days=int(np.random.uniform(0, dias_random)))
        # Estacionalidad: más ausentismo en invierno (jun-ago en Argentina)
        mes = fecha_inicio_aus.month
        factor_estacional = 1.4 if mes in [6, 7, 8] else 1.1 if mes in [5, 9] else 1.0
        if np.random.random() > (1 / factor_estacional):
            continue  # re-sample implícito vía skip

        ausencias.append({
            'empleado_id':      emp['empleado_id'],
            'departamento':     emp['departamento'],
            'ubicacion':        emp['ubicacion'],
            'turno':            emp['turno'],
            'causa':            causa,
            'fecha_inicio':     fecha_inicio_aus.strftime('%Y-%m-%d'),
            'dias_ausencia':    dias,
            'mes':              fecha_inicio_aus.month,
            'anio':             fecha_inicio_aus.year,
            'trimestre':        f"Q{(fecha_inicio_aus.month-1)//3+1}",
            'es_accidente':     1 if causa in ['Accidente laboral', 'Enfermedad profesional'] else 0,
        })

df_aus = pd.DataFrame(ausencias)

# ─────────────────────────────────────────────
# 3. REGISTROS DE INCIDENTES / ACCIDENTES
# ─────────────────────────────────────────────
tipos_incidente = {
    'Casi accidente (near miss)':     {'gravedad': 0, 'prob_relativa': 0.45},
    'Primeros auxilios':              {'gravedad': 1, 'prob_relativa': 0.22},
    'Tratamiento médico':             {'gravedad': 2, 'prob_relativa': 0.14},
    'Tiempo perdido (LTI)':           {'gravedad': 3, 'prob_relativa': 0.10},
    'Incapacidad permanente parcial': {'gravedad': 4, 'prob_relativa': 0.05},
    'Fatalidad':                      {'gravedad': 5, 'prob_relativa': 0.01},
    'Incidente ambiental':            {'gravedad': 2, 'prob_relativa': 0.03},
}
tipos_list  = list(tipos_incidente.keys())
tipos_probs = [tipos_incidente[t]['prob_relativa'] for t in tipos_list]

causas_raiz = ['Acto inseguro', 'Condición insegura', 'Falla de equipo',
               'Procedimiento inadecuado', 'Fatiga/turno extendido',
               'Comunicación deficiente', 'Falta de EPP', 'Condición climática']

areas_peligro = ['Pozos / Drilling', 'Planta compresora', 'Tanques / Almacenamiento',
                 'Transporte en ruta', 'Taller mecánico', 'Área eléctrica', 'Oficina / Comedor']

incidentes = []
for _, emp in df_emp.iterrows():
    n_inc = np.random.poisson(emp['riesgo_score'] * 1.8)
    for _ in range(n_inc):
        tipo  = np.random.choice(tipos_list, p=tipos_probs)
        dias_random = (fecha_fin - fecha_inicio).days
        fecha_inc = fecha_inicio + timedelta(days=int(np.random.uniform(0, dias_random)))
        hora = int(np.random.choice(range(24), p=[
            0.01,0.01,0.01,0.01,0.01,0.02,  # 0-5h
            0.04,0.06,0.07,0.07,0.07,0.07,  # 6-11h
            0.06,0.06,0.07,0.07,0.06,0.05,  # 12-17h
            0.05,0.04,0.03,0.03,0.02,0.01   # 18-23h
        ]))
        dias_perdidos = 0
        if tipo == 'Tiempo perdido (LTI)':
            dias_perdidos = max(1, int(np.random.exponential(8)))
        elif tipo == 'Incapacidad permanente parcial':
            dias_perdidos = max(30, int(np.random.normal(90, 30)))

        incidentes.append({
            'empleado_id':      emp['empleado_id'],
            'departamento':     emp['departamento'],
            'ubicacion':        emp['ubicacion'],
            'turno':            emp['turno'],
            'tipo_incidente':   tipo,
            'gravedad':         tipos_incidente[tipo]['gravedad'],
            'causa_raiz':       np.random.choice(causas_raiz),
            'area':             np.random.choice(areas_peligro),
            'fecha':            fecha_inc.strftime('%Y-%m-%d'),
            'hora':             hora,
            'mes':              fecha_inc.month,
            'anio':             fecha_inc.year,
            'trimestre':        f"Q{(fecha_inc.month-1)//3+1}",
            'dias_perdidos':    dias_perdidos,
            'es_registrable':   1 if tipos_incidente[tipo]['gravedad'] >= 2 else 0,
            'es_lti':           1 if tipo == 'Tiempo perdido (LTI)' else 0,
        })

df_inc = pd.DataFrame(incidentes)

# ─────────────────────────────────────────────
# 4. KPIs MENSUALES AGREGADOS
# ─────────────────────────────────────────────
meses = pd.date_range('2022-01-01', '2024-12-01', freq='MS')
kpis = []
horas_hombre_mes = N_EMP * 190  # ~190 h/mes por empleado

for fecha in meses:
    mes = fecha.month
    anio = fecha.year
    inc_mes = df_inc[(df_inc['mes'] == mes) & (df_inc['anio'] == anio)]
    aus_mes = df_aus[(df_aus['mes'] == mes) & (df_aus['anio'] == anio)]

    lti = inc_mes['es_lti'].sum()
    registrables = inc_mes['es_registrable'].sum()
    dias_perdidos = inc_mes['dias_perdidos'].sum()
    near_misses = (inc_mes['tipo_incidente'] == 'Casi accidente (near miss)').sum()
    dias_ausencia = aus_mes['dias_ausencia'].sum()

    tasa_aus = dias_ausencia / (N_EMP * 22) * 100 if N_EMP > 0 else 0
    ltifr = lti * 1_000_000 / horas_hombre_mes if horas_hombre_mes > 0 else 0
    trifr = registrables * 1_000_000 / horas_hombre_mes if horas_hombre_mes > 0 else 0

    kpis.append({
        'fecha':                 fecha.strftime('%Y-%m-%d'),
        'mes':                   mes,
        'anio':                  anio,
        'trimestre':             f"Q{(mes-1)//3+1}",
        'horas_hombre':          horas_hombre_mes,
        'incidentes_total':      len(inc_mes),
        'near_misses':           near_misses,
        'registrables':          registrables,
        'lti':                   lti,
        'dias_perdidos':         dias_perdidos,
        'dias_ausencia_total':   dias_ausencia,
        'tasa_ausentismo_pct':   round(tasa_aus, 3),
        'ltifr':                 round(ltifr, 4),
        'trifr':                 round(trifr, 4),
        'ratio_nm_a_lti':        round(near_misses / max(lti, 1), 1),
    })

df_kpi = pd.DataFrame(kpis)

# ─────────────────────────────────────────────
# 5. GUARDAR ARCHIVOS
# ─────────────────────────────────────────────
out = BASE / 'data' / 'processed'
df_emp.to_csv(out / 'empleados.csv', index=False)
df_aus.to_csv(out / 'ausentismo.csv', index=False)
df_inc.to_csv(out / 'incidentes.csv', index=False)
df_kpi.to_csv(out / 'kpis_mensuales.csv', index=False)

# Excel para Power BI
with pd.ExcelWriter(BASE / 'outputs' / 'powerbi' / 'HSE_PowerBI_Ready.xlsx', engine='openpyxl') as writer:
    df_emp.to_excel(writer, sheet_name='Empleados', index=False)
    df_aus.to_excel(writer, sheet_name='Ausentismo', index=False)
    df_inc.to_excel(writer, sheet_name='Incidentes', index=False)
    df_kpi.to_excel(writer, sheet_name='KPIs_Mensuales', index=False)

print("Dataset HSE generado:")
print(f"  Empleados:   {len(df_emp):,}")
print(f"  Ausentismo:  {len(df_aus):,} eventos | {df_aus['dias_ausencia'].sum():,} dias totales")
print(f"  Incidentes:  {len(df_inc):,} registros")
print(f"  KPIs:        {len(df_kpi)} meses")
print(f"  LTIFR prom:  {df_kpi['ltifr'].mean():.2f}")
print(f"  TRIFR prom:  {df_kpi['trifr'].mean():.2f}")
print(f"  Tasa aus.:   {df_kpi['tasa_ausentismo_pct'].mean():.2f}%")
print(f"  Excel Power BI: outputs/powerbi/HSE_PowerBI_Ready.xlsx")

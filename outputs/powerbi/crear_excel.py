import numpy as np, pandas as pd
from pathlib import Path

np.random.seed(42)
N=850
dates=pd.date_range('2022-01-01','2024-12-01',freq='MS')
hh=N*190

# KPIs mensuales
kpis=[]
for d in dates:
    lti=max(0,int(np.random.poisson(1.2)))
    reg=lti+max(0,int(np.random.poisson(2.5)))
    nm=max(0,int(np.random.poisson(8)))
    dp=lti*max(1,int(np.random.exponential(6)))
    da=max(0,int(np.random.normal(280,60)))
    tas=round(da/(N*22)*100,3)
    kpis.append({'fecha':d.strftime('%Y-%m-%d'),'mes':d.month,'anio':d.year,
                 'trimestre':f'Q{(d.month-1)//3+1}','horas_hombre':hh,
                 'incidentes_total':nm+reg,'near_misses':nm,'registrables':reg,
                 'lti':lti,'dias_perdidos':dp,'dias_ausencia_total':da,
                 'tasa_ausentismo_pct':tas,
                 'ltifr':round(lti*1e6/hh,4),
                 'trifr':round(reg*1e6/hh,4),
                 'ratio_nm_a_lti':round(nm/max(lti,1),1)})
df_kpi=pd.DataFrame(kpis)

# Empleados
deptos=['Perforacion','Produccion','Mantenimiento','Transporte','HSE','Administracion','Ingenieria']
turnos=['Diurno','Nocturno','Rotativo 14x14','Rotativo 7x7']
emp=[]
for i in range(N):
    d=np.random.choice(deptos,p=[0.21,0.26,0.19,0.13,0.05,0.09,0.07])
    edad=max(22,min(62,int(np.random.normal(38,9))))
    ant=max(0,min(edad-22,int(np.random.exponential(7))))
    turno=np.random.choice(turnos,p=[0.25,0.15,0.40,0.20]) if d not in ['Administracion','Ingenieria','HSE'] else 'Diurno'
    cap=max(0,int(np.random.normal(32,15)))
    rs=min(1.0,max(0.05,np.random.beta(2,3)))
    cat='Alto' if rs>0.6 else 'Medio' if rs>0.3 else 'Bajo'
    emp.append({'empleado_id':1000+i,'departamento':d,'cargo':'Operador','edad':edad,
                'antiguedad_anios':ant,'turno':turno,'ubicacion':'Neuquen - Vaca Muerta',
                'capacitacion_hs_ano':cap,'condicion_cronica':'Ninguna',
                'riesgo_score':round(rs,4),'categoria_riesgo':cat})
df_emp=pd.DataFrame(emp)

# Incidentes
tipos=['Casi accidente (near miss)','Primeros auxilios','Tratamiento medico',
       'Tiempo perdido (LTI)','Incapacidad permanente','Fatalidad','Incidente ambiental']
causas=['Acto inseguro','Condicion insegura','Falla de equipo','Procedimiento inadecuado',
        'Fatiga','Comunicacion deficiente','Falta de EPP','Condicion climatica']
areas=['Pozos / Drilling','Planta compresora','Tanques / Almacenamiento','Transporte en ruta',
       'Taller mecanico','Area electrica','Oficina']
inc=[]
for _, e in df_emp.iterrows():
    for _ in range(max(0,int(np.random.poisson(e['riesgo_score']*1.5)))):
        t=np.random.choice(tipos,p=[0.45,0.22,0.14,0.10,0.05,0.01,0.03])
        fd=pd.Timestamp('2022-01-01')+pd.Timedelta(days=int(np.random.uniform(0,1095)))
        dp=max(1,int(np.random.exponential(7))) if t=='Tiempo perdido (LTI)' else 0
        inc.append({'empleado_id':int(e['empleado_id']),'departamento':e['departamento'],
                    'ubicacion':e['ubicacion'],'turno':e['turno'],'tipo_incidente':t,
                    'gravedad':tipos.index(t),'causa_raiz':np.random.choice(causas),
                    'area':np.random.choice(areas),'fecha':fd.strftime('%Y-%m-%d'),
                    'hora':int(np.random.choice(range(24))),'mes':fd.month,'anio':fd.year,
                    'dias_perdidos':dp,
                    'es_registrable':1 if tipos.index(t)>=2 else 0,
                    'es_lti':1 if t=='Tiempo perdido (LTI)' else 0})
df_inc=pd.DataFrame(inc)

# Ausentismo
causas_aus=['Enfermedad comun','Accidente laboral','Enfermedad profesional','Licencia medica',
            'Salud mental / burnout','Cirugia / recuperacion','Permiso gremial','Otro']
aus=[]
for _, e in df_emp.iterrows():
    for _ in range(max(0,int(np.random.poisson(e['riesgo_score']*3)))):
        c=np.random.choice(causas_aus,p=[0.42,0.12,0.08,0.15,0.10,0.05,0.05,0.03])
        dias=max(1,min(90,int(np.random.exponential(8))))
        fd=pd.Timestamp('2022-01-01')+pd.Timedelta(days=int(np.random.uniform(0,1095)))
        aus.append({'empleado_id':int(e['empleado_id']),'departamento':e['departamento'],
                    'ubicacion':e['ubicacion'],'turno':e['turno'],'causa':c,
                    'fecha_inicio':fd.strftime('%Y-%m-%d'),'dias_ausencia':dias,
                    'mes':fd.month,'anio':fd.year,
                    'es_accidente':1 if c in ['Accidente laboral','Enfermedad profesional'] else 0})
df_aus=pd.DataFrame(aus)

out=Path(r'C:\Users\mpere\Documents\hse-oilgas-predictive-analytics\outputs\powerbi')
out.mkdir(parents=True,exist_ok=True)
xlsx=out/'HSE_PowerBI_Ready.xlsx'
with pd.ExcelWriter(xlsx,engine='openpyxl') as w:
    df_emp.to_excel(w,sheet_name='Empleados',index=False)
    df_inc.to_excel(w,sheet_name='Incidentes',index=False)
    df_aus.to_excel(w,sheet_name='Ausentismo',index=False)
    df_kpi.to_excel(w,sheet_name='KPIs_Mensuales',index=False)

print(f"Excel creado: {xlsx.stat().st_size//1024} KB")
print(f"Empleados:{len(df_emp)} | Incidentes:{len(df_inc)} | Ausencias:{len(df_aus)} | KPIs:{len(df_kpi)}")

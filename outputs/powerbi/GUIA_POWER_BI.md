# Guía Power BI — Dashboard HSE Oil & Gas
## De cero al dashboard en 15 pasos

---

## ANTES DE EMPEZAR

Necesitás:
- **Power BI Desktop** (gratis): powerbi.microsoft.com/desktop
- El archivo Excel: `HSE_PowerBI_Ready.xlsx` (está en esta misma carpeta)
- El tema JSON: `tema_corporativo_hse.json` (misma carpeta)

---

## PASO 1 — Abrir Power BI y aplicar el tema corporativo

1. Abrir Power BI Desktop
2. Ir a la pestaña **Vista** (View) en el menú superior
3. Clic en **Temas** → **Examinar temas**
4. Seleccionar el archivo `tema_corporativo_hse.json`
5. Clic en **Aceptar** → el reporte ya tiene los colores corporativos

---

## PASO 2 — Importar el Excel

1. Clic en **Obtener datos** (botón principal o menú Inicio)
2. Seleccionar **Excel**
3. Navegar a `outputs/powerbi/HSE_PowerBI_Ready.xlsx`
4. En el Navegador que aparece, tildar las 4 hojas:
   - ✅ **Empleados**
   - ✅ **Incidentes**
   - ✅ **Ausentismo**
   - ✅ **KPIs_Mensuales**
5. Clic en **Cargar**

---

## PASO 3 — Crear relaciones entre tablas

1. Ir a la vista **Modelo** (ícono de diagrama, barra lateral izquierda)
2. Verás las 4 tablas como cajas
3. Crear estas relaciones arrastrando campos:
   - `Empleados[empleado_id]` → `Incidentes[empleado_id]` (1 a muchos)
   - `Empleados[empleado_id]` → `Ausentismo[empleado_id]` (1 a muchos)
4. Las relaciones deben quedar con la flecha apuntando desde Empleados hacia las otras tablas

---

## PASO 4 — Agregar todas las medidas DAX

1. En la vista **Datos** (tabla), seleccionar la tabla `KPIs_Mensuales`
2. Ir a **Modelado** → **Nueva medida**
3. Copiar y pegar cada medida del archivo `DAX_Medidas.txt`
4. Repetir para cada medida (hay ~25 medidas en total)
5. Para las medidas de Incidentes, seleccionar primero la tabla `Incidentes`
6. Para las de Ausentismo, seleccionar `Ausentismo`, etc.

**Tip:** Podés crear una tabla vacía llamada `_Medidas` y poner todas ahí:
- Modelado → Escribir datos → tabla con 1 columna, 1 fila vacía, nombre `_Medidas`
- Agregar todas las medidas a esa tabla para tenerlas organizadas

---

## PASO 5 — Crear la página "Portada Ejecutiva"

**Renombrar la página:** doble clic en "Página 1" → escribir `Dashboard Ejecutivo`

### 5.1 — Encabezado corporativo
- Insertar → **Cuadro de texto**
- Escribir: `YPF-Patagonia S.A. — Dashboard HSE | 2022–2024`
- Fuente: Segoe UI, 20pt, negrita, color `#1B4F72`
- Debajo: subtítulo `Health, Safety & Environment Analytics`, 13pt, color `#4A4E69`

### 5.2 — 4 tarjetas KPI en la fila superior
Insertar 4 visuales tipo **Tarjeta** (Card):

| Posición | Campo | Medida |
|----------|-------|--------|
| 1° (izq) | `LTIFR Promedio` | Llamar "LTIFR Promedio" |
| 2° | `TRIFR Promedio` | Llamar "TRIFR Promedio" |
| 3° | `Tasa Ausentismo %` | Llamar "Tasa Ausentismo" |
| 4° (der) | `% Riesgo Alto` | Llamar "% Empleados Riesgo Alto" |

Para cada tarjeta:
- Formato → Valor de llamada → 2 decimales
- Formato → Etiqueta de categoría → visible, texto descriptivo
- Agregar **borde izquierdo** de color: LTIFR=rojo, TRIFR=naranja, Aus=amarillo, Riesgo=azul

### 5.3 — Gráfico de líneas: LTIFR y TRIFR mensual
- Visual: **Gráfico de líneas**
- Eje X: `KPIs_Mensuales[fecha]` (nivel: Mes)
- Valores: `LTIFR Promedio` y `TRIFR Promedio`
- Colores: LTIFR = `#C1121F`, TRIFR = `#E85D04`
- Título: "Evolución de Frecuencia de Incidentes"
- Agregar línea de referencia en Y=1.5 (benchmark clase mundial)

### 5.4 — Gráfico de barras: Tasa ausentismo mensual
- Visual: **Gráfico de barras agrupadas**
- Eje X: `KPIs_Mensuales[fecha]` (Mes)
- Valores: `Tasa Ausentismo %`
- Agregar línea constante en Y=3.5 (objetivo)
- Formato condicional: rojo si > 4.5, naranja si > 3.0, verde si ≤ 3.0

### 5.5 — Gráfico de barras horizontal: Incidentes por departamento
- Visual: **Gráfico de barras apiladas horizontal**
- Eje Y: `Incidentes[departamento]`
- Valores: `Total Incidentes`
- Leyenda: `Incidentes[tipo_incidente]`
- Ordenar por valor descendente

### 5.6 — Filtro de año (Slicer)
- Visual: **Segmentación de datos**
- Campo: `KPIs_Mensuales[anio]`
- Estilo: Lista o desplegable
- Ubicar en esquina superior derecha
- Este filtro afecta a todos los visuales de la página automáticamente

---

## PASO 6 — Crear la página "Análisis de Incidentes"

Clic derecho en tab → **Nueva página** → Renombrar: `Análisis de Incidentes`

### 6.1 — Pirámide de Bird (barras horizontales)
- Visual: **Gráfico de barras apiladas horizontal**
- Eje Y: `Incidentes[tipo_incidente]`
- Valores: `Total Incidentes`
- Ordenar por valor: Near Miss primero (más largo), Fatalidad último
- Colores manuales: Near Miss=verde, Primeros Auxilios=amarillo, LTI=naranja, Fatalidad=rojo

### 6.2 — Tabla de incidentes por área y turno (Heatmap manual)
- Visual: **Matriz**
- Filas: `Incidentes[area]`
- Columnas: `Incidentes[turno]`
- Valores: `Incidentes Registrables`
- Formato → Formato condicional → Color de fondo → escala de colores blanco→rojo

### 6.3 — Gráfico de incidentes por hora del día
- Visual: **Gráfico de columnas agrupadas**
- Eje X: `Incidentes[hora]` (0 a 23)
- Valores: `Total Incidentes`
- Resaltar manualmente las horas 22-6 con color rojo (turno nocturno)
- Título: "Incidentes por Hora — Riesgo Nocturno"

### 6.4 — Gráfico de dona: Causas raíz
- Visual: **Gráfico de anillos** (Donut)
- Leyenda: `Incidentes[causa_raiz]`
- Valores: `Total Incidentes`
- Colores: el tema corporativo se aplica automáticamente

### 6.5 — Tarjetas de detalle
Agregar 3 tarjetas pequeñas:
- `Total Incidentes`
- `Incidentes Registrables`
- `Total LTI`

---

## PASO 7 — Crear la página "Ausentismo"

Nueva página → `Análisis de Ausentismo`

### 7.1 — Barras: Días perdidos por causa
- Visual: **Gráfico de barras horizontal**
- Eje Y: `Ausentismo[causa]`
- Valores: `Total Dias Ausencia`
- Resaltar en rojo: Accidente laboral, Enfermedad profesional, Salud mental

### 7.2 — Líneas: Tendencia mensual ausentismo por año
- Visual: **Gráfico de líneas**
- Eje X: `Ausentismo[mes]` (1 a 12)
- Valores: `Total Dias Ausencia`
- Leyenda: `Ausentismo[anio]`
- Colores: 2022=azul, 2023=naranja, 2024=rojo

### 7.3 — Matriz: Ausentismo departamento × mes (Heatmap)
- Visual: **Matriz**
- Filas: `Ausentismo[departamento]`
- Columnas: `Ausentismo[mes]`
- Valores: `Total Dias Ausencia`
- Formato condicional: escala blanco → rojo oscuro

### 7.4 — Tarjetas de resumen
- `Total Dias Ausencia`
- `Total Eventos Ausentismo`
- `Promedio Dias por Evento`
- `% Origen Laboral`

---

## PASO 8 — Crear la página "Mapa de Riesgo Individual"

Nueva página → `Riesgo por Empleado`

### 8.1 — Gráfico de dispersión: edad vs score riesgo
- Visual: **Gráfico de dispersión**
- Eje X: `Empleados[edad]`
- Eje Y: `Empleados[riesgo_score]`
- Leyenda: `Empleados[categoria_riesgo]`
- Tamaño: `Empleados[antiguedad_anios]`
- Colores: Alto=rojo, Medio=naranja, Bajo=verde

### 8.2 — Barras 100% apiladas: riesgo por departamento
- Visual: **Gráfico de barras 100% apiladas**
- Eje Y: `Empleados[departamento]`
- Valores: `Total Empleados`
- Leyenda: `Empleados[categoria_riesgo]`
- Colores: Alto=`#C1121F`, Medio=`#F48C06`, Bajo=`#2D6A4F`

### 8.3 — Tabla detalle empleados en riesgo alto
- Visual: **Tabla**
- Columnas: `departamento`, `turno`, `ubicacion`, `condicion_cronica`, `capacitacion_hs_año`, `riesgo_score`
- Filtrar: `categoria_riesgo = "Alto"`
- Ordenar por `riesgo_score` descendente
- Agregar formato condicional en `riesgo_score`: gradiente verde→rojo

### 8.4 — Segmentaciones
- Slicer: `Empleados[departamento]`
- Slicer: `Empleados[categoria_riesgo]`
- Slicer: `Empleados[turno]`

---

## PASO 9 — Agregar logo corporativo (opcional)

1. Insertar → **Imagen**
2. Podés usar cualquier logo PNG de YPF o crear uno simple con el nombre de la empresa
3. Ubicar en esquina superior izquierda de cada página

---

## PASO 10 — Publicar en Power BI Service (opcional)

Si tenés cuenta Microsoft 365 o Power BI Pro:
1. Inicio → **Publicar**
2. Seleccionar tu workspace
3. El dashboard queda accesible desde cualquier navegador y el celular

---

## RESULTADO FINAL

Tu dashboard de Power BI tendrá 4 páginas:
1. **Dashboard Ejecutivo** — KPIs, LTIFR/TRIFR, ausentismo, incidentes por depto
2. **Análisis de Incidentes** — Pirámide Bird, heatmaps, hora, causas raíz
3. **Análisis de Ausentismo** — Por causa, tendencia, heatmap depto×mes
4. **Mapa de Riesgo** — Scatter empleados, barras 100%, tabla de alto riesgo

Todos los filtros (año, departamento, turno) funcionan en cascada entre páginas.

---

## ARCHIVOS EN ESTA CARPETA

| Archivo | Para qué sirve |
|---------|---------------|
| `HSE_PowerBI_Ready.xlsx` | Datos — importar en Paso 2 |
| `tema_corporativo_hse.json` | Tema — aplicar en Paso 1 |
| `DAX_Medidas.txt` | Fórmulas — copiar en Paso 4 |
| `GUIA_POWER_BI.md` | Esta guía |

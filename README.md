# 🌬️ Dashboard Interactivo de Calidad del Aire en Chile

## 📋 Descripción del Proyecto

Este proyecto implementa un **dashboard interactivo** para el análisis integral de la calidad del aire en Chile, combinando datos de estaciones de monitoreo, fuentes de emisiones contaminantes y estadísticas poblacionales. Desarrollado con **Dash/Plotly** y **Python**, ofrece visualizaciones dinámicas y análisis correlacionales para apoyar la toma de decisiones en políticas ambientales.

### 🎯 Objetivos Principales

- **Visualización Interactiva**: Mapas y gráficos dinámicos de calidad del aire por región
- **Análisis Temporal**: Evolución de contaminantes por estación de monitoreo
- **Análisis de Fuentes**: Caracterización de emisiones por tipo (difusas, puntuales, móviles)
- **Correlaciones**: Relaciones entre contaminación, población y actividad industrial
- **Insights Regionales**: Identificación de patrones y tendencias por región

## 🚀 Funcionalidades Implementadas

### ✅ **Completamente Funcional**

#### 🗺️ **Pestaña 1: Estaciones de Monitoreo**
- **Mapa interactivo** de Chile con datos de calidad del aire
- **Visualización por colores** según niveles de PM2.5 (estándar AQI)
- **Análisis temporal** detallado por estación seleccionada
- **Filtros por rango de años** (2019-2023)
- **Información regional**: población, emisiones y conclusiones
- **Gráficos multi-contaminante**: PM2.5, PM10, O3, NO2, CO, SO2

#### 🏭 **Pestaña 2: Fuentes de Contaminación**
- **Análisis por región**: emisiones totales por área geográfica
- **Análisis por tipo de fuente**: difusas, puntuales (EFP), en ruta (TR)
- **Evolución temporal**: tendencias de emisiones a lo largo del tiempo
- **Estadísticas detalladas**: totales, promedios y porcentajes
- **Filtros dinámicos**: por región y tipo de análisis

#### 📊 **Pestaña 3: Análisis de Correlación**
- **Matriz de correlación**: Pearson entre todas las variables
- **Población vs Contaminación**: análisis de dispersión regional
- **Emisiones vs Calidad del Aire**: relaciones causa-efecto
- **Análisis temporal de correlaciones**: evolución de relaciones
- **Insights automáticos**: interpretación estadística de resultados

## 📊 Estructura de Datos

### 📈 **Datos de Calidad del Aire**
- **Fuente**: Estaciones de monitoreo ambiental
- **Período**: 2014-2023
- **Regiones**: 16 regiones de Chile
- **Estaciones**: 39 estaciones de monitoreo
- **Contaminantes**: PM2.5, PM10, O3, NO2, CO, SO2
- **Registros**: 132,913 mediciones

### 🏭 **Datos de Emisiones**
- **Fuente**: Registro de Emisiones y Transferencia de Contaminantes (RETC)
- **Período**: 2019-2022
- **Tipos**: Difusas, Puntuales (EFP), En Ruta (TR)
- **Registros**: 5,223,049 entradas
- **Unidad**: Toneladas por año

### 👥 **Datos Poblacionales**
- **Fuente**: Instituto Nacional de Estadísticas (INE)
- **Período**: 2002-2035 (proyecciones)
- **Granularidad**: Por región y año
- **Registros**: 544 datos regionales

## 🛠️ Instalación y Configuración

### 📋 **Prerrequisitos**
```bash
Python 3.8+
pip (gestor de paquetes)
```

### ⚡ **Instalación Rápida**

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd analisis-compcientifica
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Procesar datos (IMPORTANTE)**:
```bash
# Ejecutar scripts ETL en orden
python data_processing/etl_air_quality_stations.py
python data_processing/etl_emission_sources.py
python data_processing/etl_population.py
```

5. **Ejecutar dashboard**:
```bash
python app.py
```

6. **Acceder**: Abrir navegador en `http://localhost:8050`

## 📁 Estructura del Proyecto

```
analisis-compcientifica/
├── 📱 app.py                    # Aplicación principal
├── 🔧 callbacks.py             # Logic callbacks de Dash
├── 📊 charts.py                # Funciones de gráficos
├── 🧩 components.py            # Componentes UI
├── ⚙️ config.py                # Configuraciones
├── 📋 requirements.txt         # Dependencias
├── 📖 README.md               # Documentación
├── data/                      # Datos del proyecto
│   ├── raw/                   # Datos originales
│   │   ├── AirQualitySM/     # Estaciones calidad aire
│   │   ├── RECT/             # Datos emisiones
│   │   └── population/       # Datos población
│   └── processed/            # Datos procesados (.pkl)
├── data_processing/          # Scripts ETL
│   ├── etl_air_quality_stations.py
│   ├── etl_emission_sources.py
│   └── etl_population.py
└── notebooks/               # Jupyter notebooks de análisis
```

## 🎮 Guía de Uso

### 🗺️ **Pestaña Estaciones de Monitoreo**

1. **Explorar el Mapa**:
   - Colores indican niveles de PM2.5 (verde=bueno, rojo=malo)
   - Click en regiones para seleccionar
   - Filtrar por rango de años

2. **Análisis Regional**:
   - Información poblacional y de emisiones
   - Selección de estaciones disponibles

3. **Análisis Temporal**:
   - Gráficos por contaminante
   - Evolución en el tiempo
   - Información detallada de mediciones

### 🏭 **Pestaña Fuentes de Contaminación**

1. **Seleccionar Tipo de Análisis**:
   - **Por Región**: Emisiones totales por área
   - **Por Tipo de Fuente**: Distribución difusas/puntuales/ruta
   - **Evolución Temporal**: Tendencias anuales

2. **Aplicar Filtros**:
   - Filtrar por región específica
   - Ajustar rango de años

3. **Interpretar Resultados**:
   - Estadísticas en panel lateral
   - Identificar principales fuentes contaminantes

### 📊 **Pestaña Análisis de Correlación**

1. **Seleccionar Análisis**:
   - **Matriz General**: Correlaciones entre todas las variables
   - **Población vs Contaminación**: Relación demográfica
   - **Emisiones vs Calidad**: Impacto directo
   - **Temporal**: Evolución de correlaciones

2. **Configurar Variables**:
   - Seleccionar contaminantes de interés
   - Incluir variables poblacionales/emisiones

3. **Interpretar Insights**:
   - Correlaciones fuertes (>0.7) vs débiles (<0.3)
   - Relaciones positivas vs negativas
   - Implicaciones para políticas públicas

## 🔬 Metodología Técnica

### 📊 **Procesamiento de Datos**
- **ETL Pipeline**: Extracción, transformación y carga automatizada
- **Normalización**: Estandarización de nombres de regiones
- **Validación**: Verificación de consistencia entre datasets
- **Optimización**: Almacenamiento en pickle para acceso rápido

### 🎨 **Visualizaciones**
- **Mapas Interactivos**: Plotly Scattermapbox con OpenStreetMap
- **Gráficos Temporales**: Series de tiempo multi-variable
- **Análisis Estadístico**: Matrices de correlación y scatter plots
- **UI Responsiva**: Bootstrap para diseño adaptativo

### ⚡ **Arquitectura**
- **Frontend**: Dash + Bootstrap Components
- **Backend**: Python + Pandas + NumPy
- **Visualización**: Plotly.js
- **Datos**: Pickle files para performance óptima

## 📈 Insights Principales

### 🔍 **Hallazgos Clave**

1. **Calidad del Aire**:
   - PM2.5 más alto en zonas urbanas e industriales
   - Variabilidad estacional significativa
   - Mejores condiciones en regiones australes

2. **Fuentes de Emisión**:
   - Fuentes puntuales: mayor concentración industrial
   - Fuentes móviles: impacto urbano significativo
   - Fuentes difusas: distribuidas regionalmente

3. **Correlaciones**:
   - Población correlaciona moderadamente con contaminación
   - Emisiones industriales impactan directamente calidad del aire
   - Factores geográficos moderan relaciones

## 🚧 Desarrollo Futuro

### 🎯 **Próximas Funcionalidades**
- [ ] **Predicción**: Modelos ML para forecasting
- [ ] **Alertas**: Sistema de notificaciones por umbral
- [ ] **Comparación**: Benchmarking internacional
- [ ] **Mobile**: Versión responsive mejorada
- [ ] **API**: Endpoints para integración externa

### 🔧 **Mejoras Técnicas**
- [ ] **Performance**: Optimización con Dask
- [ ] **Base de Datos**: Migración a PostgreSQL
- [ ] **Testing**: Suite de tests automatizados
- [ ] **CI/CD**: Pipeline de deployment
- [ ] **Docker**: Containerización completa

## 🤝 Contribuciones

### 🛠️ **Para Desarrolladores**

1. **Fork** el repositorio
2. **Crear rama** feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. **Push** rama: `git push origin feature/nueva-funcionalidad`
5. **Pull Request** con descripción detallada

### 📋 **Estándares de Código**
- **PEP 8**: Estilo de código Python
- **Docstrings**: Documentación de funciones
- **Type Hints**: Anotaciones de tipos
- **Comments**: Comentarios en español para funcionalidad compleja

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores y Reconocimientos

### 🏆 **Desarrollado por**
- **Análisis y Desarrollo**: Equipo de Computación Científica
- **Datos**: SINCA, RETC, INE Chile
- **Tecnologías**: Plotly Dash Community

### 🙏 **Agradecimientos**
- **SINCA**: Sistema de Información Nacional de Calidad del Aire
- **MMA**: Ministerio del Medio Ambiente de Chile
- **INE**: Instituto Nacional de Estadísticas
- **Comunidad Open Source**: Plotly, Pandas, NumPy

## 📞 Soporte y Contacto

### 🆘 **Problemas Comunes**

**Error al cargar datos**:
```bash
# Ejecutar ETL scripts
python data_processing/etl_air_quality_stations.py
python data_processing/etl_emission_sources.py
python data_processing/etl_population.py
```

**Puerto en uso**:
```bash
# Cambiar puerto en app.py línea final
app.run_server(port=8051)  # Usar puerto diferente
```

**Dependencias faltantes**:
```bash
pip install -r requirements.txt --upgrade
```

### 📧 **Contacto**
- **Issues**: Reportar en GitHub Issues
- **Documentación**: Wiki del repositorio
- **Comunidad**: Discussions del proyecto

---

## 🌟 ¡Gracias por usar nuestro Dashboard de Calidad del Aire!

**Si este proyecto te resulta útil, considera darle una ⭐ en GitHub**

---

*Última actualización: Diciembre 2024*
*Versión: 1.0.0*
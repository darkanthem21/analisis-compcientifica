import os
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ===== CONFIGURACIÓN Y DATOS GEOGRÁFICOS =====

def get_chile_regions_geojson():
    """Obtiene el GeoJSON de regiones de Chile desde archivo o fallback"""

    # Intentar cargar el archivo GeoJSON real
    script_dir = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(script_dir, 'data', 'chile_regiones.geojson')

    if os.path.exists(geojson_path):
        try:
            with open(geojson_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error cargando GeoJSON: {e}")

    # Fallback con coordenadas mejoradas y más propiedades
    return {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature",
             "properties": {
                 "region": "Arica y Parinacota",
                 "codigo": "XV",
                 "superficie": 16873.3,
                 "capital": "Arica"
             },
             "geometry": {"type": "Point", "coordinates": [-70.2979, -18.4746]}},
            {"type": "Feature",
             "properties": {
                 "region": "Tarapacá",
                 "codigo": "I",
                 "superficie": 42225.8,
                 "capital": "Iquique"
             },
             "geometry": {"type": "Point", "coordinates": [-70.1522, -20.2133]}},
            {"type": "Feature",
             "properties": {
                 "region": "Antofagasta",
                 "codigo": "II",
                 "superficie": 126049.1,
                 "capital": "Antofagasta"
             },
             "geometry": {"type": "Point", "coordinates": [-70.3975, -23.6509]}},
            {"type": "Feature",
             "properties": {
                 "region": "Atacama",
                 "codigo": "III",
                 "superficie": 75176.2,
                 "capital": "Copiapó"
             },
             "geometry": {"type": "Point", "coordinates": [-70.3323, -27.3668]}},
            {"type": "Feature",
             "properties": {
                 "region": "Coquimbo",
                 "codigo": "IV",
                 "superficie": 40579.9,
                 "capital": "La Serena"
             },
             "geometry": {"type": "Point", "coordinates": [-71.3395, -29.9533]}},
            {"type": "Feature",
             "properties": {
                 "region": "Valparaíso",
                 "codigo": "V",
                 "superficie": 16396.1,
                 "capital": "Valparaíso"
             },
             "geometry": {"type": "Point", "coordinates": [-71.6197, -33.0458]}},
            {"type": "Feature",
             "properties": {
                 "region": "O'Higgins",
                 "codigo": "VI",
                 "superficie": 16387.0,
                 "capital": "Rancagua"
             },
             "geometry": {"type": "Point", "coordinates": [-70.7444, -34.1708]}},
            {"type": "Feature",
             "properties": {
                 "region": "Maule",
                 "codigo": "VII",
                 "superficie": 30296.1,
                 "capital": "Talca"
             },
             "geometry": {"type": "Point", "coordinates": [-71.6554, -35.4264]}},
            {"type": "Feature",
             "properties": {
                 "region": "Ñuble",
                 "codigo": "XVI",
                 "superficie": 13178.5,
                 "capital": "Chillán"
             },
             "geometry": {"type": "Point", "coordinates": [-72.1025, -36.6096]}},
            {"type": "Feature",
             "properties": {
                 "region": "Biobío",
                 "codigo": "VIII",
                 "superficie": 23890.2,
                 "capital": "Concepción"
             },
             "geometry": {"type": "Point", "coordinates": [-73.0444, -36.8201]}},
            {"type": "Feature",
             "properties": {
                 "region": "Araucanía",
                 "codigo": "IX",
                 "superficie": 31842.3,
                 "capital": "Temuco"
             },
             "geometry": {"type": "Point", "coordinates": [-72.5904, -38.7369]}},
            {"type": "Feature",
             "properties": {
                 "region": "Los Ríos",
                 "codigo": "XIV",
                 "superficie": 18429.5,
                 "capital": "Valdivia"
             },
             "geometry": {"type": "Point", "coordinates": [-73.2459, -39.8142]}},
            {"type": "Feature",
             "properties": {
                 "region": "Los Lagos",
                 "codigo": "X",
                 "superficie": 48583.6,
                 "capital": "Puerto Montt"
             },
             "geometry": {"type": "Point", "coordinates": [-72.9424, -41.4693]}},
            {"type": "Feature",
             "properties": {
                 "region": "Aysén",
                 "codigo": "XI",
                 "superficie": 108494.4,
                 "capital": "Coyhaique"
             },
             "geometry": {"type": "Point", "coordinates": [-72.0662, -45.5752]}},
            {"type": "Feature",
             "properties": {
                 "region": "Magallanes",
                 "codigo": "XII",
                 "superficie": 132297.2,
                 "capital": "Punta Arenas"
             },
             "geometry": {"type": "Point", "coordinates": [-70.9171, -53.1638]}},
            {"type": "Feature",
             "properties": {
                 "region": "Metropolitana",
                 "codigo": "XIII",
                 "superficie": 15403.2,
                 "capital": "Santiago"
             },
             "geometry": {"type": "Point", "coordinates": [-70.6693, -33.4489]}}
        ]
    }

def get_pollutant_colors():
    """Obtiene colores específicos para cada contaminante - consistentes con tema"""
    return {
        'pm25': '#E74C3C',    # Rojo principal - material particulado fino
        'pm10': '#3498DB',    # Azul principal - material particulado grueso
        'o3': '#27AE60',      # Verde principal - ozono
        'no2': '#F39C12',     # Naranja principal - dióxido de nitrógeno
        'co': '#9B59B6',      # Púrpura - monóxido de carbono
        'so2': '#34495E'      # Gris oscuro - dióxido de azufre
    }

def get_enhanced_color_scale():
    """Obtiene una escala de colores mejorada para PM2.5 - consistente con tema"""
    return [
        [0.0, '#00E400'],    # Verde brillante - Excelente (0-12)
        [0.2, '#FFFF00'],    # Amarillo - Bueno (12-35)
        [0.4, '#FF7E00'],    # Naranja - Moderado (35-55)
        [0.6, '#FF0000'],    # Rojo - Insalubre para sensibles (55-150)
        [0.8, '#8F3F97'],    # Púrpura - Insalubre (150-250)
        [1.0, '#7E0023']     # Granate - Muy insalubre (250+)
    ]

def get_aqi_category(pm25_value):
    """Obtiene la categoría AQI y color para un valor de PM2.5"""
    if pd.isna(pm25_value):
        return "Sin datos", "#CCCCCC"

    if pm25_value <= 12:
        return "Excelente", "#00E400"
    elif pm25_value <= 35:
        return "Bueno", "#FFFF00"
    elif pm25_value <= 55:
        return "Moderado", "#FF7E00"
    elif pm25_value <= 150:
        return "Insalubre para sensibles", "#FF0000"
    elif pm25_value <= 250:
        return "Insalubre", "#8F3F97"
    else:
        return "Muy insalubre", "#7E0023"

def get_map_config():
    """Configuración mejorada del mapa con tema consistente"""
    return {
        'center': {'lat': -35.0, 'lon': -71.0},
        'zoom_level': 3.5,
        'style': 'open-street-map',
        'theme_color': '#2C3E50'
    }

def get_color_for_pm25(pm25_value):
    """Obtiene color hexadecimal para valor de PM2.5"""
    category, color = get_aqi_category(pm25_value)
    return color

def normalize_region_name(name):
    """Normaliza nombres de regiones"""
    if pd.isna(name):
        return ""

    name = str(name).strip()

    # Mapeo de nombres de regiones
    region_mapping = {
        'Arica': 'Arica y Parinacota',
        'Atacama': 'Atacama',
        'Aysen': 'Aysén',
        'Biobio': 'Biobío',
        'La Araucanía': 'Araucanía',
        'Los Lagos': 'Los Lagos',
        'Los Rios': 'Los Ríos',
        'Magallanes': 'Magallanes',
        'Maule': 'Maule',
        'Metropolitana': 'Metropolitana',
        "O'Higgins": "O'Higgins",
        'Tarapaca': 'Tarapacá',
        'Valparaiso': 'Valparaíso',
        'antofagasta': 'Antofagasta',
        'coquimbo': 'Coquimbo',
        'Ñuble': 'Ñuble',
    }

    return region_mapping.get(name, name)

def map_geojson_region_name(geojson_name):
    """Mapea nombres de regiones del GeoJSON a nombres estándar"""
    if pd.isna(geojson_name):
        return "Sin nombre"

    name = str(geojson_name).strip()

    # Mapeo de nombres del GeoJSON (formato "Región de X") a nombres estándar
    geojson_mapping = {
        'Región de Arica y Parinacota': 'Arica y Parinacota',
        'Región de Tarapacá': 'Tarapacá',
        'Región de Antofagasta': 'Antofagasta',
        'Región de Atacama': 'Atacama',
        'Región de Coquimbo': 'Coquimbo',
        'Región de Valparaíso': 'Valparaíso',
        'Región del Libertador General Bernardo O\'Higgins': "O'Higgins",
        'Región del Maule': 'Maule',
        'Región del Ñuble': 'Ñuble',
        'Región del Biobío': 'Biobío',
        'Región de la Araucanía': 'Araucanía',
        'Región de Los Ríos': 'Los Ríos',
        'Región de Los Lagos': 'Los Lagos',
        'Región Aysén del General Carlos Ibáñez del Campo': 'Aysén',
        'Región de Magallanes y de la Antártica Chilena': 'Magallanes',
        'Región Metropolitana de Santiago': 'Metropolitana',
        'Región Metropolitana': 'Metropolitana'
    }

    return geojson_mapping.get(name, name)

def get_region_coordinates():
    """Obtiene coordenadas optimizadas de las capitales regionales para mejor visualización"""
    return {
        'Arica y Parinacota': {'lat': -18.4746, 'lon': -70.2979},
        'Tarapacá': {'lat': -20.2133, 'lon': -70.1522},
        'Antofagasta': {'lat': -23.6509, 'lon': -70.3975},
        'Atacama': {'lat': -27.3668, 'lon': -70.3323},
        'Coquimbo': {'lat': -29.9533, 'lon': -71.3395},
        'Valparaíso': {'lat': -33.0458, 'lon': -71.6197},
        "O'Higgins": {'lat': -34.1708, 'lon': -70.7444},
        'Maule': {'lat': -35.4264, 'lon': -71.6554},
        'Ñuble': {'lat': -36.6096, 'lon': -72.1025},
        'Biobío': {'lat': -36.8201, 'lon': -73.0444},
        'Araucanía': {'lat': -38.7369, 'lon': -72.5904},
        'Los Ríos': {'lat': -39.8142, 'lon': -73.2459},
        'Los Lagos': {'lat': -41.4693, 'lon': -72.9424},
        'Aysén': {'lat': -45.5752, 'lon': -72.0662},
        'Magallanes': {'lat': -53.1638, 'lon': -70.9171},
        'Metropolitana': {'lat': -33.4489, 'lon': -70.6693}
    }

# ===== FUNCIONES PRINCIPALES DE MAPAS =====

def create_chile_map(df_air_quality, year_from=2019, year_to=2023):
    """Crea un mapa simple de Chile como selector de regiones"""

    # Obtener coordenadas conocidas de regiones
    region_coords = get_region_coordinates()

    # Preparar datos básicos del mapa
    lats = []
    lons = []
    names = []
    colors = []

    for region, coords in region_coords.items():
        lats.append(coords['lat'])
        lons.append(coords['lon'])
        names.append(region)
        colors.append('blue')  # Color simple para todas las regiones

    # Crear mapa simple con colores del tema
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers+text',
        marker=dict(
            size=18,
            color='#E74C3C',  # Rojo más visible
            opacity=0.9,
            symbol='circle'
        ),
        text=names,
        textposition="middle center",
        textfont=dict(size=9, color='#FFFFFF', family='Arial Black'),
        hovertemplate='<b>%{text}</b><br>📍 Haga clic para seleccionar<extra></extra>',
        name='Regiones de Chile'
    ))

    # Configuración del mapa con tema consistente para mostrar Chile completo
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=-35.0, lon=-71.0),
            zoom=3.5,
            bearing=0,
            pitch=0
        ),
        height=650,
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text="🗺️ Seleccione una Región",
            font=dict(size=16, color='#2C3E50', family='Arial'),
            x=0.5
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

# ===== GRÁFICOS TEMPORALES =====

def create_temporal_chart(df_air_quality, station_name, year_from=2019, year_to=2023):
    """Crea gráfico temporal unificado para una estación específica"""

    if df_air_quality is None or df_air_quality.empty:
        return create_empty_temporal_chart()

    try:
        # Filtrar datos por estación y período
        df_station = df_air_quality[
            df_air_quality['estacion'] == station_name
        ].copy()

        if df_station.empty:
            return create_empty_temporal_chart(f"Sin datos para {station_name}")

        # Filtrar por años
        if 'timestamp' in df_station.columns:
            df_station['timestamp'] = pd.to_datetime(df_station['timestamp'])
            df_station = df_station[
                (df_station['timestamp'].dt.year >= year_from) &
                (df_station['timestamp'].dt.year <= year_to)
            ]

        if df_station.empty:
            return create_empty_temporal_chart(f"Sin datos para {station_name} en el período {year_from}-{year_to}")

        colors = get_pollutant_colors()

        # Crear figura simple sin subplots complejos
        fig = go.Figure()

        # PM2.5 y PM10 - Escala principal
        if 'pm25' in df_station.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_station['timestamp'],
                    y=df_station['pm25'],
                    mode='lines+markers',
                    name='PM2.5 (μg/m³)',
                    line=dict(color=colors['pm25'], width=3),
                    marker=dict(size=4),
                    hovertemplate='<b>PM2.5</b><br>%{x}<br>%{y:.1f} μg/m³<extra></extra>'
                )
            )

        if 'pm10' in df_station.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_station['timestamp'],
                    y=df_station['pm10'],
                    mode='lines+markers',
                    name='PM10 (μg/m³)',
                    line=dict(color=colors['pm10'], width=3),
                    marker=dict(size=4),
                    hovertemplate='<b>PM10</b><br>%{x}<br>%{y:.1f} μg/m³<extra></extra>'
                )
            )

        # Gases con escala normalizadas (dividir para mejor visualización)
        gas_pollutants = ['o3', 'no2', 'co', 'so2']
        for pollutant in gas_pollutants:
            if pollutant in df_station.columns and not df_station[pollutant].isna().all():
                units = 'ppb' if pollutant in ['o3', 'no2', 'so2'] else 'ppm'
                # Normalizar valores para mejor visualización
                scale_factor = 10 if pollutant in ['o3', 'no2'] else 100 if pollutant == 'co' else 1
                normalized_values = df_station[pollutant] / scale_factor

                # Crear texto para hover con valores originales
                hover_text = [f'<b>{pollutant.upper()}</b><br>{timestamp}<br>{value:.2f} {units}<extra></extra>'
                             for timestamp, value in zip(df_station['timestamp'], df_station[pollutant])]

                fig.add_trace(
                    go.Scatter(
                        x=df_station['timestamp'],
                        y=normalized_values,
                        mode='lines+markers',
                        name=f"{pollutant.upper()} ({units}/×{scale_factor})",
                        line=dict(color=colors[pollutant], width=2, dash='dot'),
                        marker=dict(size=5),
                        hovertext=hover_text,
                        hoverinfo='text',
                        showlegend=True
                    )
                )

        # Layout configurado para mantenerse dentro del contenedor
        fig.update_layout(
            height=400,  # Altura fija para que quepa en el contenedor
            title=dict(
                text=f"📈 Evolución Temporal - {station_name} ({year_from}-{year_to})",
                font=dict(size=14, color='#2C3E50', family='Arial'),
                x=0.5,
                y=0.95
            ),
            hovermode='x unified',
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#2C3E50', size=10),
                bgcolor="#F8F9FA",
                bordercolor="#2C3E50",
                borderwidth=1
            ),
            margin=dict(l=50, r=50, t=50, b=80),  # Márgenes más ajustados
            plot_bgcolor='white',
            paper_bgcolor='white',
            autosize=True  # Permitir que se ajuste automáticamente
        )

        # Configurar eje X
        fig.update_xaxes(
            title_text="Fecha",
            title_font=dict(color='#2C3E50', size=12),
            tickfont=dict(color='#34495E', size=10),
            showgrid=True,
            gridcolor="#e1e5ed"
        )

        # Configurar eje Y
        fig.update_yaxes(
            title_text="Concentración (μg/m³, valores normalizados)",
            title_font=dict(color='#2C3E50', size=12),
            tickfont=dict(color='#34495E', size=10),
            showgrid=True,
            gridcolor="#e1e5ed"
        )

        return fig

    except Exception as e:
        print(f"❌ Error creando gráfico temporal: {e}")
        import traceback
        traceback.print_exc()
        return create_empty_temporal_chart(f"Error: {str(e)}")

def create_empty_temporal_chart(message="Sin datos disponibles"):
    """Crea gráfico temporal vacío"""
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )

    fig.update_layout(
        height=600,
        title=dict(
            text="📈 Análisis Temporal",
            font=dict(color='#2C3E50', family='Arial')
        ),
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

# ===== GRÁFICOS DE EMISIONES =====

def create_emissions_chart(df_emissions, chart_type='region', region_filter=None):
    """Crea gráficos de análisis de emisiones mejorados"""

    if df_emissions is None or df_emissions.empty:
        return create_empty_emissions_chart()

    try:
        df_filtered = df_emissions.copy()

        # Usar solo el año más reciente
        latest_year = df_filtered['año'].max()
        df_filtered = df_filtered[df_filtered['año'] == latest_year]

        # Aplicar filtro de región si se especifica
        if region_filter and region_filter != 'all':
            df_filtered = df_filtered[df_filtered['region'] == region_filter]

        if df_filtered.empty:
            return create_empty_emissions_chart("Sin datos para los filtros seleccionados")

        if chart_type == 'region':
            return create_emissions_by_region(df_filtered)
        elif chart_type == 'source_type':
            return create_emissions_by_source_type(df_filtered)
        elif chart_type == 'temporal':
            return create_emissions_temporal(df_emissions)  # Para temporal usamos todos los años
        else:
            return create_emissions_by_region(df_filtered)

    except Exception as e:
        print(f"❌ Error creando gráfico de emisiones: {e}")
        return create_empty_emissions_chart(f"Error: {str(e)}")

def create_emissions_by_region(df_emissions):
    """Crea gráfico de emisiones por región"""

    # Agrupar por región y tipo de fuente
    df_grouped = df_emissions.groupby(['region', 'tipo_fuente'])['cantidad_toneladas'].sum().reset_index()

    # Crear gráfico de barras apiladas
    fig = px.bar(
        df_grouped,
        x='region',
        y='cantidad_toneladas',
        color='tipo_fuente',
        title='🏭 Emisiones por Región y Tipo de Fuente',
        labels={
            'cantidad_toneladas': 'Emisiones (toneladas)',
            'region': 'Región',
            'tipo_fuente': 'Tipo de Fuente'
        },
        color_discrete_map={
            'Difusas': '#F39C12',    # Naranja fuerte
            'Puntuales': '#2C3E50',  # Azul oscuro
            'En Ruta': '#27AE60'     # Verde
        }
    )

    fig.update_layout(
        height=650,
        template='plotly_white',
        xaxis_tickangle=-45,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5,
            bgcolor="#F8F9FA",
            bordercolor="#2C3E50",
            borderwidth=1,
            font=dict(color="#2C3E50", size=14)
        ),
        margin=dict(l=40, r=40, t=60, b=120)
    )
    fig.update_traces(marker_line_width=1.5, marker_line_color="#fff")

    return fig

def create_emissions_by_source_type(df_emissions):
    """Crea gráfico de emisiones por tipo de fuente"""

    # Agrupar por tipo de fuente
    df_grouped = df_emissions.groupby('tipo_fuente')['cantidad_toneladas'].sum().reset_index()

    # Crear gráfico de dona
    fig = px.pie(
        df_grouped,
        values='cantidad_toneladas',
        names='tipo_fuente',
        title='🔄 Distribución de Emisiones por Tipo de Fuente',
        hole=0.4,
        color_discrete_map={
            'Difusas': '#FF9999',
            'Puntuales': '#66B2FF',
            'En Ruta': '#99FF99'
        }
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} toneladas<br>%{percent}<extra></extra>'
    )

    fig.update_layout(
        height=500,
        template='plotly_white',
        annotations=[dict(text='Emisiones<br>Totales', x=0.5, y=0.5, font_size=12, showarrow=False)]
    )

    return fig

def create_emissions_temporal(df_emissions):
    """Crea gráfico temporal de emisiones"""

    if 'año' not in df_emissions.columns:
        return create_empty_emissions_chart("Sin datos temporales disponibles")

    # Agrupar por año y tipo de fuente
    df_grouped = df_emissions.groupby(['año', 'tipo_fuente'])['cantidad_toneladas'].sum().reset_index()

    fig = px.line(
        df_grouped,
        x='año',
        y='cantidad_toneladas',
        color='tipo_fuente',
        title='📈 Evolución Temporal de Emisiones',
        labels={
            'cantidad_toneladas': 'Emisiones (toneladas)',
            'año': 'Año',
            'tipo_fuente': 'Tipo de Fuente'
        },
        color_discrete_map={
            'Difusas': '#FF9999',
            'Puntuales': '#66B2FF',
            'En Ruta': '#99FF99'
        },
        markers=True
    )

    fig.update_layout(
        height=500,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

def create_empty_emissions_chart(message="Sin datos de emisiones disponibles"):
    """Crea gráfico de emisiones vacío"""
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )

    fig.update_layout(
        height=500,
        title="🏭 Análisis de Emisiones",
        template='plotly_white'
    )

    return fig

# ===== GRÁFICOS DE CORRELACIÓN =====

def create_correlation_heatmap(df_air_quality, df_population=None, df_emissions=None, variables=None):
    """Crea matriz de correlación mejorada"""

    if df_air_quality is None or df_air_quality.empty:
        return create_empty_correlation_chart()

    try:
        # Preparar datos para correlación
        df_corr = prepare_correlation_data(df_air_quality, df_population, df_emissions, variables)

        if df_corr.empty:
            return create_empty_correlation_chart("Sin datos suficientes para correlación")

        # Calcular matriz de correlación
        corr_matrix = df_corr.corr()

        # Crear heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect="auto",
            title='🔥 Matriz de Correlación - Variables Ambientales',
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )

        fig.update_layout(
            height=600,
            template='plotly_white',
            title_x=0.5
        )

        return fig

    except Exception as e:
        print(f"❌ Error creando heatmap de correlación: {e}")
        return create_empty_correlation_chart(f"Error: {str(e)}")

def create_population_vs_pollution_scatter(df_air_quality, df_population):
    """Crea gráfico de dispersión población vs contaminación con manejo robusto de NaN"""

    if df_air_quality is None or df_population is None:
        return create_empty_correlation_chart("Datos insuficientes para análisis")

    try:
        # Combinar datos
        df_combined = combine_air_quality_population(df_air_quality, df_population)

        if df_combined.empty:
            return create_empty_correlation_chart("Sin datos combinados disponibles")

        # Limpiar datos NaN y preparar para scatter plot
        df_combined = df_combined.dropna(subset=['poblacion', 'pm25', 'pm10'])

        if df_combined.empty:
            return create_empty_correlation_chart("Sin datos válidos después de limpiar NaN")

        # Asegurar que los valores de tamaño sean positivos y finitos
        df_combined['pm10_size'] = df_combined['pm10'].fillna(10)  # valor por defecto si es NaN
        df_combined['pm10_size'] = np.clip(df_combined['pm10_size'], 5, 100)  # limitar tamaño

        # Crear scatter plot
        fig = px.scatter(
            df_combined,
            x='poblacion',
            y='pm25',
            size='pm10_size',
            color='region',
            hover_name='region',
            title='👥 Población vs Contaminación del Aire',
            labels={
                'poblacion': 'Población',
                'pm25': 'PM2.5 (μg/m³)',
                'pm10_size': 'PM10 (μg/m³)'
            },
            size_max=60
        )

        # Agregar línea de tendencia si hay suficientes datos
        if len(df_combined) >= 3:
            try:
                # Crear scatter simple para tendencia
                fig_trend = px.scatter(
                    df_combined, x='poblacion', y='pm25',
                    trendline='ols'
                )
                if len(fig_trend.data) > 1:
                    fig.add_trace(fig_trend.data[1])
            except:
                pass  # Si falla la tendencia, continuar sin ella

        fig.update_layout(
            height=600,
            template='plotly_white',
            title_x=0.5
        )

        return fig

    except Exception as e:
        print(f"❌ Error creando scatter plot: {e}")
        return create_empty_correlation_chart(f"Error: {str(e)}")

def prepare_correlation_data(df_air_quality, df_population, df_emissions, variables):
    """Prepara datos para análisis de correlación usando año más reciente"""

    # Empezar con datos de calidad del aire
    df_base = df_air_quality.groupby('region').agg({
        'pm25': 'mean',
        'pm10': 'mean',
        'o3': 'mean',
        'no2': 'mean',
        'co': 'mean',
        'so2': 'mean'
    }).reset_index()

    # Combinar con datos de población si están disponibles
    if df_population is not None:
        # Usar solo el año más reciente
        latest_year = df_population['año'].max()
        df_pop_latest = df_population[df_population['año'] == latest_year]
        df_pop_agg = df_pop_latest.groupby('region')['poblacion'].sum().reset_index()
        df_base = df_base.merge(df_pop_agg, on='region', how='left')

    # Combinar con datos de emisiones si están disponibles
    if df_emissions is not None:
        # Usar solo el año más reciente
        latest_year = df_emissions['año'].max()
        df_em_latest = df_emissions[df_emissions['año'] == latest_year]
        df_em_agg = df_em_latest.groupby('region')['cantidad_toneladas'].sum().reset_index()
        df_em_agg.rename(columns={'cantidad_toneladas': 'emisiones'}, inplace=True)
        df_base = df_base.merge(df_em_agg, on='region', how='left')

    # Filtrar variables si se especifican
    if variables:
        available_vars = ['region'] + [var for var in variables if var in df_base.columns]
        df_base = df_base[available_vars]

    # Eliminar columnas no numéricas para correlación
    numeric_cols = df_base.select_dtypes(include=[np.number]).columns

    return df_base[numeric_cols]

def combine_air_quality_population(df_air_quality, df_population):
    """Combina datos de calidad del aire y población usando año más reciente"""

    # Agrupar calidad del aire por región
    df_air_agg = df_air_quality.groupby('region').agg({
        'pm25': 'mean',
        'pm10': 'mean',
        'o3': 'mean',
        'no2': 'mean'
    }).reset_index()

    # Usar solo el año más reciente para población
    latest_year = df_population['año'].max()
    df_pop_latest = df_population[df_population['año'] == latest_year]
    df_pop_agg = df_pop_latest.groupby('region')['poblacion'].sum().reset_index()

    # Combinar datasets
    df_combined = df_air_agg.merge(df_pop_agg, on='region', how='inner')

    return df_combined

def create_empty_correlation_chart(message="Sin datos para análisis de correlación"):
    """Crea gráfico de correlación vacío"""
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )

    fig.update_layout(
        height=600,
        title="📊 Análisis de Correlación",
        template='plotly_white'
    )

    return fig

# ===== ANÁLISIS AVANZADO DE CORRELACIONES =====

def create_correlation_heatmap(df_air_quality, df_population, df_emissions, variables=None):
    """Crea matriz de correlación interactiva"""

    if not variables:
        variables = ['pm25', 'pm10', 'poblacion', 'emisiones']

    try:
        # Preparar datos para correlación
        correlation_data = {}

        # Agregar datos de calidad del aire por región
        if df_air_quality is not None and not df_air_quality.empty:
            # Solo agregar columnas que existen en el DataFrame
            available_air_vars = {}
            for var in ['pm25', 'pm10', 'o3', 'no2']:
                if var in df_air_quality.columns:
                    available_air_vars[var] = 'mean'

            if available_air_vars:
                air_summary = df_air_quality.groupby('region').agg(available_air_vars).round(2)

                for var in ['pm25', 'pm10', 'o3', 'no2']:
                    if var in variables and var in air_summary.columns:
                        correlation_data[var] = air_summary[var]

        # Agregar datos de población
        if df_population is not None and not df_population.empty and 'poblacion' in variables:
            pop_latest = df_population[df_population['año'] == df_population['año'].max()]
            pop_by_region = pop_latest.groupby('region')['poblacion'].sum()
            correlation_data['poblacion'] = pop_by_region

        # Agregar datos de emisiones
        if df_emissions is not None and not df_emissions.empty and 'emisiones' in variables:
            em_latest = df_emissions[df_emissions['año'] == df_emissions['año'].max()]
            em_by_region = em_latest.groupby('region')['cantidad_toneladas'].sum()
            correlation_data['emisiones'] = em_by_region

        if len(correlation_data) < 2:
            return create_empty_correlation_figure("Datos insuficientes para análisis de correlación")

        # Crear DataFrame de correlación
        df_corr = pd.DataFrame(correlation_data)
        df_corr = df_corr.dropna()

        if df_corr.empty:
            return create_empty_correlation_figure("No hay datos válidos para correlación")

        # Calcular matriz de correlación
        corr_matrix = df_corr.corr()

        # Crear heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale=[
                [0, '#E74C3C'],      # Rojo para correlación negativa
                [0.5, '#F8F9FA'],    # Blanco para correlación neutral
                [1, '#27AE60']       # Verde para correlación positiva
            ],
            zmid=0,
            text=corr_matrix.round(3).values,
            texttemplate="%{text}",
            textfont={"size": 12, "color": "#2C3E50"},
            hovertemplate='<b>%{x} vs %{y}</b><br>Correlación: %{z:.3f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text="🔥 Matriz de Correlación - Variables Ambientales",
                font=dict(size=16, color='#2C3E50', family='Arial'),
                x=0.5
            ),
            height=600,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title="", tickfont=dict(color='#2C3E50')),
            yaxis=dict(title="", tickfont=dict(color='#2C3E50'))
        )

        return fig

    except Exception as e:
        print(f"❌ Error creando matriz de correlación: {e}")
        return create_empty_correlation_figure(f"Error: {str(e)}")

def create_population_vs_pollution_scatter(df_air_quality, df_population):
    """Crea gráfico de dispersión población vs contaminación"""

    try:
        if df_air_quality is None or df_population is None:
            return create_empty_correlation_figure("Datos insuficientes para análisis")

        # Preparar datos de calidad del aire por región
        air_summary = df_air_quality.groupby('region').agg({
            'pm25': 'mean',
            'pm10': 'mean'
        }).round(2)

        # Preparar datos de población más reciente
        pop_latest = df_population[df_population['año'] == df_population['año'].max()]
        pop_by_region = pop_latest.groupby('region')['poblacion'].sum()

        # Combinar datos
        combined_data = pd.merge(
            air_summary,
            pop_by_region.to_frame('poblacion'),
            left_index=True,
            right_index=True,
            how='inner'
        )

        if combined_data.empty:
            return create_empty_correlation_figure("No hay datos coincidentes")

        # Crear gráfico de dispersión
        fig = go.Figure()

        # PM2.5 vs Población
        fig.add_trace(go.Scatter(
            x=combined_data['poblacion'],
            y=combined_data['pm25'],
            mode='markers+text',
            text=combined_data.index,
            textposition="top center",
            textfont=dict(size=10, color='#2C3E50'),
            marker=dict(
                size=12,
                color='#E74C3C',
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            name='PM2.5',
            hovertemplate='<b>%{text}</b><br>Población: %{x:,.0f}<br>PM2.5: %{y:.1f} μg/m³<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text="👥 Población vs Contaminación por PM2.5",
                font=dict(size=16, color='#2C3E50', family='Arial'),
                x=0.5
            ),
            xaxis=dict(
                title="Población",
                title_font=dict(color='#2C3E50'),
                tickfont=dict(color='#34495E')
            ),
            yaxis=dict(
                title="PM2.5 (μg/m³)",
                title_font=dict(color='#2C3E50'),
                tickfont=dict(color='#34495E')
            ),
            height=600,
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='closest'
        )

        return fig

    except Exception as e:
        print(f"❌ Error creando gráfico población vs contaminación: {e}")
        return create_empty_correlation_figure(f"Error: {str(e)}")

def create_empty_correlation_figure(message="Sin datos disponibles"):
    """Crea figura vacía para análisis de correlación"""
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="#6C757D")
    )

    fig.update_layout(
        height=600,
        title=dict(
            text="📊 Análisis de Correlación",
            font=dict(color='#2C3E50', family='Arial')
        ),
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

from dash import Input, Output, State, callback_context
import pandas as pd
import plotly.graph_objects as go
from charts import (
    create_chile_map, create_temporal_chart, create_emissions_chart,
    create_correlation_heatmap, create_population_vs_pollution_scatter,
    normalize_region_name
)
from components import (
    create_stations_tab, create_sources_tab, create_correlation_tab
)
import dash_bootstrap_components as dbc
from dash import html

def register_callbacks(app, df_air_quality, df_emissions, df_population):
    """Registra todos los callbacks del dashboard con manejo mejorado de errores"""

    # ===== CALLBACK DE NAVEGACIÓN =====

    @app.callback(
        Output('active-tab', 'data'),
        [Input('btn-stations', 'n_clicks'),
         Input('btn-sources', 'n_clicks'),
         Input('btn-correlation', 'n_clicks')]
    )
    def update_active_tab(btn_stations, btn_sources, btn_correlation):
        """Actualiza la pestaña activa basada en clics de botones"""
        ctx = callback_context
        if not ctx.triggered:
            return 'stations'

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        tab_mapping = {
            'btn-stations': 'stations',
            'btn-sources': 'sources',
            'btn-correlation': 'correlation'
        }

        return tab_mapping.get(button_id, 'stations')

    @app.callback(
        [Output('btn-stations', 'active'),
         Output('btn-sources', 'active'),
         Output('btn-correlation', 'active'),
         Output('btn-stations', 'color'),
         Output('btn-sources', 'color'),
         Output('btn-correlation', 'color')],
        [Input('active-tab', 'data')]
    )
    def update_button_styles(active_tab):
        """Actualiza estilos de botones según pestaña activa"""
        buttons_state = [False, False, False]
        colors = ['outline-primary', 'outline-warning', 'outline-success']

        if active_tab == 'stations':
            buttons_state[0] = True
            colors[0] = 'primary'
        elif active_tab == 'sources':
            buttons_state[1] = True
            colors[1] = 'warning'
        elif active_tab == 'correlation':
            buttons_state[2] = True
            colors[2] = 'success'

        return buttons_state + colors

    @app.callback(
        Output('tab-content', 'children'),
        [Input('active-tab', 'data')]
    )
    def render_tab_content(active_tab):
        """Renderiza el contenido de la pestaña activa"""
        try:
            if active_tab == 'sources':
                return create_sources_tab()
            elif active_tab == 'correlation':
                return create_correlation_tab()
            else:  # default to stations
                return create_stations_tab()
        except Exception as e:
            print(f"❌ Error renderizando pestaña {active_tab}: {e}")
            return create_stations_tab()

    # ===== CALLBACKS DEL MAPA =====

    @app.callback(
        Output('chile-map', 'figure'),
        [Input('date-from', 'value'),
         Input('date-to', 'value')]
    )
    def update_map(year_from, year_to):
        """Actualiza el mapa de Chile con datos filtrados"""
        try:
            year_from = year_from or 2019
            year_to = year_to or 2023
            return create_chile_map(df_air_quality, year_from, year_to)
        except Exception as e:
            print(f"❌ Error actualizando mapa: {e}")
            return create_chile_map(None, year_from, year_to)

    @app.callback(
        [Output('population-percentage', 'children'),
         Output('emissions-percentage', 'children'),
         Output('regional-conclusion', 'children'),
         Output('info-text', 'children'),
         Output('station-dropdown', 'options')],
        [Input('chile-map', 'clickData')]
    )
    def update_region_info(clickData):
        """Actualiza información regional cuando se hace clic en el mapa"""
        try:
            if not clickData or not clickData.get('points'):
                return "--", "--", generate_default_conclusion(), generate_default_info(), []

            # Extraer información del clic
            point = clickData['points'][0]
            region_name = point.get('text', '')

            print(f"🔍 Debug - Clic en región: '{region_name}'")

            if not region_name:
                print("❌ Debug - Nombre de región vacío")
                return "--", "--", generate_default_conclusion(), generate_default_info(), []

            # El nombre ya viene normalizado del mapa, no necesita más normalización
            # region_name = normalize_region_name(region_name)
            print(f"🔍 Debug - Región procesada: '{region_name}'")

            # Verificar que la región existe en los datos
            if df_air_quality is not None:
                available_regions = df_air_quality['region'].unique()
                print(f"🔍 Debug - Regiones disponibles en aire: {list(available_regions)}")
                if region_name not in available_regions:
                    print(f"❌ Debug - Región '{region_name}' no encontrada en datos de aire")

            # Calcular estadísticas poblacionales
            pop_percentage = calculate_population_percentage(region_name, df_population)
            print(f"🔍 Debug - Población: {pop_percentage}")

            # Calcular estadísticas de emisiones
            emissions_percentage = calculate_emissions_percentage(region_name, df_emissions)
            print(f"🔍 Debug - Emisiones: {emissions_percentage}")

            # Generar conclusión regional
            conclusion = generate_regional_conclusion(region_name, pop_percentage, emissions_percentage)

            # Generar información detallada
            info_text = generate_regional_info(region_name, df_air_quality, df_population, df_emissions)

            # Obtener opciones de estaciones para la región
            station_options = get_station_options(region_name, df_air_quality)
            print(f"🔍 Debug - Estaciones encontradas: {len(station_options)}")

            return pop_percentage, emissions_percentage, conclusion, info_text, station_options

        except Exception as e:
            print(f"❌ Error actualizando información regional: {e}")
            import traceback
            traceback.print_exc()
            return "--", "--", generate_error_conclusion(), generate_error_info(), []

    # ===== CALLBACKS DE ANÁLISIS TEMPORAL =====

    @app.callback(
        Output('temporal-chart', 'figure'),
        [Input('station-dropdown', 'value'),
         Input('date-from', 'value'),
         Input('date-to', 'value')]
    )
    def update_temporal_chart_callback(station_name, year_from, year_to):
        """Actualiza el gráfico temporal para la estación seleccionada"""
        try:
            if not station_name:
                return create_empty_temporal_figure()

            year_from = year_from or 2019
            year_to = year_to or 2023

            return create_temporal_chart(df_air_quality, station_name, year_from, year_to)

        except Exception as e:
            print(f"❌ Error creando gráfico temporal: {e}")
            return create_empty_temporal_figure(f"Error: {str(e)}")

    # ===== CALLBACKS DE FUENTES DE EMISIÓN =====

    @app.callback(
        Output('sources-region-filter', 'options'),
        [Input('active-tab', 'data')]
    )
    def update_sources_region_dropdown(active_tab):
        """Actualiza opciones del dropdown de regiones para fuentes"""
        try:
            if active_tab != 'sources' or df_emissions is None:
                return []

            regions = sorted(df_emissions['region'].dropna().unique())
            options = [{'label': 'Todas las regiones', 'value': 'all'}]
            options.extend([{'label': region, 'value': region} for region in regions])

            return options

        except Exception as e:
            print(f"❌ Error actualizando dropdown de regiones: {e}")
            return [{'label': 'Error cargando regiones', 'value': 'error'}]

    @app.callback(
        [Output('emissions-chart', 'figure'),
         Output('emissions-stats', 'children')],
        [Input('sources-chart-type', 'value'),
         Input('sources-region-filter', 'value')]
    )
    def update_emissions_analysis(chart_type, region_filter):
        """Actualiza análisis de emisiones"""
        try:
            if df_emissions is None:
                return create_empty_emissions_figure(), generate_no_data_stats()

            # Crear gráfico
            figure = create_emissions_chart(df_emissions, chart_type, region_filter)

            # Generar estadísticas
            stats = generate_emissions_statistics(df_emissions, chart_type, region_filter)

            return figure, stats

        except Exception as e:
            print(f"❌ Error en análisis de emisiones: {e}")
            return create_empty_emissions_figure(f"Error: {str(e)}"), generate_error_stats()

    # ===== CALLBACKS DE CORRELACIÓN =====

    @app.callback(
        [Output('correlation-chart', 'figure'),
         Output('correlation-stats', 'children'),
         Output('correlation-insights', 'children')],
        [Input('correlation-analysis-type', 'value'),
         Input('correlation-variables', 'value')]
    )
    def update_correlation_analysis(analysis_type, variables):
        """Actualiza análisis de correlación"""
        try:
            if analysis_type == 'heatmap':
                figure = create_correlation_heatmap(df_air_quality, df_population, df_emissions, variables)
            elif analysis_type == 'population_pollution':
                figure = create_population_vs_pollution_scatter(df_air_quality, df_population)
            elif analysis_type == 'emissions_air_quality':
                figure = create_emissions_vs_air_quality_scatter(df_air_quality, df_emissions)
            elif analysis_type == 'temporal_correlation':
                figure = create_temporal_correlation_chart(df_air_quality, variables)
            else:
                figure = create_correlation_heatmap(df_air_quality, df_population, df_emissions, variables)

            # Generar estadísticas e insights
            stats = generate_correlation_statistics(analysis_type, variables, df_air_quality, df_population, df_emissions)
            insights = generate_correlation_insights(analysis_type, variables, df_air_quality, df_population, df_emissions)

            return figure, stats, insights

        except Exception as e:
            print(f"❌ Error en análisis de correlación: {e}")
            return create_empty_correlation_figure(f"Error: {str(e)}"), generate_error_stats(), generate_error_insights()

    # ===== FUNCIONES AUXILIARES =====

    def calculate_population_percentage(region_name, df_population):
        """Calcula el porcentaje poblacional de una región usando el año más reciente"""
        try:
            if df_population is None or df_population.empty:
                return "--"

            df_pop = df_population.copy()
            # Los datos ya vienen normalizados desde app.py, no necesitamos normalizar otra vez

            # Usar solo el año más reciente disponible
            latest_year = df_pop['año'].max()
            df_latest = df_pop[df_pop['año'] == latest_year]

            total_population = df_latest['poblacion'].sum()
            region_population = df_latest[df_latest['region'] == region_name]['poblacion'].sum()

            if total_population > 0:
                percentage = (region_population / total_population) * 100
                return f"{percentage:.1f}%"
            else:
                return "--"

        except Exception as e:
            print(f"❌ Error calculando porcentaje poblacional: {e}")
            return "--"

    def calculate_emissions_percentage(region_name, df_emissions):
        """Calcula el porcentaje de emisiones de una región usando el año más reciente"""
        try:
            if df_emissions is None or df_emissions.empty:
                return "--"

            df_em = df_emissions.copy()
            # Los datos ya vienen normalizados desde app.py, no necesitamos normalizar otra vez

            # Usar solo el año más reciente disponible
            latest_year = df_em['año'].max()
            df_latest = df_em[df_em['año'] == latest_year]

            total_emissions = df_latest['cantidad_toneladas'].sum()
            region_emissions = df_latest[df_latest['region'] == region_name]['cantidad_toneladas'].sum()

            if total_emissions > 0:
                percentage = (region_emissions / total_emissions) * 100
                return f"{percentage:.1f}%"
            else:
                return "--"

        except Exception as e:
            print(f"❌ Error calculando porcentaje de emisiones: {e}")
            return "--"

    def generate_regional_conclusion(region_name, pop_percentage, emissions_percentage):
        """Genera conclusión regional basada en estadísticas"""
        try:
            if pop_percentage == "--" or emissions_percentage == "--":
                return html.Div([
                    html.I(className="fas fa-question-circle text-muted me-2"),
                    "Datos insuficientes para evaluación"
                ], className="small text-muted")

            # Extraer valores numéricos
            pop_val = float(pop_percentage.replace('%', ''))
            em_val = float(emissions_percentage.replace('%', ''))

            # Generar conclusión
            if em_val > pop_val * 1.5:
                icon = "fas fa-exclamation-triangle text-danger"
                text = "Emisiones desproporcionalmente altas"
                color = "text-danger"
            elif em_val < pop_val * 0.5:
                icon = "fas fa-leaf text-success"
                text = "Emisiones relativamente bajas"
                color = "text-success"
            else:
                icon = "fas fa-balance-scale text-warning"
                text = "Emisiones proporcionales a población"
                color = "text-warning"

            return html.Div([
                html.I(className=f"{icon} me-2"),
                html.Span(text, className=color)
            ], className="small")

        except Exception as e:
            print(f"❌ Error generando conclusión regional: {e}")
            return html.Div([
                html.I(className="fas fa-exclamation-circle text-danger me-2"),
                "Error en evaluación"
            ], className="small text-danger")

    def generate_regional_info(region_name, df_air_quality, df_population, df_emissions):
        """Genera información detallada de la región"""
        try:
            info_components = [
                html.H5([
                    html.I(className="fas fa-map-marker-alt text-primary me-2"),
                    f"Información detallada - {region_name}"
                ], className="mb-3")
            ]

            # Información de calidad del aire
            if df_air_quality is not None and not df_air_quality.empty:
                df_air = df_air_quality.copy()
                # Los datos ya vienen normalizados desde app.py
                region_air = df_air[df_air['region'] == region_name]

                if not region_air.empty:
                    avg_pm25 = region_air['pm25'].mean()
                    if not pd.isna(avg_pm25):
                        info_components.append(
                            html.P([
                                html.I(className="fas fa-lungs text-danger me-2"),
                                f"PM2.5 promedio: {avg_pm25:.1f} μg/m³"
                            ], className="mb-2")
                        )

            # Información poblacional
            if df_population is not None and not df_population.empty:
                df_pop = df_population.copy()
                # Los datos ya vienen normalizados desde app.py
                # Usar solo el año más reciente
                latest_year = df_pop['año'].max()
                df_latest = df_pop[df_pop['año'] == latest_year]
                region_pop = df_latest[df_latest['region'] == region_name]['poblacion'].sum()

                if region_pop > 0:
                    info_components.append(
                        html.P([
                            html.I(className="fas fa-users text-info me-2"),
                            f"Población total ({latest_year}): {region_pop:,.0f} habitantes"
                        ], className="mb-2")
                    )

            # Información de emisiones
            if df_emissions is not None and not df_emissions.empty:
                df_em = df_emissions.copy()
                # Los datos ya vienen normalizados desde app.py
                # Usar solo el año más reciente
                latest_year = df_em['año'].max()
                df_latest = df_em[df_em['año'] == latest_year]
                region_emissions = df_latest[df_latest['region'] == region_name]['cantidad_toneladas'].sum()

                if region_emissions > 0:
                    info_components.append(
                        html.P([
                            html.I(className="fas fa-smog text-warning me-2"),
                            f"Emisiones totales ({latest_year}): {region_emissions:,.0f} toneladas"
                        ], className="mb-2")
                    )

            if len(info_components) == 1:  # Solo el título
                info_components.append(
                    html.P([
                        html.I(className="fas fa-info-circle text-muted me-2"),
                        "No hay datos disponibles para esta región."
                    ], className="text-muted")
                )

            return html.Div(info_components)

        except Exception as e:
            print(f"❌ Error generando información regional: {e}")
            return generate_error_info()

    def get_station_options(region_name, df_air_quality):
        """Obtiene opciones de estaciones para una región"""
        try:
            if df_air_quality is None or df_air_quality.empty:
                return []

            df_air = df_air_quality.copy()
            # Los datos ya vienen normalizados desde app.py, no necesitamos normalizar otra vez

            stations = df_air[df_air['region'] == region_name]['estacion'].dropna().unique()
            return [{'label': station, 'value': station} for station in sorted(stations)]

        except Exception as e:
            print(f"❌ Error obteniendo opciones de estaciones: {e}")
            return []

    def generate_emissions_statistics(df_emissions, chart_type, region_filter):
        """Genera estadísticas de emisiones usando datos del año más reciente"""
        try:
            if df_emissions is None or df_emissions.empty:
                return generate_no_data_stats()

            df_filtered = df_emissions.copy()

            # Usar solo el año más reciente
            latest_year = df_filtered['año'].max()
            df_filtered = df_filtered[df_filtered['año'] == latest_year]

            if region_filter and region_filter != 'all':
                df_filtered = df_filtered[df_filtered['region'] == region_filter]

            total_emissions = df_filtered['cantidad_toneladas'].sum()
            avg_emissions = df_filtered['cantidad_toneladas'].mean()
            max_emissions = df_filtered['cantidad_toneladas'].max()

            stats_components = [
                html.H6("📊 Estadísticas Generales", className="mb-3"),
                html.P([
                    html.Strong("Total de emisiones: "),
                    f"{total_emissions:,.0f} toneladas"
                ], className="mb-2"),
                html.P([
                    html.Strong("Emisiones promedio: "),
                    f"{avg_emissions:.1f} toneladas"
                ], className="mb-2"),
                html.P([
                    html.Strong("Emisiones máximas: "),
                    f"{max_emissions:,.0f} toneladas"
                ], className="mb-2")
            ]

            # Estadísticas por tipo de fuente
            if 'tipo_fuente' in df_filtered.columns:
                by_source = df_filtered.groupby('tipo_fuente')['cantidad_toneladas'].sum().sort_values(ascending=False)
                stats_components.append(html.Hr())
                stats_components.append(html.H6("🏭 Por Tipo de Fuente", className="mb-2"))

                for source_type, emissions in by_source.head(3).items():
                    percentage = (emissions / total_emissions) * 100
                    stats_components.append(
                        html.P([
                            html.Strong(f"{source_type}: "),
                            f"{emissions:,.0f} ton ({percentage:.1f}%)"
                        ], className="mb-1 small")
                    )

            return html.Div(stats_components)

        except Exception as e:
            print(f"❌ Error generando estadísticas de emisiones: {e}")
            return generate_error_stats()

    def generate_correlation_statistics(analysis_type, variables, df_air_quality, df_population, df_emissions):
        """Genera estadísticas de correlación"""
        try:
            if analysis_type == 'heatmap':
                return html.Div([
                    html.P([
                        html.Strong("Tipo de análisis: "),
                        "Matriz de correlación"
                    ], className="mb-2"),
                    html.P([
                        html.Strong("Variables incluidas: "),
                        f"{len(variables) if variables else 0}"
                    ], className="mb-2"),
                    html.P("Valores cercanos a ±1 indican correlaciones fuertes.",
                           className="small text-muted")
                ])
            else:
                return html.Div([
                    html.P("Estadísticas específicas del análisis seleccionado.",
                           className="text-muted")
                ])

        except Exception as e:
            print(f"❌ Error generando estadísticas de correlación: {e}")
            return generate_error_stats()

    def generate_correlation_insights(analysis_type, variables, df_air_quality, df_population, df_emissions):
        """Genera insights de correlación"""
        try:
            insights = [
                html.P([
                    html.I(className="fas fa-lightbulb text-warning me-2"),
                    f"Análisis basado en {analysis_type.replace('_', ' ')}"
                ], className="mb-2")
            ]

            if analysis_type == 'population_pollution':
                insights.append(
                    html.P("Las áreas más pobladas tienden a mostrar mayores niveles "
                           "de contaminación, especialmente PM2.5 y NO2.",
                           className="small")
                )
            elif analysis_type == 'heatmap':
                insights.append(
                    html.P("Las correlaciones fuertes (>0.7) sugieren relaciones "
                           "causales que requieren investigación adicional.",
                           className="small")
                )

            return html.Div(insights)

        except Exception as e:
            print(f"❌ Error generando insights de correlación: {e}")
            return generate_error_insights()

    # Funciones de elementos por defecto y error
    def generate_default_conclusion():
        return html.Div([
            html.I(className="fas fa-mouse-pointer text-muted me-2"),
            "Seleccione una región"
        ], className="small text-muted")

    def generate_default_info():
        return dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Haga clic en una región del mapa para ver información detallada."
        ], color="light", className="text-center")

    def generate_error_conclusion():
        return html.Div([
            html.I(className="fas fa-exclamation-triangle text-danger me-2"),
            "Error cargando datos"
        ], className="small text-danger")

    def generate_error_info():
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Error cargando información regional."
        ], color="danger", className="text-center")

    def generate_no_data_stats():
        return dbc.Alert([
            html.I(className="fas fa-database me-2"),
            "No hay datos disponibles para mostrar estadísticas."
        ], color="warning", className="text-center small")

    def generate_error_stats():
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Error generando estadísticas."
        ], color="danger", className="text-center small")

    def generate_error_insights():
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            "Error generando insights."
        ], color="danger", className="text-center small")

    def create_empty_temporal_figure(message="Seleccione una estación para ver análisis temporal"):
        """Crea figura temporal vacía"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            height=400,
            title="📈 Análisis Temporal",
            template='plotly_white'
        )
        return fig

    def create_empty_emissions_figure(message="Sin datos de emisiones disponibles"):
        """Crea figura de emisiones vacía"""
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

    def create_empty_correlation_figure(message="Sin datos para análisis de correlación"):
        """Crea figura de correlación vacía"""
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

    # Funciones adicionales para análisis avanzados
    def create_emissions_vs_air_quality_scatter(df_air_quality, df_emissions):
        """Crea scatter plot de emisiones vs calidad del aire"""
        try:
            if df_air_quality is None or df_emissions is None:
                return create_empty_correlation_figure("Datos insuficientes para análisis")

            # Combinar datos por región
            df_air_agg = df_air_quality.groupby('region').agg({
                'pm25': 'mean',
                'pm10': 'mean'
            }).reset_index()

            df_em_agg = df_emissions.groupby('region')['cantidad_toneladas'].sum().reset_index()

            df_combined = df_air_agg.merge(df_em_agg, on='region', how='inner')

            if df_combined.empty:
                return create_empty_correlation_figure("Sin datos combinados disponibles")

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_combined['cantidad_toneladas'],
                y=df_combined['pm25'],
                mode='markers+text',
                text=df_combined['region'],
                textposition='top center',
                marker=dict(
                    size=12,
                    color=df_combined['pm10'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="PM10 (μg/m³)")
                ),
                name='Regiones'
            ))

            fig.update_layout(
                title='🏭 Emisiones vs Calidad del Aire por Región',
                xaxis_title='Emisiones Totales (toneladas)',
                yaxis_title='PM2.5 Promedio (μg/m³)',
                height=600,
                template='plotly_white'
            )

            return fig

        except Exception as e:
            print(f"❌ Error creando scatter emisiones vs calidad aire: {e}")
            return create_empty_correlation_figure(f"Error: {str(e)}")

    def create_temporal_correlation_chart(df_air_quality, variables):
        """Crea análisis de correlación temporal"""
        try:
            if df_air_quality is None or not variables:
                return create_empty_correlation_figure("Variables insuficientes para análisis temporal")

            # Preparar datos temporales
            df_temp = df_air_quality.copy()
            if 'timestamp' in df_temp.columns:
                df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'])
                df_temp['year'] = df_temp['timestamp'].dt.year
                df_temp['month'] = df_temp['timestamp'].dt.month

                # Agrupar por año y mes
                available_vars = [var for var in variables if var in df_temp.columns]
                if not available_vars:
                    return create_empty_correlation_figure("Variables no encontradas en los datos")

                df_monthly = df_temp.groupby(['year', 'month'])[available_vars].mean().reset_index()

                fig = go.Figure()

                for var in available_vars:
                    if var in df_monthly.columns:
                        fig.add_trace(go.Scatter(
                            x=pd.to_datetime(df_monthly[['year', 'month']].assign(day=1)),
                            y=df_monthly[var],
                            mode='lines+markers',
                            name=var.upper(),
                            line=dict(width=2),
                            marker=dict(size=4)
                        ))

                fig.update_layout(
                    title='📈 Evolución Temporal de Contaminantes',
                    xaxis_title='Fecha',
                    yaxis_title='Concentración',
                    height=600,
                    template='plotly_white',
                    hovermode='x unified'
                )

                return fig
            else:
                return create_empty_correlation_figure("Sin datos temporales disponibles")

        except Exception as e:
            print(f"❌ Error creando correlación temporal: {e}")
            return create_empty_correlation_figure(f"Error: {str(e)}")

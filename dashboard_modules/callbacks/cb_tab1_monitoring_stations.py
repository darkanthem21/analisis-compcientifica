# dashboard_modules/callbacks/cb_tab1_monitoring_stations.py

from dash import Input, Output, callback, no_update
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_tab1_callbacks(app, df_estaciones, df_poblacion):
    """
    Registra todos los callbacks para la Pestaña 1.
    """

    # --- Callback 1: Actualizar el dropdown de Estaciones (VERSIÓN CON DEPURACIÓN) ---
    @app.callback(
        [Output('filtro-estacion-tab1', 'options'),
         Output('filtro-estacion-tab1', 'value'),
         Output('filtro-estacion-tab1', 'disabled')],
        [Input('filtro-region-tab1', 'value')]
    )
    def update_station_dropdown(selected_region):
        # --- Inicio de Depuración ---
        print("\n--- Callback de Estación Activado ---")
        print(f"Región recibida como input: '{selected_region}' (tipo: {type(selected_region)})")
        # --- Fin de Depuración ---

        if not selected_region:
            print("  -> Input de región está vacío. Deshabilitando dropdown de estación.")
            return [], None, True # Si no hay región, el dropdown de estación está vacío y deshabilitado

        # Filtrar las estaciones para la región seleccionada
        estaciones_en_region = sorted(df_estaciones[df_estaciones['region'] == selected_region]['estacion'].unique())

        # --- Inicio de Depuración ---
        print(f"  -> Estaciones encontradas para '{selected_region}': {estaciones_en_region}")
        # --- Fin de Depuración ---

        if not estaciones_en_region:
            print(f"  -> No se encontraron estaciones para '{selected_region}'. Devolviendo dropdown vacío y deshabilitado.")
            return [], None, True

        # Crear las opciones para el dropdown
        opciones_estaciones = [{'label': estacion, 'value': estacion} for estacion in estaciones_en_region]

        # Valor por defecto para el dropdown (la primera estación de la lista)
        valor_inicial_estacion = opciones_estaciones[0]['value']

        # --- Inicio de Depuración ---
        print(f"  -> Opciones generadas para el dropdown: {opciones_estaciones}")
        print(f"  -> Valor inicial seleccionado: '{valor_inicial_estacion}'")
        print("  -> Habilitando dropdown y devolviendo valores.")
        # --- Fin de Depuración ---

        # Devolver las opciones, seleccionar la primera por defecto y habilitar el dropdown
        return opciones_estaciones, valor_inicial_estacion, False

    # ... (El resto de tus callbacks, update_station_graph y update_kpi_cards, se mantienen igual) ...

    # --- Callback 2: Actualizar el Gráfico de Series de Tiempo ---
    @app.callback(
        Output('grafico-series-tiempo-estacion', 'figure'),
        [Input('filtro-estacion-tab1', 'value'),
         Input('filtro-contaminante-tab1', 'value'),
         Input('filtro-año-desde-tab1', 'value'),
         Input('filtro-año-hasta-tab1', 'value'),
         Input('filtro-region-tab1', 'value')]
    )
    def update_station_graph(selected_station, selected_pollutant, start_year, end_year, selected_region):
        if not all([selected_station, selected_pollutant, start_year, end_year, selected_region]):
            return go.Figure().update_layout(
                title_text="Por favor, seleccione todos los filtros",
                xaxis_title="Fecha",
                yaxis_title="Concentración"
            )

        df_filtrado = df_estaciones[
            (df_estaciones['region'] == selected_region) &
            (df_estaciones['estacion'] == selected_station) &
            (df_estaciones['timestamp'].dt.year >= start_year) &
            (df_estaciones['timestamp'].dt.year <= end_year)
        ]

        fig = px.line(
            df_filtrado,
            x='timestamp',
            y=selected_pollutant,
            title=f'Concentración de {selected_pollutant.upper()} en {selected_station}',
            labels={'timestamp': 'Fecha', selected_pollutant: f'Concentración ({selected_pollutant.upper()})'}
        )

        fig.update_traces(mode='lines+markers', marker=dict(size=4))

        return fig

    # --- Callback 3: Actualizar las Tarjetas de KPI ---
    @app.callback(
        [Output('kpi-cantidad-estaciones', 'children'),
         Output('kpi-poblacion-pct', 'children')],
        [Input('filtro-region-tab1', 'value'),
         Input('filtro-año-desde-tab1', 'value'),
         Input('filtro-año-hasta-tab1', 'value')]
    )
    def update_kpi_cards(selected_region, start_year, end_year):
        if not all([selected_region, start_year, end_year]):
            return "N/A", "N/A"

        cantidad_estaciones = df_estaciones[df_estaciones['region'] == selected_region]['estacion'].nunique()

        df_pob_filtrada = df_poblacion[
            (df_poblacion['año'] >= start_year) &
            (df_poblacion['año'] <= end_year)
        ]

        pob_total_chile = df_pob_filtrada[df_pob_filtrada['año'] == end_year]['poblacion'].sum()
        pob_region_seleccionada = df_pob_filtrada[
            (df_pob_filtrada['año'] == end_year) &
            (df_pob_filtrada['region'] == selected_region)
        ]['poblacion'].sum()

        if pob_total_chile > 0:
            porcentaje_poblacion = f"{(pob_region_seleccionada / pob_total_chile) * 100:.1f}%"
        else:
            porcentaje_poblacion = "N/A"

        return f"{cantidad_estaciones}", porcentaje_poblacion

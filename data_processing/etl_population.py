import os
import pandas as pd
import numpy as np

# --- Constantes y Configuraciones ---

COLUMNAS_ID_RAW = ['Region', 'Sexo', 'Edad']
COLUMNAS_ESTANDAR_ETL_POP = ['codigo_region', 'region', 'año', 'poblacion']

MAPA_CODIGO_A_NOMBRE_REGION = {
    1: 'Tarapacá',
    2: 'Antofagasta',
    3: 'Atacama',
    4: 'Coquimbo',
    5: 'Valparaíso',
    6: "O'Higgins",
    7: 'Maule',
    8: 'Biobío',
    9: 'Araucanía',
    10: 'Los Lagos',
    11: 'Aysén',
    12: 'Magallanes',
    13: 'Metropolitana',
    14: 'Los Ríos',
    15: 'Arica y Parinacota',
    16: 'Ñuble'
}

def procesar_datos_poblacion(ruta_csv_poblacion_raw, ruta_archivo_salida_procesado):
    """
    Carga y transforma los datos de población de formato ancho a largo.
    Agrupa por región para obtener la población total, limpia los datos
    y los guarda en un archivo pickle.
    """
    print(f"INFO ETL-POP: Iniciando carga de datos de población desde: {ruta_csv_poblacion_raw}")

    try:
        # El archivo es separado por comas.
        df_poblacion_raw = pd.read_csv(ruta_csv_poblacion_raw, sep=',', encoding='latin-1')
        print(f"INFO ETL-POP: Archivo de población leído exitosamente.")
    except FileNotFoundError:
        print(f"ERROR CRÍTICO ETL-POP: No se encontró el archivo de población en '{ruta_csv_poblacion_raw}'")
        return None
    except Exception as e:
        print(f"ERROR CRÍTICO ETL-POP al leer el archivo de población: {type(e).__name__} - {e}")
        return None

    print(f"DEBUG ETL-POP: Columnas reales leídas: {df_poblacion_raw.columns.tolist()}")

    # --- Transformación de Formato Ancho a Largo (Melt) ---
    print("INFO ETL-POP: Transformando datos de formato ancho a largo (melt)...")

    columnas_id_melt = [col for col in COLUMNAS_ID_RAW if col in df_poblacion_raw.columns]
    if len(columnas_id_melt) != len(COLUMNAS_ID_RAW):
        print(f"ERROR CRÍTICO ETL-POP: Faltan columnas de ID esperadas ('Region', 'Sexo', 'Edad'). Se encontraron: {columnas_id_melt}")
        return None

    columnas_años_raw = [col for col in df_poblacion_raw.columns if col.startswith('a')]

    df_poblacion_largo = df_poblacion_raw.melt(
        id_vars=columnas_id_melt,
        value_vars=columnas_años_raw,
        var_name='año',
        value_name='poblacion'
    )

    print("INFO ETL-POP: Transformación a formato largo completada.")

    # --- Limpieza y Agrupación ---
    print("INFO ETL-POP: Limpiando y agrupando datos...")

    # 1. Limpiar la columna 'año' para quitar la 'a' inicial y convertir a número
    df_poblacion_largo['año'] = df_poblacion_largo['año'].str.replace('a', '').astype(int)

    # 2. Convertir población a numérico
    df_poblacion_largo['poblacion'] = pd.to_numeric(df_poblacion_largo['poblacion'], errors='coerce').fillna(0).astype(int)

    # 3. Eliminar desglose por Sexo y Edad agrupando y sumando la población
    #    Se agrupa por el CÓDIGO de la región ('Region') y por 'año'.
    print("INFO ETL-POP: Agrupando por código de región y año para obtener población total...")
    df_agrupado = df_poblacion_largo.groupby(['Region', 'año'])['poblacion'].sum().reset_index()

    # 4. Renombrar la columna de código y mapear para crear la columna con el nombre de la región
    df_agrupado.rename(columns={'Region': 'codigo_region'}, inplace=True)
    df_agrupado['region'] = df_agrupado['codigo_region'].map(MAPA_CODIGO_A_NOMBRE_REGION)

    # 5. Verificar si algún código de región no se pudo mapear
    if df_agrupado['region'].isnull().any():
        codigos_no_mapeados = df_agrupado[df_agrupado['region'].isnull()]['codigo_region'].unique()
        print(f"ADVERTENCIA ETL-POP: Los siguientes códigos de región no pudieron ser mapeados a un nombre: {codigos_no_mapeados}")
        df_agrupado.dropna(subset=['region'], inplace=True) # Eliminar filas que no se pudieron mapear

    # 6. Seleccionar y reordenar las columnas finales
    # Asegurarse que todas las columnas estándar existan antes de seleccionar
    columnas_finales_presentes = [col for col in COLUMNAS_ESTANDAR_ETL_POP if col in df_agrupado.columns]
    df_final = df_agrupado[columnas_finales_presentes]

    print(f"--- Preparación de Datos de Población Finalizada ---")
    print(f"DataFrame de Población final listo con {df_final.shape[0]} filas.")

    return df_final

# --- Bloque de Ejecución ---
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Corrección para la ruta si la carpeta se llama 'data_processsing' con 'ss'
    if 'data_processsing' in script_dir:
        project_root = os.path.dirname(os.path.dirname(script_dir))

    path_raw_pop_data = os.path.join(project_root, 'data', 'raw', 'population', 'ine_estimaciones-y-proyecciones-2002-2035_base-2017_region_base.csv')

    path_processed_dir = os.path.join(project_root, 'data', 'processed')
    os.makedirs(path_processed_dir, exist_ok=True)
    path_output_processed_file = os.path.join(path_processed_dir, 'population_processed.pkl')

    print(f"Ruta de datos raw de Población: {path_raw_pop_data}")
    print(f"Ruta de salida para datos procesados: {path_output_processed_file}")

    df_poblacion_procesado = procesar_datos_poblacion(
        ruta_csv_poblacion_raw=path_raw_pop_data,
        ruta_archivo_salida_procesado=path_output_processed_file
    )

    if df_poblacion_procesado is not None and not df_poblacion_procesado.empty:
        try:
            df_poblacion_procesado.to_pickle(path_output_processed_file)
            print(f"\nINFO ETL-POP: Datos de población procesados y guardados en: {path_output_processed_file}")
            print(f"INFO ETL-POP: Dimensiones del archivo guardado: {df_poblacion_procesado.shape}")
            if not df_poblacion_procesado.empty:
                 print(f"INFO ETL-POP: Columnas del archivo guardado: {df_poblacion_procesado.columns.tolist()}")
                 print("INFO ETL-POP: Primeras filas del archivo guardado:")
                 print(df_poblacion_procesado.head())
                 print("\nINFO ETL-POP: Últimas filas del archivo guardado:")
                 print(df_poblacion_procesado.tail())

        except Exception as e:
            print(f"ERROR CRÍTICO ETL-POP al guardar el archivo procesado de población: {type(e).__name__} - {e}")
    else:
        print("ERROR ETL-POP: No se generaron datos de población procesados para guardar (DataFrame vacío o None).")

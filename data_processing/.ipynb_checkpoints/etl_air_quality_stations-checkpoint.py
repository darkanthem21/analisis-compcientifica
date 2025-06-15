import os
import pandas as pd
import numpy as np
import glob

# --- Constantes y Configuraciones ---

# Columnas de contaminantes que esperamos encontrar y procesar en los archivos de AirQualitySM
# Estas son las columnas que se convertirán a numérico.
COLUMNAS_CONTAMINANTES_AQ = ['pm25', 'pm10', 'o3', 'no2', 'co', 'so2']

# Columnas finales que queremos en nuestro archivo procesado.
COLUMNAS_ESTANDAR_ETL_AQ = ['timestamp', 'region', 'estacion', 'pm25', 'pm10', 'o3', 'no2', 'co', 'so2']


def procesar_datos_estaciones_calidad_aire(ruta_base_aqsm_raw, ruta_archivo_salida_procesado):
    """
    Carga, limpia, unifica y guarda los datos de todas las estaciones de monitoreo
    de la carpeta AirQualitySM.
    """
    # Usar glob para encontrar todos los subdirectorios de regiones en AirQualitySM
    patron_regiones = os.path.join(ruta_base_aqsm_raw, '*')
    lista_directorios_regiones = [d for d in glob.glob(patron_regiones) if os.path.isdir(d)]
    
    if not lista_directorios_regiones:
        print(f"ERROR ETL-AQ: No se encontraron directorios de regiones en '{ruta_base_aqsm_raw}'")
        return pd.DataFrame()

    todos_los_datos_estaciones = []
    print(f"INFO ETL-AQ: Iniciando carga de datos de estaciones desde: {ruta_base_aqsm_raw}")
    print(f"INFO ETL-AQ: Se encontraron {len(lista_directorios_regiones)} directorios de regiones.")

    for dir_region in lista_directorios_regiones:
        nombre_region = os.path.basename(dir_region)
        print(f"  Procesando Región: {nombre_region}")

        # Encontrar todos los archivos CSV dentro del directorio de la región
        patron_estaciones_csv = os.path.join(dir_region, '*.csv')
        lista_archivos_estacion = glob.glob(patron_estaciones_csv)

        if not lista_archivos_estacion:
            print(f"    ADVERTENCIA ETL-AQ: No se encontraron archivos CSV en la carpeta de la región '{nombre_region}'.")
            continue

        for ruta_archivo_estacion in lista_archivos_estacion:
            nombre_archivo_base = os.path.basename(ruta_archivo_estacion)
            # Extraer el nombre de la estación del nombre del archivo (antes de la primera coma o guion)
            nombre_estacion = nombre_archivo_base.split(',')[0].split('-')[0].replace('_', ' ').strip().title()
            print(f"    Leyendo Estación: '{nombre_estacion}' (de archivo: {nombre_archivo_base})")

            try:
                # Los archivos de waqi.info suelen tener un encabezado y pie de página que hay que saltar
                # pero Pandas es a menudo lo suficientemente inteligente para manejarlo si el formato es estándar.
                # Si esto falla, podríamos necesitar 'skiprows'
                df_estacion = pd.read_csv(ruta_archivo_estacion, comment='#', on_bad_lines='skip')
                
                if df_estacion.empty:
                    print(f"      ADVERTENCIA ETL-AQ: Archivo '{nombre_archivo_base}' está vacío o no se pudo leer correctamente.")
                    continue
                
                # Limpieza de columnas (eliminar espacios)
                df_estacion.columns = df_estacion.columns.str.strip()

                # --- Limpieza y Estandarización del DataFrame de la Estación ---
                
                # 1. Manejo de la Fecha/Hora
                if 'date' not in df_estacion.columns:
                    print(f"      ERROR ETL-AQ: Archivo '{nombre_archivo_base}' no tiene la columna 'date'. Saltando archivo.")
                    continue
                
                df_estacion['timestamp'] = pd.to_datetime(df_estacion['date'], errors='coerce')
                # Eliminar filas donde la fecha no se pudo convertir
                df_estacion.dropna(subset=['timestamp'], inplace=True)

                # 2. Añadir columnas de Región y Estación
                df_estacion['region'] = nombre_region
                df_estacion['estacion'] = nombre_estacion

                # 3. Procesar columnas de contaminantes
                for col_contaminante in COLUMNAS_CONTAMINANTES_AQ:
                    if col_contaminante in df_estacion.columns:
                        # Convertir a numérico, los no-números (ej. ' ') se volverán NaN
                        df_estacion[col_contaminante] = pd.to_numeric(df_estacion[col_contaminante], errors='coerce')
                    else:
                        # Si una columna de contaminante no existe en el archivo, la creamos con NaN
                        df_estacion[col_contaminante] = np.nan
                
                # 4. Seleccionar y reordenar las columnas estándar
                columnas_presentes = [col for col in COLUMNAS_ESTANDAR_ETL_AQ if col in df_estacion.columns]
                df_estacion_limpia = df_estacion[columnas_presentes]
                
                todos_los_datos_estaciones.append(df_estacion_limpia)

            except Exception as e:
                print(f"      ERROR CRÍTICO ETL-AQ procesando el archivo '{nombre_archivo_base}': {type(e).__name__} - {e}")
                continue

    if not todos_los_datos_estaciones:
        print("\nERROR CRÍTICO ETL-AQ: No se cargaron datos válidos de ninguna estación.")
        return pd.DataFrame()

    print(f"\nINFO ETL-AQ: Unificando datos de {len(todos_los_datos_estaciones)} archivos de estaciones...")
    try:
        df_unificado = pd.concat(todos_los_datos_estaciones, ignore_index=True, sort=False)
    except Exception as error_concat:
        print(f"ERROR CRÍTICO ETL-AQ al concatenar DataFrames de estaciones: {error_concat}")
        return pd.DataFrame()
    
    # Limpieza final del DataFrame unificado
    # Eliminar filas donde TODOS los contaminantes son NaN, ya que no aportan información
    filas_antes_nan = len(df_unificado)
    df_unificado.dropna(subset=COLUMNAS_CONTAMINANTES_AQ, how='all', inplace=True)
    filas_despues_nan = len(df_unificado)
    print(f"INFO ETL-AQ: Limpieza final: Se eliminaron {filas_antes_nan - filas_despues_nan} filas donde todos los valores de contaminantes eran nulos.")
    
    # Ordenar por fecha y región para mejor organización
    df_unificado.sort_values(by=['region', 'estacion', 'timestamp'], inplace=True)
    
    print(f"--- Preparación de Datos de Estaciones Finalizada ---")
    print(f"DataFrame de Estaciones final listo con {df_unificado.shape[0]} filas y {df_unificado.shape[1]} columnas.")
    
    return df_unificado

# --- Bloque de Ejecución ---
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    path_raw_aq_data = os.path.join(project_root, 'data', 'raw', 'AirQualitySM')
    
    path_processed_dir = os.path.join(project_root, 'data', 'processed')
    os.makedirs(path_processed_dir, exist_ok=True)
    path_output_processed_file = os.path.join(path_processed_dir, 'air_quality_stations_processed.pkl')

    print(f"Ruta de datos raw AirQualitySM: {path_raw_aq_data}")
    print(f"Ruta de salida para datos procesados: {path_output_processed_file}")

    df_estaciones_procesado = procesar_datos_estaciones_calidad_aire(
        ruta_base_aqsm_raw=path_raw_aq_data,
        ruta_archivo_salida_procesado=path_output_processed_file
    )

    if df_estaciones_procesado is not None and not df_estaciones_procesado.empty:
        try:
            df_estaciones_procesado.to_pickle(path_output_processed_file)
            print(f"\nINFO ETL-AQ: Datos de estaciones procesados y guardados en: {path_output_processed_file}")
            print(f"INFO ETL-AQ: Dimensiones del archivo guardado: {df_estaciones_procesado.shape}")
            if not df_estaciones_procesado.empty:
                 print(f"INFO ETL-AQ: Columnas del archivo guardado: {df_estaciones_procesado.columns.tolist()}")
                 print("INFO ETL-AQ: Primeras filas del archivo guardado:")
                 print(df_estaciones_procesado.head())
                 print("\nINFO ETL-AQ: Conteo de registros por región:")
                 print(df_estaciones_procesado['region'].value_counts())
                 print("\nINFO ETL-AQ: Conteo de NaNs por columna de contaminante en el archivo guardado:")
                 print(df_estaciones_procesado[COLUMNAS_CONTAMINANTES_AQ].isnull().sum())
        except Exception as e:
            print(f"ERROR CRÍTICO ETL-AQ al guardar el archivo procesado de estaciones: {type(e).__name__} - {e}")
    else:
        print("ERROR ETL-AQ: No se generaron datos de estaciones procesados para guardar (DataFrame vacío o None).")
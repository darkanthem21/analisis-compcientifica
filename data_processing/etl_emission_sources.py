import os
import pandas as pd
import numpy as np
import glob # Útil para encontrar archivos con patrones

# --- Constantes y Configuraciones ---
# Años a procesar (como strings, igual que en tu notebook)
AÑOS_A_PROCESAR = [str(año) for año in range(2019, 2024)]

# Mapeo de los nombres de las subcarpetas en data/raw/RECT/ a los tipos de fuente descriptivos
TIPOS_FUENTE_DESCRIPTIVOS_MAP = {
    'difusas': 'Difusas',
    'puntuales': 'Puntuales (EFP)', # Establecimientos Fijo-Puntuales
    'ruta': 'En Ruta (TR)'       # Transporte en Ruta
}
# Nombres de las subcarpetas raw (deben coincidir con los nombres de directorio)
SUBCARPETAS_RAW = ['difusas', 'puntuales', 'ruta']

# Columnas estándar que se esperan en el DataFrame final después del procesamiento
COLUMNAS_ESTANDAR_ETL = ['año', 'region', 'comuna', 'cantidad_toneladas', 'contaminante', 'tipo_fuente']

# Mapeos para estandarizar nombres de contaminantes (de tu analisis.ipynb)
MAPA_CONTAMINANTES_ESTANDAR = {
    'NOx ': 'NOx',
    'Nitrogen oxides (NOx)': 'NOx',
    'NOx': 'NOx',
    'Compuestos Orgánicos Volátiles': 'COV',
    'Volatile organic compounds (VOC)': 'COV',
    'COV': 'COV',

    # CO2 (Dióxido de Carbono)
    'Carbon dioxide': 'Dióxido de carbono (CO2)',
    'Dióxido de carbono (CO2)': 'Dióxido de carbono (CO2)',

    # CO (Monóxido de Carbono)
    'Carbon monoxide': 'Monóxido de carbono (CO)',
    'Monóxido de carbono': 'Monóxido de carbono (CO)',
    'Monóxido de carbono (CO)': 'Monóxido de carbono (CO)',

    # SO2 (Dióxido de Azufre)
    'Sulfur dioxide': 'Dióxido de azufre (SO2)',
    'Dióxido de azúfre (SO2)': 'Dióxido de azufre (SO2)', # Corregir tilde si es necesario
    'Dióxido de azufre (SO2)': 'Dióxido de azufre (SO2)',

    # SOx (Óxidos de Azufre)
    'Sulfur oxides (SOx)': 'SOx',
    'SOx': 'SOx',

    # Arsénico
    'Arsenic': 'Arsénico',
    'Arsénico': 'Arsénico',

    # Plomo
    'Lead': 'Plomo',
    'Plomo': 'Plomo',

    # Mercurio
    'Mercury': 'Mercurio',
    'Mercurio': 'Mercurio',

    # Amoniaco (NH3)
    'Ammonia': 'Amoniaco (NH3)',
    'Nitrógeno amoniacal (o NH3)': 'Amoniaco (NH3)',
    'Amoniaco (NH3)': 'Amoniaco (NH3)',

    # MP2.5
    'MP2,5': 'MP2.5', # Con coma
    'PM2.5, primary': 'MP2.5',
    'MP2.5': 'MP2.5', # Estándar

    # MP10
    'PM10, primary': 'MP10',
    'MP10': 'MP10', # Estándar

    # Material Particulado Total
    'PM, primary': 'Material Particulado Total',
    'Material particulado': 'Material Particulado Total',
    'Material Particulado Total': 'Material Particulado Total',

    # Tolueno
    'Toluene': 'Tolueno',
    'Tolueno / metil benceno / Toluol / Fenilmetano': 'Tolueno',
    'Tolueno': 'Tolueno',

    # Benceno
    'Benzene': 'Benceno',
    'Benceno': 'Benceno',

    # PCDD/F (Dioxinas y Furanos)
    'PCDD-F': 'Dibenzoparadioxinas policloradas y furanos (PCDD/F)',
    'Dibenzoparadioxinas policloradas y furanos (PCDD/F)': 'Dibenzoparadioxinas policloradas y furanos (PCDD/F)',

    # Contaminantes que no estaban antes pero aparecieron (decide el nombre estándar)
    'Carbono Negro': 'Carbono Negro', # O 'CN' si prefieres un código
    'Metano (CH4)': 'Metano (CH4)',
    'Oxido Nitroso': 'Óxido Nitroso (N2O)', # Sugerencia: añadir (N2O) y tilde
    'Hidrocarburos totales': 'Hidrocarburos Totales (HCT)'
}

# Mapeos para estandarizar nombres de regiones (de tu analisis.ipynb)
MAPEO_REGIONES_ESTANDAR = {
    'Metropolitana de Santiago': 'Metropolitana', 'Región Metropolitana de Santiago': 'Metropolitana',
    'Región del Gral. Carlos Ibáñez del Campo': 'Aysén',
    'Aysen del General Carlos Ibanez del Campo': 'Aysén',
    'Aysén del Gral. Carlos Ibañez del Campo': 'Aysén',
    'Aysén del Gral. Carlos Ibáñez del Campo':'Aysén',
    'Libertador Gral. Bernardo O Higgins': "O'Higgins", "O'Higgins": "O'Higgins",
    'Libertador General Bernardo O Higgins': "O'Higgins",
    "Libertador Gral. Bernardo O'Higgins":"O'Higgins",
    'Nuble': 'Ñuble',
    'Magallanes y de la Antártica Chilena':'Magallanes',
}
# --- FIN DE CONSTANTES ---


def cargar_y_preparar_datos_fuente(ruta_base_rect_raw, subcarpetas_fuentes_raw, lista_años,
                                   mapa_contaminantes_est, mapa_regiones_est, tipos_fuente_desc_map,
                                   debug_archivo_especifico=None):
    """
    Carga, renombra columnas, filtra, estandariza y unifica datos de emisiones de RECT.
    """
    todos_los_datos = []
    # Columnas internas temporales a las que se renombrarán las columnas originales
    cols_internas_map = {
        'region': 'region_raw',
        'comuna': 'comuna_raw',
        'cantidad_toneladas': 'cantidad_toneladas_raw',
        'contaminante': 'contaminante_raw'
    }

    print(f"DEBUG ETL: Iniciando carga y preparación desde: {ruta_base_rect_raw}")

    for año_actual in lista_años:
        if debug_archivo_especifico and debug_archivo_especifico["año"] != año_actual:
            continue
        print(f"DEBUG ETL: Procesando año: {año_actual}")

        for carpeta_raw in subcarpetas_fuentes_raw:
            if debug_archivo_especifico and debug_archivo_especifico["carpeta"] != carpeta_raw:
                continue

            ruta_carpeta_especifica = os.path.join(ruta_base_rect_raw, carpeta_raw)
            print(f"DEBUG ETL: Buscando en carpeta: {ruta_carpeta_especifica}")

            if not os.path.isdir(ruta_carpeta_especifica):
                print(f"    ADVERTENCIA ETL: Carpeta no encontrada: '{ruta_carpeta_especifica}'. Saltando.")
                continue

            patron_archivos = os.path.join(ruta_carpeta_especifica, f"*{año_actual}*")
            archivos_potenciales_glob = [f for f in glob.glob(patron_archivos) if f.lower().endswith(('.csv', '.xlsx', '.xls'))]

            if not archivos_potenciales_glob:
                print(f"    INFO ETL: No se encontró archivo para año {año_actual} en '{carpeta_raw}' con patrón '{patron_archivos}'.")
                continue

            archivos_csv = [f for f in archivos_potenciales_glob if f.lower().endswith('.csv')]
            if archivos_csv:
                ruta_archivo = archivos_csv[0]
            else:
                ruta_archivo = archivos_potenciales_glob[0]

            nombre_archivo_base = os.path.basename(ruta_archivo)
            if debug_archivo_especifico and debug_archivo_especifico["nombre_archivo"] != nombre_archivo_base:
                continue

            print(f"    INFO ETL: Intentando leer archivo: '{nombre_archivo_base}' de carpeta '{carpeta_raw}'")
            df_temporal = None

            try:
                if ruta_archivo.lower().endswith('.csv'):
                    encodings_to_try = ['utf-8', 'latin-1', 'windows-1252']
                    df_csv_cargado = None
                    for enc in encodings_to_try:
                        print(f"      DEBUG ETL: Intentando leer '{nombre_archivo_base}' con encoding '{enc}'...")
                        try:
                            df_csv_cargado = pd.read_csv(ruta_archivo, encoding=enc, sep=';', decimal=',', on_bad_lines='warn', low_memory=False)
                            print(f"      INFO ETL: Archivo '{nombre_archivo_base}' leído exitosamente con encoding '{enc}'.")
                            df_temporal = df_csv_cargado
                            break
                        except UnicodeDecodeError:
                            print(f"      ADVERTENCIA ETL: Falló la lectura de '{nombre_archivo_base}' con encoding '{enc}' (UnicodeDecodeError).")
                        except Exception as e_inner_csv:
                            print(f"      ERROR ETL leyendo CSV '{nombre_archivo_base}' con encoding '{enc}': {type(e_inner_csv).__name__} - {e_inner_csv}")
                            df_csv_cargado = None
                            break

                    if df_temporal is None:
                        print(f"      ERROR CRÍTICO ETL: No se pudo leer el archivo CSV '{nombre_archivo_base}' con los encodings probados. Saltando archivo.")
                        continue

                elif ruta_archivo.lower().endswith(('.xlsx', '.xls')):
                    print(f"      DEBUG ETL: Intentando leer archivo Excel '{nombre_archivo_base}'...")
                    try:
                        df_temporal = pd.read_excel(ruta_archivo, engine='openpyxl')
                        print(f"      INFO ETL: Archivo Excel '{nombre_archivo_base}' leído exitosamente.")
                    except ImportError:
                        print(f"      ERROR CRÍTICO ETL: Falta 'openpyxl'. Instala con 'pip install openpyxl'. Saltando '{nombre_archivo_base}'.")
                        continue
                    except Exception as e_excel:
                        print(f"      ERROR CRÍTICO ETL: Falló la lectura Excel '{nombre_archivo_base}'. Error: {type(e_excel).__name__} - {e_excel}. Saltando.")
                        continue
            except Exception as error_general_lectura:
                 print(f"      ERROR INESPERADO ETL durante lectura de {nombre_archivo_base}: {type(error_general_lectura).__name__} - {error_general_lectura}. Saltando.")
                 continue

            if df_temporal is None or df_temporal.empty:
                print(f"      INFO ETL: Archivo '{nombre_archivo_base}' vacío o no leído. Saltando post-procesamiento para este archivo.")
                continue

            print(f"      DEBUG ETL: Archivo '{nombre_archivo_base}' cargado. Filas: {len(df_temporal)}, Columnas originales: {df_temporal.columns.tolist()}")

            if debug_archivo_especifico and debug_archivo_especifico["nombre_archivo"] == nombre_archivo_base:
                print(f"\n      --- DIAGNÓSTICO DETALLADO para '{nombre_archivo_base}' ---")
                print(f"      Columnas Originales (antes de strip): {df_temporal.columns.tolist()}")

            df_temporal.columns = df_temporal.columns.str.strip()
            print(f"      DEBUG ETL: Columnas después de strip(): {df_temporal.columns.tolist()}")

            df_temporal['año_original_carga'] = año_actual
            df_temporal['origen_carpeta_carga'] = carpeta_raw

            # --- Lógica de Renombrado Mejorada ---
            dicc_renombrar_a_raw = {}
            # REGION
            if 'REGION' in df_temporal.columns: dicc_renombrar_a_raw['REGION'] = cols_internas_map['region']
            elif 'nom_region' in df_temporal.columns: dicc_renombrar_a_raw['nom_region'] = cols_internas_map['region']
            elif 'region' in df_temporal.columns: dicc_renombrar_a_raw['region'] = cols_internas_map['region'] # Si ya se llama 'region'

            # COMUNA
            if 'NOM_COM' in df_temporal.columns: dicc_renombrar_a_raw['NOM_COM'] = cols_internas_map['comuna']
            elif 'Comuna_Ruta' in df_temporal.columns: dicc_renombrar_a_raw['Comuna_Ruta'] = cols_internas_map['comuna']
            elif 'comuna' in df_temporal.columns: dicc_renombrar_a_raw['comuna'] = cols_internas_map['comuna'] # Si ya se llama 'comuna'

            # CONTAMINANTE
            if 'codigo_parametro' in df_temporal.columns: dicc_renombrar_a_raw['codigo_parametro'] = cols_internas_map['contaminante']
            elif 'codigo_parameter' in df_temporal.columns: dicc_renombrar_a_raw['codigo_parameter'] = cols_internas_map['contaminante']
            elif 'codigo_contaminante_ruta' in df_temporal.columns: dicc_renombrar_a_raw['codigo_contaminante_ruta'] = cols_internas_map['contaminante']
            elif 'contaminantes' in df_temporal.columns: dicc_renombrar_a_raw['contaminantes'] = cols_internas_map['contaminante']
            elif 'contaminante' in df_temporal.columns: dicc_renombrar_a_raw['contaminante'] = cols_internas_map['contaminante'] # Si ya se llama 'contaminante'

            # CANTIDAD
            if 'cantidad_toneladas' in df_temporal.columns:
                dicc_renombrar_a_raw['cantidad_toneladas'] = cols_internas_map['cantidad_toneladas']

            if dicc_renombrar_a_raw:
                columnas_a_renombrar_efectivamente = {k: v for k, v in dicc_renombrar_a_raw.items() if k in df_temporal.columns}
                df_temporal.rename(columns=columnas_a_renombrar_efectivamente, inplace=True)
                print(f"      DEBUG ETL: Columnas después de renombrado a _raw: {df_temporal.columns.tolist()}")
            else:
                print(f"      DEBUG ETL: No se aplicó ningún renombrado dinámico a _raw para {nombre_archivo_base}.")

            for col_std_original, col_raw_target in cols_internas_map.items():
                if col_raw_target not in df_temporal.columns:
                    print(f"      ADVERTENCIA ETL: Columna '{col_raw_target}' (para '{col_std_original}') no existe después del renombrado desde '{nombre_archivo_base}'. Se crea como NaN.")
                    df_temporal[col_raw_target] = np.nan
                elif debug_archivo_especifico and debug_archivo_especifico["nombre_archivo"] == nombre_archivo_base:
                     print(f"      DEBUG VALS '{col_raw_target}' (primeros 5 únicos no nulos): {df_temporal[col_raw_target].dropna().unique()[:5]}")

            todos_los_datos.append(df_temporal)

            if debug_archivo_especifico and debug_archivo_especifico["nombre_archivo"] == nombre_archivo_base:
                print("DEBUG ETL: Se procesó el archivo de depuración específico. Terminando bucles de carga.")
                if todos_los_datos:
                    df_unificado_debug = pd.concat(todos_los_datos, ignore_index=True, sort=False)
                    df_limpio_debug = pd.DataFrame() # Para construir el df limpio
                    df_limpio_debug['año'] = df_unificado_debug['año_original_carga'].astype(str)
                    df_limpio_debug['tipo_fuente'] = df_unificado_debug['origen_carpeta_carga'].map(tipos_fuente_desc_map).fillna(df_unificado_debug['origen_carpeta_carga'])

                    print(f"      DEBUG VALS (DEBUG MODE) - Antes de estandarizar region: {df_unificado_debug[cols_internas_map['region']].dropna().unique()[:10]}")
                    df_limpio_debug['region'] = df_unificado_debug[cols_internas_map['region']].astype(str).str.strip().replace(mapa_regiones_est)
                    print(f"      DEBUG VALS (DEBUG MODE) - Después de estandarizar region: {df_limpio_debug['region'].dropna().unique()[:10]}")

                    print(f"      DEBUG VALS (DEBUG MODE) - Antes de estandarizar comuna: {df_unificado_debug[cols_internas_map['comuna']].dropna().unique()[:10]}")
                    df_limpio_debug['comuna'] = df_unificado_debug[cols_internas_map['comuna']].astype(str).str.strip().str.title()
                    print(f"      DEBUG VALS (DEBUG MODE) - Después de estandarizar comuna: {df_limpio_debug['comuna'].dropna().unique()[:10]}")

                    df_limpio_debug['contaminante_raw_val_debug'] = df_unificado_debug[cols_internas_map['contaminante']] # Solo para ver
                    df_limpio_debug['contaminante'] = df_unificado_debug[cols_internas_map['contaminante']].astype(str).str.strip()
                    df_limpio_debug['contaminante'] = df_limpio_debug['contaminante'].apply(lambda x: mapa_contaminantes_est.get(x, x))
                    df_limpio_debug['cantidad_toneladas'] = pd.to_numeric(df_unificado_debug[cols_internas_map['cantidad_toneladas']], errors='coerce')

                    print("\n--- DEBUG: DataFrame del Archivo Específico ANTES de dropna ---")
                    columnas_para_mostrar_debug = ['año', 'region', 'comuna', 'cantidad_toneladas', 'contaminante', 'tipo_fuente',
                                                 cols_internas_map['region'], cols_internas_map['comuna'], cols_internas_map['contaminante']]
                    columnas_existentes_para_mostrar = [c for c in columnas_para_mostrar_debug if c in df_limpio_debug.columns]

                    print(df_limpio_debug[columnas_existentes_para_mostrar].head(20))
                    print(f"NaNs en 'region' (antes dropna): {df_limpio_debug['region'].isnull().sum()}, NaNs en 'comuna' (antes dropna): {df_limpio_debug['comuna'].isnull().sum()}")

                    columnas_clave_para_dropna_final = ['año', 'region', 'comuna', 'cantidad_toneladas', 'contaminante', 'tipo_fuente']
                    df_limpio_debug.dropna(subset=columnas_clave_para_dropna_final, inplace=True)

                    print("\n--- DEBUG: DataFrame del Archivo Específico DESPUÉS de dropna ---")
                    print(df_limpio_debug[COLUMNAS_ESTANDAR_ETL].head(20))
                    print(f"NaNs en 'region' (después dropna): {df_limpio_debug['region'].isnull().sum()}, NaNs en 'comuna' (después dropna): {df_limpio_debug['comuna'].isnull().sum()}")

                    # Asegurar que las columnas finales existan antes de intentar seleccionarlas
                    final_cols_present = [col for col in COLUMNAS_ESTANDAR_ETL if col in df_limpio_debug.columns]
                    return df_limpio_debug[final_cols_present].copy()
                return pd.DataFrame()

    if not todos_los_datos:
        print("\nERROR CRÍTICO ETL: No se cargaron datos válidos de ninguna fuente de RECT.")
        return pd.DataFrame()

    print(f"\nINFO ETL: Unificando datos de {len(todos_los_datos)} DataFrame(s) cargados de RECT...")
    try:
        df_unificado = pd.concat(todos_los_datos, ignore_index=True, sort=False)
    except Exception as error_concat:
        print(f"ERROR CRÍTICO ETL al concatenar DataFrames de RECT: {error_concat}")
        return pd.DataFrame()
    print(f"INFO ETL: DataFrame RECT unificado creado con {df_unificado.shape[0]} filas y {df_unificado.shape[1]} columnas antes de la limpieza final.")

    df_limpio = pd.DataFrame()
    df_limpio['año'] = df_unificado['año_original_carga'].astype(str)
    df_limpio['tipo_fuente'] = df_unificado['origen_carpeta_carga'].map(tipos_fuente_desc_map).fillna(df_unificado['origen_carpeta_carga'])

    print("DEBUG ETL: Aplicando estandarización final a 'region', 'comuna', 'contaminante' y 'cantidad_toneladas'")
    df_limpio['region'] = df_unificado[cols_internas_map['region']].astype(str).str.strip().replace(mapa_regiones_est)
    df_limpio['comuna'] = df_unificado[cols_internas_map['comuna']].astype(str).str.strip().str.title()

    # Para ver qué valores de contaminante_raw están llegando antes del mapeo
    df_limpio['contaminante_raw_val_final_debug'] = df_unificado[cols_internas_map['contaminante']].astype(str).str.strip()
    print(f"DEBUG ETL: Valores únicos de contaminante_raw_val_final_debug (top 20): {df_limpio['contaminante_raw_val_final_debug'].value_counts().nlargest(50)}")

    df_limpio['contaminante'] = df_unificado[cols_internas_map['contaminante']].astype(str).str.strip()
    df_limpio['contaminante'] = df_limpio['contaminante'].apply(lambda x: mapa_contaminantes_est.get(x, x))

    df_limpio['cantidad_toneladas'] = pd.to_numeric(df_unificado[cols_internas_map['cantidad_toneladas']], errors='coerce')
    print(f"DEBUG ETL: NaNs en 'cantidad_toneladas' después de to_numeric (final): {df_limpio['cantidad_toneladas'].isnull().sum()}")

    columnas_clave_para_dropna_final = ['año', 'region', 'comuna', 'cantidad_toneladas', 'contaminante', 'tipo_fuente']

    filas_antes_nan = len(df_limpio)
    df_limpio.dropna(subset=columnas_clave_para_dropna_final, inplace=True)
    filas_despues_nan = len(df_limpio)
    print(f"INFO ETL: Limpieza final: Se eliminaron {filas_antes_nan - filas_despues_nan} filas con valores nulos en columnas clave para el dashboard.")

    if 'cantidad_toneladas' in df_limpio.columns and pd.api.types.is_numeric_dtype(df_limpio['cantidad_toneladas']):
        neg_count = (df_limpio['cantidad_toneladas'] < 0).sum()
        if neg_count > 0:
             print(f"  ADVERTENCIA ETL: Se encontraron {neg_count} registros con valores negativos en 'cantidad_toneladas' en el DF final.")
    else:
        print("ADVERTENCIA ETL: La columna 'cantidad_toneladas' no es numérica en el df_limpio final o no existe.")

    if df_limpio.empty:
        print("ERROR CRÍTICO ETL: No quedan datos válidos después de la limpieza final de NaNs en RECT.")
        return pd.DataFrame()

    columnas_finales_presentes = [col for col in COLUMNAS_ESTANDAR_ETL if col in df_limpio.columns]
    if len(columnas_finales_presentes) != len(COLUMNAS_ESTANDAR_ETL):
        faltantes = set(COLUMNAS_ESTANDAR_ETL) - set(columnas_finales_presentes)
        print(f"ERROR CRÍTICO ETL: No todas las columnas estándar finales están presentes. Faltan: {faltantes}")

    df_final_seleccionado = df_limpio[columnas_finales_presentes].copy()

    print(f"--- Preparación de Datos RECT Finalizada ---")
    print(f"DataFrame RECT final listo con {df_final_seleccionado.shape[0]} filas y {df_final_seleccionado.shape[1]} columnas.")
    return df_final_seleccionado

# --- Bloque de Ejecución ---
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    path_raw_rect_data = os.path.join(project_root, 'data', 'raw', 'RECT')

    path_processed_dir = os.path.join(project_root, 'data', 'processed')
    os.makedirs(path_processed_dir, exist_ok=True)
    path_output_processed_file = os.path.join(path_processed_dir, 'emission_sources_processed.pkl')

    debug_file_info = None

    print(f"Ruta de datos raw RECT: {path_raw_rect_data}")
    print(f"Ruta de salida para datos procesados: {path_output_processed_file}")

    df_emisiones_procesado = cargar_y_preparar_datos_fuente(
        ruta_base_rect_raw=path_raw_rect_data,
        subcarpetas_fuentes_raw=SUBCARPETAS_RAW,
        lista_años=AÑOS_A_PROCESAR,
        mapa_contaminantes_est=MAPA_CONTAMINANTES_ESTANDAR,
        mapa_regiones_est=MAPEO_REGIONES_ESTANDAR,
        tipos_fuente_desc_map=TIPOS_FUENTE_DESCRIPTIVOS_MAP,
        debug_archivo_especifico=debug_file_info
    )

    if df_emisiones_procesado is not None and not df_emisiones_procesado.empty:
        if debug_file_info:
            print("\n--- RESULTADO DE DEPURACIÓN (DataFrame del archivo específico) ---")
            cols_debug_display = [col for col in COLUMNAS_ESTANDAR_ETL if col in df_emisiones_procesado.columns]
            if 'region_raw_val' in df_emisiones_procesado.columns: cols_debug_display.append('region_raw_val')
            if 'comuna_raw_val' in df_emisiones_procesado.columns: cols_debug_display.append('comuna_raw_val')

            print(df_emisiones_procesado[cols_debug_display].head(20))
            df_emisiones_procesado.info(verbose=True, show_counts=True)
            if 'region' in df_emisiones_procesado.columns : print(f"NaNs en region (debug): {df_emisiones_procesado['region'].isnull().sum()}")
            if 'comuna' in df_emisiones_procesado.columns : print(f"NaNs en comuna (debug): {df_emisiones_procesado['comuna'].isnull().sum()}")
            print("--- FIN DE DEPURACIÓN ---")
        else:
            try:
                df_emisiones_procesado.to_pickle(path_output_processed_file)
                print(f"\nINFO ETL: Datos de emisiones (RECT) procesados y guardados en: {path_output_processed_file}")
                print(f"INFO ETL: Dimensiones del archivo guardado: {df_emisiones_procesado.shape}")
                if not df_emisiones_procesado.empty:
                     print(f"INFO ETL: Columnas del archivo guardado: {df_emisiones_procesado.columns.tolist()}")
                     print("INFO ETL: Primeras filas del archivo guardado:")
                     print(df_emisiones_procesado.head())
                     print("\nINFO ETL: Conteo de tipos de fuente en el archivo guardado:")
                     print(df_emisiones_procesado['tipo_fuente'].value_counts(dropna=False))
                     print("\nINFO ETL: Conteo de contaminantes (top 10) en el archivo guardado:")
                     print(df_emisiones_procesado['contaminante'].value_counts(dropna=False).nlargest(40))
                     print("\nINFO ETL: Conteo de NaNs por columna en el archivo guardado:")
                     print(df_emisiones_procesado.isnull().sum())
            except Exception as e:
                print(f"ERROR CRÍTICO ETL al guardar el archivo procesado de emisiones (RECT): {type(e).__name__} - {e}")
    else:
        print("ERROR ETL: No se generaron datos de emisiones (RECT) procesados para guardar (DataFrame vacío o None).")

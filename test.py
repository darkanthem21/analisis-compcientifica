def leer_archivo_rect(nombre_archivo):
    import pandas as pd
    import os
    ruta_archivo = os.path.join('data', 'raw', 'RECT','difusas', nombre_archivo)
    try:
        if nombre_archivo.endswith('.csv'):
            df = pd.read_csv(ruta_archivo)
        elif nombre_archivo.endswith('.xlsx') or nombre_archivo.endswith('.xls'):
            df = pd.read_excel(ruta_archivo)
        elif nombre_archivo.endswith('.json'):
            df = pd.read_json(ruta_archivo)
        else:
            df = pd.read_csv(ruta_archivo)
        print(f"Archivo '{nombre_archivo}' leído correctamente.")
        print(df)
        return df

    except Exception as e:
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
        return None

if __name__ == '__main__':
    leer_archivo_rect('ruea-efd-2019-ckan.csv')

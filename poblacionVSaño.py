import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta al archivo CSV relativa al archivo .py
carpeta_actual = os.path.dirname(__file__)
ruta_csv = os.path.join(carpeta_actual, 'ine_estimaciones-y-proyecciones-2002-2035_base-2017_region_base.csv')

# Cargar el archivo CSV
df = pd.read_csv(ruta_csv)

# Mapeo de número a nombre de región
regiones = {
    1: 'Tarapacá',
    2: 'Antofagasta',
    3: 'Atacama',
    4: 'Coquimbo',
    5: 'Valparaíso',
    6: 'O’Higgins',
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
df['Region'] = df['Region'].map(regiones)
años = ['a2019', 'a2020', 'a2021', 'a2022', 'a2023']
df_años = df[['Region'] + años]

# Agrupar y sumar por región
df_agrupado = df_años.groupby('Region')[años].sum()

# Convertir a millones
df_agrupado = df_agrupado / 1_000_000

# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(14, 8))

# Dibujar el gráfico de barras
df_agrupado.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Cantidad de personas por región (2019–2023)', fontsize=16)
ax.set_xlabel('Región', fontsize=12)
ax.set_ylabel('Cantidad de personas (millones)', fontsize=12)
ax.tick_params(axis='x', rotation=45)

# Hacer que la cuadrícula esté detrás de las barras y sea punteada
ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.7)
ax.set_axisbelow(True)

# Mostrar el gráfico
plt.tight_layout()
plt.show()

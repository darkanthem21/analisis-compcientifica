import pandas as pd
import matplotlib.pyplot as plt

archivo = 'C:/Users/franh/OneDrive/Escritorio/computacion cientifica/GRAFICOS/analisis-compcientifica/AirQualitySM/Los Rios/valdivia-air-quality.csv'
df = pd.read_csv(archivo)

df.columns = df.columns.str.strip().str.lower()

for col in df.columns:
    if col != 'date':
        df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors='coerce')

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])
df = df[(df['date'].dt.year >= 2019) & (df['date'].dt.year <= 2024)]
df = df.sort_values('date')

unidades = {
    'pm25': 'AQI',
    'pm10': 'AQI',
    'o3': 'AQI',
    'no2': 'AQI',
    'so2': 'AQI',
    'co': 'AQI'  
}

contaminantes = list(unidades.keys())
contaminantes_presentes = [c for c in contaminantes if c in df.columns]

plt.figure(figsize=(12, 6))
for contaminante in contaminantes_presentes:
    etiqueta = f"{contaminante.upper()} ({unidades[contaminante]})"
    plt.plot(df['date'], df[contaminante], label=etiqueta, linestyle='-')

plt.xlabel('Fecha')
plt.ylabel('Concentración en escala AQI')
plt.title('Concentración de contaminantes en Valdivia (2019 - 2024)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

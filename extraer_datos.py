import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('doc.csv')

# Eliminar filas que no tienen un código válido
df = df.dropna(subset=['Código'])

# Filtrar filas donde la prelación no sea '---'
relaciones = df[['Código', 'Prelación']]

relaciones = relaciones.replace(r'\s*-\s*', "-", regex=True)
relaciones = relaciones.replace(r'\s*/\s*', "&", regex=True)
relaciones = relaciones.replace(r'\s*ó\s*', "|", regex=True)
relaciones = relaciones.replace(r'\s*o\s*', "|", regex=True)




relaciones.to_csv('relaciones.csv', index=False)
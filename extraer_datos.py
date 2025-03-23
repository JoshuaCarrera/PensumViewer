import camelot
import pandas as pd

tables = camelot.read_pdf('doc.pdf', pages='all')
print(f"Número de tablas detectadas: {len(tables)}")

# Crear una lista para almacenar los DataFrames de cada tabla
dataframes = []

# Iterar sobre cada tabla y agregar su DataFrame a la lista
for i, table in enumerate(tables):
    df = table.df
    if i > 0:  # Si no es la primera tabla, elimina la primera fila (encabezados)
        df = df[1:]
    dataframes.append(df)

# Concatenar todos los DataFrames en uno solo
combined_df = pd.concat(dataframes, ignore_index=True)

# Usar la primera fila como nombres de columnas
nuevos_nombres = combined_df.iloc[0]  # Obtener la primera fila
combined_df = combined_df[1:]  # Eliminar la primera fila del DataFrame
combined_df.columns = nuevos_nombres  # Asignar los nuevos nombres de columnas
combined_df = combined_df.reset_index(drop=True)

# Eliminar filas duplicadas
combined_df = combined_df.drop_duplicates(subset=['Código'])

# Guardar el DataFrame combinado en un único archivo CSV
combined_df.to_csv('doc.csv', index=False)
import camelot
import pandas as pd

# Especificar las páginas que deseas leer (por ejemplo, página 1 y 2)
tables = camelot.read_pdf('doc.pdf', pages='1,2')
print(f"Número de tablas detectadas: {len(tables)}")

# Crear una lista para almacenar los DataFrames de cada tabla
dataframes = []

# Iterar sobre cada tabla y agregar su DataFrame a la lista
for table in tables:
    dataframes.append(table.df)

# Concatenar todos los DataFrames en uno solo
combined_df = pd.concat(dataframes, ignore_index=True)

# Usar la primera fila como nombres de columnas
nuevos_nombres = combined_df.iloc[0]  # Obtener la primera fila
combined_df = combined_df[1:]  # Eliminar la primera fila del DataFrame
combined_df.columns = nuevos_nombres  # Asignar los nuevos nombres de columnas
combined_df = combined_df.reset_index(drop=True)

# Guardar el DataFrame combinado en un único archivo CSV
combined_df.to_csv('doc.csv', index=False)

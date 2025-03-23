import camelot
import pandas as pd

# Especificar las páginas que deseas leer (por ejemplo, página 1 y 2)
tables = camelot.read_pdf('doc.pdf', pages='1,2')

# Verificar cuántas tablas se detectaron
print(f"Número de tablas detectadas: {len(tables)}")

# Crear una lista para almacenar los DataFrames de cada tabla
dataframes = []

# Iterar sobre cada tabla y agregar su DataFrame a la lista
for table in tables:
    dataframes.append(table.df)

# Concatenar todos los DataFrames en uno solo
combined_df = pd.concat(dataframes, ignore_index=True)

# Guardar el DataFrame combinado en un único archivo CSV
combined_df.to_csv('combined_doc.csv', index=False)

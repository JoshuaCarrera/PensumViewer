import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# Leer el archivo CSV
df = pd.read_csv('doc.csv')

# Eliminar filas que no tienen un código válido
df = df.dropna(subset=['Código'])

# Eliminar espacios adicionales en las columnas 'Código' y 'Prelación'
df['Código'] = df['Código'].str.strip()
df['Prelación'] = df['Prelación'].str.strip()

# Filtrar filas donde la prelación no sea '---'
relaciones = df[['Código', 'Prelación']]

# Mostrar las relaciones
print("Relaciones detectadas:")
print(relaciones)

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos (unidades curriculares)
G.add_nodes_from(df['Código'])

# Agregar relaciones (prelaciones)
for _, row in relaciones.iterrows():
    G.add_edge(row['Prelación'], row['Código'])

# Dibujar el grafo
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold', arrows=True)

# Guardar la figura en un archivo
plt.title("Mapa de Requisitos")
plt.savefig("mapa_requisitos.png")  # Guardar como imagen PNG
plt.close()  # Cerrar la figura para liberar memoria

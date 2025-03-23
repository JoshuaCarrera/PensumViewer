import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network

# Leer el archivo CSV
df = pd.read_csv('doc.csv')

# Eliminar filas que no tienen un código válido
df = df.dropna(subset=['Código'])

# Filtrar filas donde la prelación no sea '---'
relaciones = df[['Unidad Curricular', 'Código', 'Prelación']]

relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*-\s*', "-", regex=True)
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*/\s*', "&", regex=True)
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*ó\s*', "|", regex=True)
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*o\s*', "|", regex=True)

relaciones.loc[:, 'Código'] = relaciones['Código'].replace(r'\s*-\s*', "-", regex=True)

codigo_a_nombre = dict(zip(relaciones['Código'], relaciones['Unidad Curricular']))

relaciones.to_csv('relaciones.csv', index=False)

# Crear una red de Pyvis
net = Network(notebook=False, height="900px", width="100%", bgcolor="#FFFFFF", font_color="black", directed=True)
net.show_buttons(filter_=['physics'])

# Paso 1: Agregar todos los nodos (códigos de cursos)
for codigo in relaciones['Código']:
    nombre_unidad = codigo_a_nombre[codigo]
    net.add_node(codigo, nombre_unidad, title=codigo)

# Paso 2: Agregar nodos de prelaciones (requisitos generales) y edges
for _, row in relaciones.iterrows():
    codigo = row['Código']
    prelacion = row['Prelación']
    
    if prelacion != '---':
        # Separar las prelaciones en grupos AND y OR
        if type(prelacion) == str:
            for grupo in prelacion.split('|'):  # Primero separar por OR
                # Determinar el tipo de relación (AND u OR)
                if '&' in grupo:
                    tipo_relacion = 'AND'
                    prereqs = grupo.split('&')
                else:
                    tipo_relacion = 'OR'
                    prereqs = [grupo]  # Si no hay &, es un solo requisito (OR)
                
                # Agregar nodos y edges según el tipo de relación
                for prereq in prereqs:
                    # Si el prereq no es un código de curso, se agrega como un nodo adicional
                    if prereq not in relaciones['Código'].values:
                        net.add_node(prereq, prereq, title=prereq, color="#FFA500")  # Color naranja para requisitos generales
                    
                    # Agregar el edge entre el prereq y el código
                    if tipo_relacion == 'AND':
                        net.add_edge(prereq, codigo, title="AND")  # Línea roja para AND
                    else:
                        net.add_edge(prereq, codigo, title="OR", dashes=True)  # Línea verde punteada para OR

# Generar el grafo
net.save_graph("index.html")

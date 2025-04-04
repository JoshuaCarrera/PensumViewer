import pandas as pd
import re
from pyvis.network import Network

# Paleta de colores para los semestres
COLORS = ["#6FE3E1","#63DEE5","#57DAE9","#4BD5EC","#3FD1F0","#32CCF4","#26C7F8","#1AC3FB","#0EBEFF"]

# Leer el archivo CSV
df = pd.read_csv('doc.csv')

# Eliminar filas que no tienen un código válido
df = df.dropna(subset=['Código'])

# Filtrar filas donde la prelación no sea '---'
relaciones = df[['Unidad Curricular', 'Código', 'Prelación', 'UC']]

# Normalizar los valores en las columnas
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*-\s*', "-", regex=True)
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*/\s*', "&", regex=True)
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*ó\s*', "|", regex=True)
relaciones.loc[:, 'Prelación'] = relaciones['Prelación'].replace(r'\s*o\s*', "|", regex=True)
relaciones.loc[:, 'Código'] = relaciones['Código'].replace(r'\s*-\s*', "-", regex=True)

# Crear un diccionario para mapear códigos a nombres de unidades curriculares
codigo_a_nombre = dict(zip(relaciones['Código'], relaciones['Unidad Curricular']))

# Guardar las relaciones en un archivo CSV
relaciones.to_csv('relaciones.csv', index=False)

# Crear una red de Pyvis
net = Network(notebook=False, height="900px", width="100%", bgcolor="#FFFFFF", font_color="black", directed=True)
#net.show_buttons(filter_=['physics'])
net.toggle_physics(True)

# Función para extraer el semestre del código
def obtener_semestre(codigo):
    match = re.search(r'-(\d)', codigo)  # Busca el primer número después del guión
    if match:
        return int(match.group(1)) - 1  # Restar 1 para usarlo como índice en COLORS
    return 0  # Si no se encuentra, usar el primer color (semestre 1)

# Paso 1: Agregar todos los nodos (códigos de la materia)
for codigo in relaciones['Código']:
    nombre_unidad = codigo_a_nombre[codigo]
    semestre = obtener_semestre(codigo)
    color = COLORS[semestre]  # Seleccionar el color según el semestre
    uc = relaciones.loc[relaciones['Código'] == codigo, 'UC'].values[0] # Obtener el valor de la columna UC en la misma fila que el "Código"
    if pd.notna(uc):  # Verificar si el valor no es NaN
        titulo = f"{codigo} UC:{int(uc)}"
    else:
        titulo = f"{codigo} UC:N/A" 
    net.add_node(codigo, nombre_unidad, title=titulo, color=color, shape="dot", level=semestre, value=semestre)

# Paso 2: Agregar nodos de prelaciones (requisitos generales) y edges
for _, row in relaciones.iterrows():
    codigo = row['Código']
    prelacion = row['Prelación']
    
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
                    net.add_node(prereq, prereq, title=prereq, color="#FFA500", shape="dot", value=2)  # Color naranja para requisitos generales
                
                # Agregar el edge entre el prereq y el código
                if tipo_relacion == 'AND':
                    net.add_edge(prereq, codigo, title="AND", dashes=True)  # Línea roja para AND
                else:
                    net.add_edge(prereq, codigo, title="OR")  # Línea verde punteada para OR

# Generar el grafo
net.save_graph("index.html")
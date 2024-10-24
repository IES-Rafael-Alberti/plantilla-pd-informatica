import re
import os

# Función para obtener el número de módulos del archivo PD.md
def get_last_mod_number(pd_filename):
    if os.path.exists(pd_filename):
        with open(pd_filename, 'r', encoding='utf-8') as pd_file:
            pd_content = pd_file.read()
            # Buscar todas las cabeceras de módulos en el formato "# MOD X"
            mod_numbers = re.findall(r'#\s*MOD\s*(\d+)', pd_content)
            # Convertir las coincidencias a números enteros y obtener el último
            if mod_numbers:
                return max(map(int, mod_numbers))
    return 0  # Si no encuentra módulos, retorna 0

# Obtener el número de módulos a partir de PD.md
pd_filename = 'src/PD.md'
num_mods = get_last_mod_number(pd_filename)

# Inicializar una lista para almacenar el contenido de los archivos modX.md
mod_contents = []

# Crear la lista de archivos modX.md según el número de módulos detectado
mod_files = [f'src/mod{i}.md' for i in range(1, num_mods + 1)]  # Se usa el número de módulos detectado

# Extraer el contenido de los archivos modX.md
for mod_filename in sorted(mod_files):
    if os.path.exists(mod_filename):
        with open(mod_filename, 'r', encoding='utf-8') as mod_file:
            mod_content = mod_file.read()
            # Eliminar la sección ## Contenidos
            mod_content = re.sub(r'##\s*Contenidos\n.*?(?=### |\Z)', '', mod_content, flags=re.DOTALL)
            # Eliminar la sección ### Contenidos del currículo hasta ### Selección y secuencia de contenidos
            mod_content = re.sub(r'###\s*Contenidos del currículo.*?(?=### Selección y secuencia de contenidos|\Z)', '', mod_content, flags=re.DOTALL)
            # Convertir ### Selección y secuencia de contenidos a ## Selección y secuencia de contenidos
            mod_content = re.sub(r'###\s*Selección y secuencia de contenidos', '## Selección y secuencia de contenidos', mod_content)
            # Eliminar secciones ### Tratamiento de temas transversales y ### Interdisciplinaridad
            mod_content = re.sub(r'###\s*Tratamiento de temas transversales.*?(?=### |\Z)', '', mod_content, flags=re.DOTALL)
            mod_content = re.sub(r'###\s*Interdisciplinaridad.*?(?=## |\Z)', '', mod_content, flags=re.DOTALL)
            # Eliminar ## Bibliografía y referencias y subsecciones
            mod_content = re.sub(r'##\s*Bibliografía y referencias.*', '', mod_content, flags=re.DOTALL)
            
            # Añadir el contenido procesado a la lista
            mod_contents.append(mod_content)

# Extraer la sección "# Registro de versiones" del archivo src/PD.md
if os.path.exists(pd_filename):
    with open(pd_filename, 'r', encoding='utf-8') as pd_file:
        pd_content = pd_file.read()
        # Extraer la sección "# Registro de versiones"
        versions_table = re.search(r'#\s*Registro de versiones.*', pd_content, flags=re.DOTALL)
        versions_table = versions_table.group(0) if versions_table else ''

# Concatenar el contenido de los módulos al inicio del contenido actual
final_content = '\n'.join(mod_contents) + '\n' + versions_table

# Guardar el nuevo contenido en un nuevo archivo o sobrescribir el existente
with open('mkdocs-resumen/docs/resumen.md', 'w', encoding='utf-8') as file:
    file.write(final_content)

print(f"Extracción completada. El archivo resultante es resumen.md y se procesaron {num_mods} módulos.")

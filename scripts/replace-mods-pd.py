import re
import os

# Nombre del archivo principal
main_file = 'src/PD.md'

# Leer el contenido del archivo principal
with open(main_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Buscar todas las ocurrencias de # MOD X
mod_matches = re.findall(r'# MOD (\d+)', content)

for mod_number in mod_matches:
    mod_filename = f'src/mod{mod_number}.md'
    
    # Verificar si el archivo modX.md existe
    if os.path.exists(mod_filename):
        with open(mod_filename, 'r', encoding='utf-8') as mod_file:
            mod_content = mod_file.read()
        
        # Eliminar secciones que empiezan con ## Objetivos del módulo hasta la siguiente cabecera de nivel 1
        pattern = r'##\s*Objetivos del módulo.*?(?=\n## |\Z)'
        mod_content = re.sub(pattern, '', mod_content, flags=re.DOTALL)
        
        # Reemplazar # MOD X por el contenido del archivo correspondiente
        content = content.replace(f'# MOD {mod_number}', mod_content)
    else:
        print(f"Archivo {mod_filename} no encontrado. Se omite la sustitución para # MOD {mod_number}.")

# Guardar el nuevo contenido en un nuevo archivo o sobrescribir el existente
with open('mkdocs-pd/docs/PD.md', 'w', encoding='utf-8') as file:
    file.write(content)

print("Sustitución completada. El archivo resultante es PD.md.")
import yaml
import re
import os
import shutil
from pathlib import Path

# Definir rutas
templates_dir = Path('templates')
mkdocs_pd_dir = Path('mkdocs-pd/docs')
mkdocs_resumen_dir = Path('mkdocs-resumen/docs')

# Función para copiar carpetas y archivos
def copy_assets(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)  # Eliminar la carpeta si ya existe
    shutil.copytree(src, dst)

# Función para copiar y modificar el archivo cover.html
def copy_and_edit_cover(src_file, dst_dir, css_files):
    # Copiar cover.html
    dst_file = dst_dir / 'templates' / 'cover.html'
    os.makedirs(dst_file.parent, exist_ok=True)
    shutil.copy(src_file, dst_file)
    
    # Leer contenido de los archivos CSS
    css_content = ""
    for css_file in css_files:
        with open(css_file, 'r') as f:
            css_content += f.read()
    
    # Añadir el contenido CSS dentro de la etiqueta <style> al final del archivo cover.html
    with open(dst_file, 'a') as f:
        f.write(f"\n<style>\n{css_content}\n</style>\n")

# Leer el archivo datos.yml
def leer_datos_yml(ruta):
    with open(ruta, 'r', encoding='utf-8') as file:
        datos = yaml.safe_load(file)
    return datos

# Obtener la última versión de la tabla del archivo PD.md
def obtener_version_desde_pd(ruta_pd):
    with open(ruta_pd, 'r', encoding='utf-8') as pd_file:
        pd_content = pd_file.read()
        # Capturar todo el contenido desde '# Registro de versiones' hasta el final del documento
        registro_versiones = re.search(r'#\s*Registro de versiones[\s\S]*', pd_content, flags=re.DOTALL)
        if registro_versiones:
            # Extraer todas las filas de la tabla
            tabla = registro_versiones.group(0)
            # Dividir la tabla en filas
            filas = tabla.splitlines()
            # Tomar la última fila con contenido (la última fila completa)
            for fila in reversed(filas):
                if fila.startswith('|'):
                    # Extraer el valor antes del último '|'
                    columnas = fila.split('|')
                    # El penúltimo elemento contiene la versión
                    return columnas[-2].strip()
    return None

# Generar la cadena formateada
def generar_cadena(datos, version):
    año = datos['inicio_curso']
    acronimo = datos['acronimo_curso']
    curso = datos['curso']
    
    if datos['tiene_mas_de_un_curso'] == 1:
        return f"{año}_{acronimo}_{curso}_vrs_{version}"
    else:
        return f"{año}_{acronimo}_vrs_{version}"

# Modificar el archivo .yml para cambiar el output_path
def modificar_mkdocs(ruta_archivo, nueva_cadena, datos, es_resumen=False):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        lineas = file.readlines()
    
    # Construir la nueva ruta del PDF
    nueva_ruta = f"../../{'resumen_' if es_resumen else ''}{nueva_cadena}.pdf"
    
    # Buscar y reemplazar la línea de output_path
    with open(ruta_archivo, 'w', encoding='utf-8') as file:
        for linea in lineas:
            if "cover_subtitle"  in linea:
                if es_resumen:
                    file.write(f"      cover_subtitle: {datos['titulo']}\n")
                else:
                    file.write(f"      cover_subtitle: {datos['titulo']}\n")
            elif "output_path:" in linea:
                file.write(f"      output_path: {nueva_ruta}\n")
            elif "course_year:" in linea:
                file.write(f"  course_year: \"Curso {datos['inicio_curso']} / {datos['inicio_curso']+1}\"\n")
            else:
                file.write(linea)

if __name__ == "__main__":
    # Ruta al archivo datos.yml y src/PD.md
    ruta_datos = 'src/datos.yml'
    ruta_pd = 'src/PD.md'
    
    # Leer datos del archivo YML
    datos = leer_datos_yml(ruta_datos)
    
    # Verificar si 'version_documento' está en datos
    version = datos.get('version_documento')
    
    # Si no existe, buscar la versión en el archivo PD.md
    if version is None:
        version = obtener_version_desde_pd(ruta_pd)
    
    # Generar cadena formateada
    cadena_formateada = generar_cadena(datos, version)
    
    # Modificar mkdocs-pd/mkdocs.yml
    modificar_mkdocs('mkdocs-pd/mkdocs.yml', cadena_formateada, datos)
    
    # Modificar mkdocs-resumen/mkdocs.yml
    modificar_mkdocs('mkdocs-resumen/mkdocs.yml', cadena_formateada, datos, es_resumen=True)


    # Copiar carpeta templates/assets a mkdocs-pd/docs/templates y mkdocs-resumen/docs/templates
    copy_assets(templates_dir / 'assets', mkdocs_pd_dir / 'templates' / 'assets')
    copy_assets(templates_dir / 'assets', mkdocs_resumen_dir / 'templates' / 'assets')

    # Copiar y modificar cover.html para mkdocs-pd
    copy_and_edit_cover(
        templates_dir / 'cover.html',
        mkdocs_pd_dir,
        [templates_dir / 'general.css', templates_dir / 'pd.css']
    )

    # Copiar y modificar cover.html para mkdocs-resumen
    copy_and_edit_cover(
        templates_dir / 'cover.html',
        mkdocs_resumen_dir,
        [templates_dir / 'general.css', templates_dir / 'resumen.css']
    )

    print(f"Archivos modificados correctamente con la cadena: {cadena_formateada}")

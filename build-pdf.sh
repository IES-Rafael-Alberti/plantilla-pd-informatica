#!/bin/bash

# Eliminamos las programaciones antiguas y sus templates

rm *.pdf

# Eliminar mkdocs-pd/templates si existe
if [ -d "mkdocs-pd/templates" ]; then
  rm -r mkdocs-pd/templates
fi

# Eliminar mkdocs-resumen/templates si existe
if [ -d "mkdocs-resumen/templates" ]; then
  rm -r mkdocs-resumen/templates
fi

# Generamos la configuración de los archivos a partir de src/datos.yml y el template
python scripts/generate-config.py

# Construir la programación y generar el PDF

# Reemplazar los archivos modX.md en PD.md
python scripts/replace-mods-pd.py
cd mkdocs-pd
mkdocs build

# Borrar la carpeta 'site' completa
rm -rf site

cd ..

# Construir el resumen y generar el PDF

# Extraer la información de los archivos modX.md en resumen.md
python scripts/extract-mods-resumen.py

cd mkdocs-resumen
mkdocs build

# Borrar la carpeta 'site' completa
rm -rf site
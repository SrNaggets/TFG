import os
from docx import Document

# Ruta donde están tus archivos .docx
carpeta_docx = 'Informacion/documentos/Bodegas'  # cámbialo por la ruta real
# Ruta donde se guardarán los .txt
carpeta_txt = 'Informacion/documentos/Bodegas txt'    # cámbialo por la ruta real

# Crear carpeta de salida si no existe
os.makedirs(carpeta_txt, exist_ok=True)

# Función para extraer texto de un .docx
def extraer_texto_docx(ruta_archivo):
    doc = Document(ruta_archivo)
    texto = '\n'.join([p.text for p in doc.paragraphs])
    return texto.strip()

# Procesar cada archivo .docx en la carpeta
for archivo in os.listdir(carpeta_docx):
    if archivo.endswith('.docx'):
        ruta_docx = os.path.join(carpeta_docx, archivo)
        texto = extraer_texto_docx(ruta_docx)

        nombre_txt = os.path.splitext(archivo)[0] + '.txt'
        ruta_txt = os.path.join(carpeta_txt, nombre_txt)

        with open(ruta_txt, 'w', encoding='utf-8') as f:
            f.write(texto)

        print(f"✔ Guardado: {nombre_txt}")

print("✅ Conversión completada.")

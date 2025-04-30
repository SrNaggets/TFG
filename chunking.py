import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuración del splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)

# Función para cargar todos los archivos .txt de una carpeta
def cargar_archivos_txt(ruta):
    documentos = []
    for nombre_archivo in os.listdir(ruta):
        if nombre_archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta, nombre_archivo)
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                documentos.append((nombre_archivo, contenido))
    return documentos

# Función para aplicar chunking con LangChain
def chunkear_documentos(documentos):
    chunks = []
    for nombre_archivo, contenido in documentos:
        partes = text_splitter.split_text(contenido)
        for i, parte in enumerate(partes):
            chunks.append({
                "texto": parte,
                "origen": nombre_archivo,
                "indice": i
            })
    return chunks

# Cambia esta ruta por la carpeta donde están tus archivos .txt
RUTA_TXT = "Informacion/documentos/Bodegas txt"

documentos = cargar_archivos_txt(RUTA_TXT)
chunks_generados = chunkear_documentos(documentos)

# Verificamos resultado
print(f"Total de chunks generados: {len(chunks_generados)}")
print("Ejemplo:")
print(chunks_generados[0])

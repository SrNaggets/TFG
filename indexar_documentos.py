import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from docx import Document

# Configurar la base de datos de ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="vinos_jerez")

# Función para extraer texto de archivos PDF
def extraer_texto_pdf(ruta):
    texto = ""
    with open(ruta, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            texto += page.extract_text() + "\n"
    return texto

# Función para extraer texto de archivos DOCX
def extraer_texto_docx(ruta):
    doc = Document(ruta)
    return "\n".join([p.text for p in doc.paragraphs])

# Función para procesar archivos en una carpeta
def procesar_documentos(directorio):
    for archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, archivo)
        if archivo.endswith(".pdf"):
            texto = extraer_texto_pdf(ruta_completa)
        elif archivo.endswith(".docx"):
            texto = extraer_texto_docx(ruta_completa)
        else:
            continue  # Ignorar archivos no soportados
        
        # Dividir el texto en fragmentos más pequeños
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        fragmentos = splitter.split_text(texto)
        
        # Almacenar en ChromaDB
        for i, fragmento in enumerate(fragmentos):
            collection.add(
                ids=[f"{archivo}-{i}"],
                documents=[fragmento],
                metadatas=[{"fuente": archivo}]
            )

# Ruta de la carpeta donde están los documentos
directorio_documentos = "./Fuentes_Informacion"
procesar_documentos(directorio_documentos)

print("✅ Documentos indexados en ChromaDB con éxito.")

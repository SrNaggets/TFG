import json
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Cargar los chunks desde el archivo JSON
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"✅ Cargados {len(chunks)} chunks desde 'chunks.json'")

# 2. Cargar el modelo de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Modelo de embeddings cargado")

# 3. Crear cliente persistente de ChromaDB (nuevo método)
chroma_client = chromadb.PersistentClient(path="chroma_db")

# 4. Crear o acceder a una colección en Chroma
coleccion = chroma_client.get_or_create_collection(name="vinos_jerez")

# 5. Preparar datos
documentos = [chunk["texto"] for chunk in chunks]
ids = [f"{chunk['origen']}_{chunk['indice']}" for chunk in chunks]
metadatos = [{"origen": chunk["origen"]} for chunk in chunks]

# 6. Generar los embeddings
print("⚙️ Generando embeddings...")
vectores = modelo.encode(documentos, show_progress_bar=True).tolist()

# 7. Guardar en la base ChromaDB
print("💾 Guardando en ChromaDB...")
coleccion.add(
    documents=documentos,
    ids=ids,
    embeddings=vectores,
    metadatas=metadatos
)

print(f"✅ {len(documentos)} chunks indexados correctamente en la colección 'vinos_jerez'")


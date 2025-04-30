import chromadb
from sentence_transformers import SentenceTransformer
import requests

# CONFIGURACIÓN
NUM_CHUNKS = 3
NOMBRE_MODELO = "deepseek-coder:6.7b"
BASE_VECTORIAL = "chroma_db"
COLECCION = "vinos_jerez"

# PREGUNTA DEL USUARIO
pregunta = input("❓ Escribe tu pregunta: ")

# 1. Cargar modelo de embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Embedding de la pregunta
embedding_pregunta = modelo.encode(pregunta).tolist()

# 3. Conexión a ChromaDB
chroma_client = chromadb.PersistentClient(path=BASE_VECTORIAL)
coleccion = chroma_client.get_or_create_collection(name=COLECCION)

# 4. Recuperar los chunks más relevantes
resultados = coleccion.query(
    query_embeddings=[embedding_pregunta],
    n_results=NUM_CHUNKS,
    include=["documents", "metadatas", "distances"]
)

chunks = resultados["documents"][0]
fuentes = resultados["metadatas"][0]

# 5. Crear el contexto para la IA
contexto = "\n\n".join(chunks)
prompt = f"""Contesta a la siguiente pregunta usando solo la información del contexto:

### Contexto:
{contexto}

### Pregunta:
{pregunta}

### Respuesta:"""

# 6. Enviar a DeepSeek vía Ollama
respuesta = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": NOMBRE_MODELO,
        "prompt": prompt,
        "stream": False
    }
)

# 7. Mostrar respuesta
respuesta_json = respuesta.json()
print("\n🤖 Respuesta de DeepSeek:\n")
print(respuesta_json["response"])

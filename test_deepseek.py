import requests
import os

# Obtener la API Key desde las variables de entorno
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

# Verificar si la API Key está configurada
if not API_KEY:
    print("❌ ERROR: No se encontró la API Key. Asegúrate de configurarla correctamente.")
    exit()

# Configurar la solicitud a la API de Deepseek
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "Eres un experto en vinos del Marco de Jerez."},
        {"role": "user", "content": "¿Cuáles son los tipos de vinos de Jerez?"}
    ]
}

# Enviar la solicitud a la API
response = requests.post(API_URL, json=data, headers=headers)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    respuesta = response.json()
    print("✅ Conexión exitosa con Deepseek. Respuesta:")
    print(respuesta["choices"][0]["message"]["content"])
else:
    print(f"❌ ERROR: No se pudo conectar con Deepseek. Código {response.status_code}")
    print(response.text)

from fastapi import FastAPI
import requests
import os
import time
import json

app = FastAPI()

# URL do JSON fornecida
JSON_URL = "https://www.dropbox.com/scl/fi/v2fuahx8uxcar2edrkk8m/Filmes_Series.json?rlkey=mjw8j0iw5047eofkcm2wkqwbo&st=6zjei3ga&dl=1"
CACHE_FILE = "/tmp/cache.json"  # Armazena o cache no diretório temporário
CACHE_DURATION = 24 * 60 * 60   # Expira após 24 horas (em segundos)


def is_cache_valid():
    """Verifica se o cache é válido, comparando o tempo de modificação com a duração do cache."""
    if not os.path.exists(CACHE_FILE):
        return False
    file_time = os.path.getmtime(CACHE_FILE)
    return time.time() - file_time < CACHE_DURATION


@app.get("/json")
async def get_json():
    """Rota que retorna o JSON do cache ou baixa novamente se o cache expirou."""
    if is_cache_valid():
        with open(CACHE_FILE, "r") as file:
            data = json.load(file)
    else:
        response = requests.get(JSON_URL)
        data = response.json()
        with open(CACHE_FILE, "w") as file:
            json.dump(data, file)
    return data

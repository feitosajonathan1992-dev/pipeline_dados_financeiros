import os

# Caminho base do projeto (onde está a pasta data, src, etc.)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pasta principal de dados
DATA_DIR = os.path.join(BASE_DIR, "data")

# Caminhos das Camadas (Usamos as chaves {region} para preencher depois com 'br' ou 'us')
BRONZE_PATH = os.path.join(DATA_DIR, "{region}", "bronze")
SILVER_PATH = os.path.join(DATA_DIR, "{region}", "silver")
GOLD_PATH = os.path.join(DATA_DIR, "{region}", "gold")
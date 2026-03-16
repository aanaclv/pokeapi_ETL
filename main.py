# ==========================================
# 1. IMPORTS
# ==========================================

import requests
import csv
import os #para criar o caminho data/pokemons.csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==========================================
# 1. CONFIGURAÇÕES
# ==========================================

url_base = "https://pokeapi.co/api/v2/pokemon"
pasta_data = "data"
final_file = os.path.join(pasta_data, "pokemons.csv")
timeout_sec = 10

# ==========================================
# 2. MOTOR DE REDE (RESILIÊNCIA)
# ==========================================

def get_session():
    session = requests.Session()
    retry_strategy = Retry(
        total = 3,
        backoff_factor = 1, #atraso exponencial, aguarda 1s, 2s..
        status_forcelist = [429, 500, 503, 504] #"só tente de novo se o erro for um desses"
    )

    #sempre que um site começar com "https:// use as regras de insistência que criei"
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session

# ==========================================
# 3. FUNÇÃO DE EXTRAÇÃO
# ==========================================

def data_extract_api(endpoint, session):
    url_complete = f"{url_base}/{endpoint}"

    try:
        r = session.get(url_complete, timeout = timeout_sec)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        print(f"❌ Erro de HTTP no ID {endpoint}: {err}")
    except Exception as e:
        print(f"❌ Erro inesperado no ID {endpoint}: {e}")
    
    return None

# ==========================================
# 4. EXECUÇÃO PRINCIPAL
# ==========================================

if __name__ == "__main__":

    #Garante que a pasta 'data' exista
    os.makedirs(pasta_data, exist_ok=True)

    # Inicia o motor de rede
    my_session = get_session()

    #Armazena num dicionário
    pokemons_raw = []

    print("🚀 Iniciando a extração de dados...")

    #Extração dos 10 primeiros pokemóns
    for i in range(1,11):
        data = data_extract_api(str(i), my_session)

        if data:
            pokemons_raw.append(data)
            print(f"✅ Extraído: {data['name']}")

    print(f"\nTotal de registros na memória: {len(pokemons_raw)}")
    print("Pronto para a próxima etapa: Transformação (T)")
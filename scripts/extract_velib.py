import requests
import pandas as pd
from sqlalchemy import create_engine
import os

# --- CONFIGURATION (Récupérées depuis les variables d'environnement Docker) ---
API_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=100"
DB_USER = os.getenv("DW_POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("DW_POSTGRES_PASSWORD", "admin")
DB_HOST = os.getenv("DW_POSTGRES_HOST", "postgres_dw")
DB_PORT = "5432"
DB_NAME = os.getenv("DW_POSTGRES_DB", "urban_data")

# Chaîne de connexion - Utilisation du nom de service Docker
CONNECTION_STR = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def extract_data():
    """
    1. Récupération des données depuis l'API Vélib.
    """
    print(f" Récupération des données depuis {API_URL}...")
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data_json = response.json()
        results = data_json.get('results', [])
        print(f" {len(results)} stations récupérées.")
        return results
    else:
        raise Exception(f" Erreur API : {response.status_code}")

def transform_data(results):
    """
    2. Transformation légère (Mise à plat et renommage des colonnes).
    """
    df = pd.DataFrame(results)
    
    final_df = df[[
        'stationcode', 
        'name', 
        'nom_arrondissement_communes', 
        'capacity', 
        'numdocksavailable', 
        'numbikesavailable', 
        'duedate' 
    ]].copy()

    final_df.columns = [
        'station_code', 
        'station_name', 
        'location', 
        'capacity', 
        'docks_available', 
        'bikes_available', 
        'last_updated'
    ]
    
    # Best Practice : Ajouter une colonne pour le moment de l'ingestion
    final_df['ingestion_date'] = pd.Timestamp.now()
    
    return final_df

def load_data(df):
    """
    3. Chargement de la donnée brute dans la table PostgreSQL.
    """
    engine = create_engine(CONNECTION_STR)
    
    # On utilise 'if_exists='append'' pour ajouter une nouvelle ligne à chaque fois que le DAG s'exécute.
    df.to_sql('raw_velib_data', engine, if_exists='append', index=False)
    print(" Données insérées avec succès dans la table raw_velib_data.")

def run_velib_etl():
    """ Fonction principale pour être appelée par Airflow. """
    try:
        raw_data = extract_data()
        clean_df = transform_data(raw_data)
        load_data(clean_df)
        print(" ETL Vélib terminé avec succès.")
    except Exception as e:
        print(f" Échec de l'ETL Vélib : {e}")
        raise

if __name__ == "__main__":
    run_velib_etl()
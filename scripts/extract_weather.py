import requests
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime

# --- CONFIGURATION API MÉTÉO ---
# Remplacez ceci par une vraie clé API si vous en avez une, sinon une valeur générique
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "YOUR_DUMMY_API_KEY") 
CITY = "Paris,FR"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"

# --- CONFIGURATION DB (Identique à Vélib) ---
DB_USER = os.getenv("DW_POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("DW_POSTGRES_PASSWORD", "admin")
DB_HOST = os.getenv("DW_POSTGRES_HOST", "postgres_dw")
DB_PORT = "5432"
DB_NAME = os.getenv("DW_POSTGRES_DB", "urban_data")

CONNECTION_STR = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def extract_weather_data():
    """
    1. Récupération des données depuis l'API OpenWeatherMap.
    """
    print(f"🔍 Récupération des données météo pour {CITY}...")
    try:
        response = requests.get(API_URL)
        response.raise_for_status() # Lève une exception si le statut n'est pas 200
        data_json = response.json()
        print(" Données météo récupérées.")
        return data_json
    except requests.exceptions.HTTPError as e:
        print(f" Erreur API Météo : Vérifiez la clé API. {e}")
        # Si la clé est factice, on lève l'exception pour faire échouer le DAG.
        raise Exception(f"Erreur HTTP lors de l'appel API Météo: {e}")
    except Exception as e:
        print(f" Erreur lors de l'extraction météo : {e}")
        raise

def transform_weather_data(data):
    """
    2. Transformation légère des données météo.
    """
    # Extraction des champs clés
    weather_data = {
        'city': data.get('name'),
        'temp_celsius': data['main']['temp'],
        'feels_like_celsius': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'weather_main': data['weather'][0]['main'],
        'weather_description': data['weather'][0]['description'],
        'wind_speed': data['wind']['speed'],
        'cloudiness': data.get('clouds', {}).get('all', 0),
        'ingestion_date': datetime.now()
    }
    df = pd.DataFrame([weather_data])
    return df

def load_weather_data(df):
    """
    3. Chargement de la donnée brute dans la table PostgreSQL.
    """
    engine = create_engine(CONNECTION_STR)
    # Nouvelle table : raw_weather_data
    df.to_sql('raw_weather_data', engine, if_exists='append', index=False)
    print(" Données météo insérées dans la table raw_weather_data.")

def run_weather_etl():
    """ Fonction principale pour être appelée par Airflow. """
    try:
        raw_data = extract_weather_data()
        clean_df = transform_weather_data(raw_data)
        load_weather_data(clean_df)
        print("🎉 ETL Météo terminé avec succès.")
    except Exception as e:
        print(f" Échec de l'ETL Météo : {e}")
        raise

if __name__ == "__main__":
    run_weather_etl()
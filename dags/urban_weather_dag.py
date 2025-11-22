from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator 
from datetime import datetime, timedelta
import sys
import os

# Import des fonctions Python

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../scripts"))
from extract_velib import run_velib_etl # Assurez-vous que cette ligne est bien présente
from extract_weather import run_weather_etl  


# Définition des arguments par défaut... (inchangé)
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1), 
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG
with DAG(
    'urban_mobility_etl', 
    default_args=default_args,
    description='Pipeline ELT pour les données urbaines',
    schedule_interval=timedelta(hours=1), 
    catchup=False,
    tags=['urban', 'velib', 'raw_ingestion', 'dbt'],
) as dag:

    # Tâche 1 : Ingestion Vélib (E/L)
    t1_velib_ingest = PythonOperator(
        task_id='ingest_velib_data',
        python_callable=run_velib_etl
    )

    # NOUVELLE TÂCHE MÉTÉO
    t1_weather_ingest = PythonOperator(
        task_id='ingest_weather_data',
        python_callable=run_weather_etl
    )

    # : Tâche 2 : Transformation dbt (T)
    t2_dbt_run = BashOperator(
        task_id='transform_velib_data_dbt',
        bash_command='dbt run --project-dir /opt/airflow/dbt_project/velib_analytics',
    )
    
    #: Définition de l'ordre d'exécution
    t1_velib_ingest >> t2_dbt_run 
    # Ceci crée la dépendance : Tâche 2 ne s'exécute QUE si Tâche 1 a réussi.
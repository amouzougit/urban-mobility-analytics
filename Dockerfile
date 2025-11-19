# On part de l'image officielle Airflow
FROM apache/airflow:2.8.1

# On passe en utilisateur root pour installer des dépendances système si besoin (optionnel ici)
USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# On repasse en utilisateur airflow pour installer les librairies Python
USER airflow

# On copie le fichier requirements.txt dans le conteneur
COPY requirements.txt /requirements.txt

# On installe les librairies
RUN pip install --no-cache-dir -r /requirements.txt
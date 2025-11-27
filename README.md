# 🚲 Urban Mobility ETL : Vélib' & Météo Analytics

##  À propos du projet
Ce projet est un pipeline de données **ELT (Extract, Load, Transform)** complet, conçu pour analyser la corrélation entre la disponibilité des vélos (Vélib' Métropole) et les conditions météorologiques à Paris en temps réel.

L'objectif est de fournir une infrastructure de données robuste capable d'aider à la prise de décision pour la redistribution des flottes de vélos.

##  Architecture Technique

Le projet repose sur une stack Data Engineering moderne et conteneurisée :

* **Orchestration :** Apache Airflow (gestion des DAGs et planification).
* **Ingestion (Extract & Load) :** Scripts Python (Requests/Pandas) connectés aux APIs Open Data (Vélib' Métropole & OpenWeatherMap).
* **Data Warehouse :** PostgreSQL (stockage des données brutes et transformées).
* **Transformation :** dbt (Data Build Tool) pour le nettoyage, les tests et la création de Data Marts.
* **Infrastructure :** Docker & Docker Compose pour un déploiement isolé et reproductible.
* **Sécurité :** Gestion des clés API via variables d'environnement (pas de secrets dans le code).

##  Fonctionnalités Clés

1.  **Ingestion Automatisée :** Récupération horaire des données de disponibilité des stations et de la météo locale.
2.  **Gestion des Erreurs :** Mécanismes de "Retry" dans Airflow et validation des schémas.
3.  **Modélisation Dimensionnelle :**
    * `raw_velib` & `raw_weather` : Données brutes.
    * `mart_urban_weather_context` : Table finale jointe et agrégée prête pour l'analyse BI.
4.  **Qualité des Données :** Tests dbt intégrés (unicité, non-nullité).

##  Aperçu des Données (Exemple)

Le pipeline génère une table analytique permettant de répondre à des questions telles que : *"Quel est l'impact de la pluie sur le taux de disponibilité dans le 11ème arrondissement ?"*

| hour_key            | total_bikes_available | avg_temp | weather_desc    |
|---------------------|-----------------------|----------|-----------------|
| 2025-11-22 14:00:00 | 1668                  | 8.7°C    | mist            |
| 2025-11-22 15:00:00 | 1129                  | 8.5°C    | broken clouds   |

## 🛠 Comment lancer le projet

Pré-requis : Docker et Docker Compose installés.

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/amouzougit/urban-mobility-analytics.git
    cd urban-mobility-analytics
    ```

2.  **Configurer les variables d'environnement :**
    Créer un fichier `.env` et ajouter votre clé OpenWeatherMap :
    ```bash
    WEATHER_API_KEY=votre_cle_api_ici
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=admin
    POSTGRES_DB=urban_data
    ```

3.  **Lancer les conteneurs :**
    ```bash
    docker compose up -d --build
    ```

4.  **Accéder à Airflow :**
    Rendez-vous sur `http://localhost:8080` et lancez le DAG `urban_mobility_etl`.

## 👤 Auteur
Projet réalisé par **KEVO** dans le cadre d'un portfolio Data Engineering.

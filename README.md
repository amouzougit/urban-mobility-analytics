#  Urban Mobility ETL : Vélib' & Météo Analytics

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
![Status](https://img.shields.io/badge/Status-Alpha-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

##  À propos du projet

Ce projet est un pipeline de données **ELT (Extract, Load, Transform)** complet, conçu pour analyser la corrélation entre la disponibilité des vélos (Vélib' Métropole) et les conditions météorologiques à Paris.

L'objectif est de fournir une infrastructure de données robuste capable d'aider à la prise de décision pour la redistribution des flottes de vélos en fonction des conditions météorologiques et des patterns de mobilité urbaine.

##  Architecture Technique

Le projet repose sur une stack Data Engineering moderne et conteneurisée :

* **Orchestration :** Apache Airflow (gestion des DAGs et planification)
* **Ingestion (Extract & Load) :** Scripts Python (Requests/Pandas) connectés aux APIs Open Data
  - [Vélib' Métropole API](https://www.velib-metropole.fr/)
  - [OpenWeatherMap API](https://openweathermap.org/api)
* **Data Warehouse :** PostgreSQL (stockage des données brutes et transformées)
* **Transformation :** dbt (Data Build Tool) pour le nettoyage, les tests et la création de Data Marts
* **Infrastructure :** Docker & Docker Compose pour un déploiement isolé et reproductible
* **Sécurité :** Gestion des clés API via variables d'environnement (pas de secrets dans le code)

##  Structure du Projet

```
urban-mobility-analytics/
├── dags/                          # Pipelines Airflow
│   └── urban_mobility_etl.py     # DAG principal d'orchestration
├── dbt_project/                  # Modèles dbt
│   └── velib_analytics/
│       ├── models/               # Modèles SQL dbt
│       ├── tests/                # Tests de qualité des données
│       └── dbt_project.yml
├── scripts/                      # Utilitaires Python
│   ├── extract_velib.py         # Extraction données Vélib'
│   ├── extract_weather.py       # Extraction données météo
│   └── requirements.txt
├── docker-compose.yml           # Configuration des services
├── Dockerfile                   # Image personnalisée Airflow
├── .env.example                 # Template des variables d'environnement
└── README.md
```

##  Prérequis

| Outil | Version | Lien |
|-------|---------|------|
| Docker | 20.10+ | [Installation](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.0+ | [Installation](https://docs.docker.com/compose/install/) |
| Python (optionnel) | 3.9+ | [Installation](https://www.python.org/downloads/) |

**Clés API requises :**
- OpenWeatherMap API Key (gratuit) : https://openweathermap.org/api

##  Fonctionnalités Clés

1. **Ingestion Automatisée** 
   - Récupération horaire des données de disponibilité des stations Vélib'
   - Récupération des conditions météorologiques locales
   
2. **Gestion des Erreurs** 
   - Mécanismes de "Retry" dans Airflow avec backoff exponentiel
   - Validation des schémas et des données
   
3. **Modélisation Dimensionnelle**
   - `raw_velib` & `raw_weather` : Données brutes
   - `mart_urban_weather_context` : Table finale jointe et agrégée prête pour l'analyse BI
   
4. **Qualité des Données**
   - Tests dbt intégrés (unicité, non-nullité)
   - Monitoring des anomalies

##  Aperçu des Données (Exemple)

Le pipeline génère une table analytique permettant de répondre à des questions telles que :
> *"Quel est l'impact de la pluie sur le taux de disponibilité dans le 11ème arrondissement ?"*

| hour_key            | total_bikes_available | avg_temp | weather_desc    |
|---------------------|-----------------------|----------|-----------------|
| 2025-11-22 14:00:00 | 1668                  | 8.7°C    | mist            |
| 2025-11-22 15:00:00 | 1129                  | 8.5°C    | broken clouds   |

##  Comment lancer le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/amouzougit/urban-mobility-analytics.git
cd urban-mobility-analytics
```

### 2. Configurer les variables d'environnement

Copier le fichier template et complétez vos clés :

```bash
cp .env.example .env
```

Éditer `.env` avec vos paramètres :

```bash
# OpenWeatherMap
WEATHER_API_KEY=votre_cle_api_ici

# PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin_secure_password
POSTGRES_DB=urban_data

# Airflow
AIRFLOW_UID=50000
```

### 3. Lancer les conteneurs

```bash
docker compose up -d --build
```

### 4. Accéder à Airflow

Rendez-vous sur : **http://localhost:8080**
- Identifiants par défaut : `airflow` / `airflow`
- Lancez le DAG `urban_mobility_etl` manuellement ou attendez le premier trigger planifié

### 5. Vérifier PostgreSQL

```bash
docker compose exec postgres psql -U admin -d urban_data
```

## 🔍 Troubleshooting

### Les conteneurs ne démarrent pas
```bash
# Vérifier les logs
docker compose logs -f

# Reconstruire les images
docker compose down
docker compose up -d --build
```

### Erreur de connexion à l'API OpenWeatherMap
- Vérifiez que votre `WEATHER_API_KEY` est correcte dans `.env`
- Attendez quelques minutes (délai de propagation de la clé)
- Testez la clé : `curl "https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=YOUR_KEY"`

### PostgreSQL refuse la connexion
```bash
# Vérifier les variables d'environnement
docker compose exec postgres env | grep POSTGRES

# Redémarrer le service
docker compose restart postgres
```

##  Performance et Résultats

| Métrique | Valeur |
|----------|--------|
| Fréquence d'ingestion | Horaire |
| Stations Vélib' suivi | ~1,400 |
| Volume mensuel | ~600k lignes |
| Temps de transformation | < 5 min |
| Stockage mensuel | ~200 MB |

##  Ressources Utiles

- [Documentation Airflow](https://airflow.apache.org/docs/)
- [Documentation dbt](https://docs.getdbt.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Vélib' API Documentation](https://opendata.paris.fr/explore/dataset/velib-metropole-stations)

##  Contribution

Les contributions sont bienvenues ! Pour proposer des améliorations :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout de fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

##  Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

##  Auteur

Projet réalisé par **KEVO** dans le cadre d'un portfolio Data Engineering.

---

**⭐ Si ce projet vous a été utile, n'hésitez pas à laisser une star !**

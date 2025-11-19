# 🚴‍♀️ Urban Mobility Analytics Pipeline

Ce projet met en œuvre un pipeline Data Engineering de bout en bout (ELT) pour ingérer, transformer et analyser les données de disponibilité des vélos en libre-service (Vélib') et les conditions météorologiques associées.

## Objectifs Clés

* **Ingestion :** Collecter en temps réel les données de l'API Vélib' et de l'API Météo.
* **Transformation :** Créer des modèles de données analytiques pour la consommation (Data Marts).
* **Orchestration :** Garantir l'exécution fiable et planifiée du pipeline.

## Stack Technique

| Outil | Rôle |
| :--- | :--- |
| **Docker** | Conteneurisation et isolation de l'environnement. |
| **Airflow** | Orchestration du pipeline (planification des tâches Python et dbt). |
| **dbt (Data Build Tool)** | Transformation des données (modélisation SQL) dans le Data Warehouse. |
| **PostgreSQL** | Data Warehouse (stockage de la donnée brute et des Data Marts). |
| **Python/Pandas** | Scripts d'extraction (E/L) des APIs. |

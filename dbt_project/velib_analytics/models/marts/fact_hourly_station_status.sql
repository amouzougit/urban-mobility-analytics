-- fact_hourly_station_status.sql
SELECT
    -- Création d'une clé horaire (Best Practice : arrondir la date à l'heure)
    date_trunc('hour', last_updated_at) AS hour_key,
    
    station_code,
    station_name,
    location,
    
    -- Calcul des métriques moyennes pour l'heure
    AVG(capacity) AS avg_capacity,
    AVG(bikes_available) AS avg_bikes_available,
    AVG(docks_available) AS avg_docks_available,
    
    -- Taux de disponibilité moyen
    AVG(bikes_available) * 100.0 / AVG(capacity) AS avg_availability_rate
    
-- Référence au modèle de staging que nous venons de créer
FROM {{ ref('stg_raw_velib_data') }} 

GROUP BY 1, 2, 3, 4
WITH velib_hourly AS (
    SELECT 
        hour_key, -- On a créé ça dans fact_hourly_station_status (date_trunc heure)
        COUNT(DISTINCT station_code) as total_stations,
        SUM(avg_bikes_available) as total_bikes_available,
        AVG(avg_availability_rate) as global_availability_rate
    FROM {{ ref('fact_hourly_station_status') }}
    GROUP BY 1
),

weather_hourly AS (
    SELECT
        -- On arrondit aussi l'heure météo pour pouvoir faire la jointure
        date_trunc('hour', ingestion_date) as hour_key,
        AVG(temperature) as avg_temp,
        AVG(humidite) as avg_humidity,
        AVG(vitesse_vent) as avg_wind,
        -- On prend la description la plus fréquente ou arbitraire pour l'heure
        MAX(description) as weather_desc
    FROM {{ ref('stg_raw_weather_data') }}
    GROUP BY 1
)

SELECT
    v.hour_key,
    v.total_bikes_available,
    v.global_availability_rate,
    w.avg_temp,
    w.avg_wind,
    w.weather_desc
FROM velib_hourly v
-- Left join car on veut les stats vélos même si la météo manque parfois
LEFT JOIN weather_hourly w ON v.hour_key = w.hour_key
ORDER BY v.hour_key DESC
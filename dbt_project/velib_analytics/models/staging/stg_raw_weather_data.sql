-- Fichier: models/staging/stg_raw_weather_data.sql

WITH source AS (
    SELECT *
    FROM {{ source('urban_data', 'raw_weather_data') }} 
),

renamed AS (
    SELECT
        city,
        temp_celsius::NUMERIC AS temperature,
        feels_like_celsius::NUMERIC AS temp_ressentie,
        humidity::INTEGER AS humidite,
        pressure::INTEGER AS pression,
        weather_description AS description,
        wind_speed::NUMERIC AS vitesse_vent,
        ingestion_date::TIMESTAMP AS ingestion_date
    FROM source
)

SELECT * FROM renamed
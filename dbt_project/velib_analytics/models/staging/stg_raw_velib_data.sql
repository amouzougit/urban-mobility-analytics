-- stg_raw_velib_data.sql
WITH source AS (
    SELECT 
        station_code,
        station_name,
        location,
        capacity,
        bikes_available,
        docks_available,
        last_updated,
        ingestion_date
    -- Nous faisons référence à la source déclarée ci-dessus (urban_data)
    FROM {{ source('urban_data', 'raw_velib_data') }} 
),

renamed AS (
    SELECT
        station_code,
        station_name,
        location,
        capacity::INTEGER AS capacity, 
        bikes_available::INTEGER AS bikes_available,
        docks_available::INTEGER AS docks_available,
        last_updated::TIMESTAMP AS last_updated_at,
        ingestion_date::TIMESTAMP AS ingestion_date_at
    FROM source
)

SELECT * FROM renamed
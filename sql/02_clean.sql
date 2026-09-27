CREATE OR REPLACE TABLE rides_clean AS
WITH parsed AS (
    SELECT
        ride_id,
        rideable_type,
        try_cast(started_at AS TIMESTAMP) AS start_time,
        try_cast(ended_at AS TIMESTAMP) AS end_time,
        start_station_name,
        nullif(trim(start_station_id), '') AS start_id,
        end_station_name,
        nullif(trim(end_station_id), '') AS end_id,
        member_casual
    FROM rides_raw
)
SELECT
    ride_id,
    rideable_type,
    start_time AS started_at,
    end_time AS ended_at,
    start_station_name,
    start_id AS start_station_id,
    end_station_name,
    end_id AS end_station_id,
    member_casual
FROM parsed
WHERE ride_id IS NOT NULL
  AND trim(ride_id) <> ''
  AND start_id IS NOT NULL
  AND end_id IS NOT NULL
  AND start_time IS NOT NULL
  AND end_time > start_time
  AND end_time <= start_time + INTERVAL '24 hours';

SELECT count(*) AS clean_rows FROM rides_clean;

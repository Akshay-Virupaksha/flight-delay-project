SELECT
    TO_DATE(CONCAT(year, '-', month, '-', day), 'YYYY-MM-DD') AS flight_date,
    ROUND(AVG(arrival_delay)::numeric, 2) AS avg_arrival_delay
FROM {{ ref('stg_flight_delays') }}
WHERE arrival_delay IS NOT NULL
GROUP BY flight_date
ORDER BY flight_date

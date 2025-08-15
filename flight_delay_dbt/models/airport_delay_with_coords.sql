SELECT 
    d.airport,
    d.total_departures,
    d.avg_dep_delay,
    d.avg_arr_delay,
    c.latitude,
    c.longitude
FROM {{ ref('airport_performances') }} d
LEFT JOIN airport_coordinates c
    ON upper(trim(d.airport)) = upper(trim(c.airport_code))

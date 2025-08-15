with airport_stats as (
    select
        origin_airport as airport,
        count(*) as total_departures,
        avg(departure_delay) as avg_dep_delay,
        avg(arrival_delay) as avg_arr_delay
    from {{ ref('stg_flight_delays') }}
    where departure_delay is not null and arrival_delay is not null
    group by origin_airport
)

select *
from airport_stats
order by avg_dep_delay desc
limit 10

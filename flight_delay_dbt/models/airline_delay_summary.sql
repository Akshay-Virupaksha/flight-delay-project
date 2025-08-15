with airline_stats as (
    select
        airline,
        count(*) as total_flights,
        avg(departure_delay) as avg_departure_delay,
        avg(arrival_delay) as avg_arrival_delay,
        avg(distance) as avg_distance,
        sum(case when departure_delay > 15 then 1 else 0 end) * 100.0 / count(*) as percent_delayed_departures,
        sum(case when arrival_delay > 15 then 1 else 0 end) * 100.0 / count(*) as percent_delayed_arrivals
    from {{ ref('stg_flight_delays') }}
    where departure_delay is not null and arrival_delay is not null
    group by airline
)

select *
from airline_stats
order by percent_delayed_arrivals desc


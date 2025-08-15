with route_delays as (
    select
        origin_airport,
        destination_airport,
        count(*) as total_flights,
        avg(arrival_delay) as avg_arrival_delay
    from {{ ref('stg_flight_delays') }}
    where arrival_delay is not null
    group by origin_airport, destination_airport
)

select *
from route_delays
order by avg_arrival_delay desc
limit 10

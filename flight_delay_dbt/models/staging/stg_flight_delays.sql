with raw as (

    select
        id,
        year,
        month,
        day,
        day_of_week,
        airline,
        flight_number,
        origin_airport,
        destination_airport,
        scheduled_departure,
        departure_time,
        departure_delay,
        scheduled_arrival,
        arrival_time,
        arrival_delay,
        air_time,
        distance
    from {{ source('public', 'flight_delays') }}

)

select * from raw
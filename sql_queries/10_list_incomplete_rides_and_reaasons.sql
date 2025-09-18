-- Query: 10 - List all incomplete rides along with the reason
-- Description: This query isolates rides that were not completed post-pickup,
-- which could signify a serious service failure or customer issue during the trip.

SELECT
    booking_id,
    customer_id,
    vehicle_type,
    incomplete_rides_reason
FROM
    ola_rides
WHERE
    incomplete_rides = 'True';


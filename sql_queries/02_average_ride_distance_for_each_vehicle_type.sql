-- Query: 02 - Find the average ride distance for each vehicle type
-- Date: 2025-09-19
-- Description: This query calculates the average ride distance for each vehicle
-- category. This helps identify which vehicle types are typically used for
-- longer vs. shorter trips.

SELECT
    vehicle_type,
    ROUND(AVG(ride_distance), 3) AS average_distance_km
FROM
    ola_rides
WHERE
    booking_status = 'Success' -- It only makes sense to calculate distance for successful rides
GROUP BY
    vehicle_type
ORDER BY
    average_distance_km DESC;
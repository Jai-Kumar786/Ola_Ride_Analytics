-- Query: 06 - Find the maximum and minimum driver ratings for Prime Sedan bookings
-- Description: This query examines the service quality range for the most popular
-- vehicle category. It uses MAX() and MIN() aggregate functions on a filtered dataset.

SELECT
    MAX(driver_ratings) AS max_rating,
    MIN(driver_ratings) AS min_rating
FROM
    ola_rides
WHERE
    vehicle_type = 'Prime Sedan' AND booking_status = 'Success';

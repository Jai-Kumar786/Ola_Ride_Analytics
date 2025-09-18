-- Query: 04 - List the top 5 customers who booked the highest number of rides
-- Date: 2025-09-20
-- Description: This query identifies the most loyal customers based on ride volume.
-- It uses COUNT to aggregate bookings, GROUP BY to segment by customer,
-- ORDER BY to rank them, and LIMIT to select the top 5.

SELECT
    customer_id,
    COUNT(booking_id) AS number_of_rides
FROM
    ola_rides
GROUP BY
    customer_id
ORDER BY
    number_of_rides DESC
LIMIT 5;

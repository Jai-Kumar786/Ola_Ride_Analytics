-- Query: 05 - Get the number of rides cancelled by drivers due to personal and car-related issues
-- Description: This query isolates a specific category of operational failure.
-- It uses the consolidated 'cancellation_reason' column and a WHERE clause
-- to count a specific reason for driver cancellations.

SELECT
    COUNT(*) AS total_driver_cancellations_personal_car_issue
FROM
    ola_rides
WHERE
    cancellation_reason = 'Personal & Car related issue';
-- Query: 09 - Calculate the total booking value of rides completed successfully
-- Description: This query calculates a top-level business KPI: the total gross
-- revenue generated from all successful rides. It uses the SUM() function.

SELECT
    SUM(booking_value) AS total_revenue
FROM
    ola_rides
WHERE
    booking_status = 'Success';

-- Query: 08 - Find the average customer rating per vehicle type
-- Description: This query directly helps us investigate Hypothesis 3. It calculates
-- the average customer satisfaction for each vehicle category, allowing us to
-- compare premium vs. economy services.

SELECT
    vehicle_type,
    Round(AVG(customer_rating),3) AS average_customer_rating
FROM
    ola_rides
WHERE
    booking_status = 'Success' -- Ratings only exist for successful rides
GROUP BY
    vehicle_type
ORDER BY
    average_customer_rating DESC;
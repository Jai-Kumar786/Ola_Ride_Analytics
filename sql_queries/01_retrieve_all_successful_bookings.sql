-- Query: 01 - Retrieve all successful bookings
-- Date: 2025-09-19
-- Description: This query answers the first business question by selecting all
-- records where the booking was successfully completed. This forms the basis
-- for all revenue and successful ride analysis.

SELECT
    *
FROM
    ola_rides
WHERE
    booking_status = 'Success';
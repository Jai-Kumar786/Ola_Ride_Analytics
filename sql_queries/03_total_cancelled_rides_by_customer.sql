-- Query: 03 - Get the total number of cancelled rides by customers
-- Date: 2025-09-19
-- Description: This query provides a key performance indicator (KPI) by
-- counting the total number of bookings that were cancelled by the customer.

SELECT
    COUNT(*) AS total_customer_cancellations
FROM
    ola_rides
WHERE
    booking_status = 'Canceled by Customer'
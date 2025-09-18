-- Query: GOAL FOR EXCELLENCE - Test Hypothesis 1
-- Description: This query goes beyond the original list to directly test our
-- first and most critical hypothesis. It counts the number of cancellations
-- for each hour of the day to find the peak cancellation period.

SELECT
    hour_of_day,
    COUNT(*) AS cancellation_count
FROM
    ola_rides
WHERE
    booking_status LIKE 'Canceled%' -- Catches both 'Canceled by Customer' and 'Canceled by Driver'
GROUP BY
    hour_of_day
ORDER BY
    cancellation_count DESC;

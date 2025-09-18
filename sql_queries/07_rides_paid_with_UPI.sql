-- Query: 07 - Retrieve all rides where payment was made using UPI
-- Description: This query filters the dataset to show all transactions for a
-- specific, important payment method.

SELECT
    *
FROM
    ola_rides
WHERE
    payment_method = 'UPI';

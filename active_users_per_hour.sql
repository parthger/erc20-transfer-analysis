WITH combined_activity AS (
    SELECT 
        EXTRACT(hour FROM evt_block_time) AS transfer_hour,
        "from" AS user
    FROM 
        erc20_ethereum.evt_transfer
    UNION ALL
    SELECT 
        EXTRACT(hour FROM evt_block_time) AS transfer_hour,
        "to" AS user
    FROM 
        erc20_ethereum.evt_transfer
)
SELECT 
    transfer_hour,
    COUNT(DISTINCT CASE WHEN user IN (SELECT DISTINCT "from" FROM erc20_ethereum.evt_transfer) THEN user END) AS unique_senders,
    COUNT(DISTINCT CASE WHEN user IN (SELECT DISTINCT "to" FROM erc20_ethereum.evt_transfer) THEN user END) AS unique_receivers,
    COUNT(DISTINCT user) AS total_unique_users
FROM 
    combined_activity
GROUP BY 
    transfer_hour
ORDER BY 
    transfer_hour;

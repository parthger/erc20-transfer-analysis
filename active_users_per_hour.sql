

-- combining sender and receiver activity into one view
WITH combined_activity AS (
    -- Get all sending activity with their hours
    SELECT 
        EXTRACT(hour FROM evt_block_time) AS transfer_hour,
        "from" AS user                   
    FROM 
        erc20_ethereum.evt_transfer
    
    UNION ALL  -- Combine with receiving activity
    
    
    SELECT 
        EXTRACT(hour FROM evt_block_time) AS transfer_hour,
        "to" AS user                      
    FROM 
        erc20_ethereum.evt_transfer
)

-- Main query 
SELECT 
    transfer_hour,
    -- Count unique addresses that have sent tokens during this hour
    COUNT(DISTINCT 
        CASE WHEN user IN (SELECT DISTINCT "from" FROM erc20_ethereum.evt_transfer) 
        THEN user END
    ) AS unique_senders,
    
    -- Count unique addresses that have received tokens during this hour
    COUNT(DISTINCT 
        CASE WHEN user IN (SELECT DISTINCT "to" FROM erc20_ethereum.evt_transfer) 
        THEN user END
    ) AS unique_receivers,
    
    -- Total unique addresses active in this hour (both sending and receiving)
    COUNT(DISTINCT user) AS total_unique_users

FROM 
    combined_activity
GROUP BY 
    transfer_hour
ORDER BY 
    transfer_hour;  -- Sort by hour for easier analysis


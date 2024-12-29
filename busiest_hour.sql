SELECT 
    EXTRACT(hour FROM evt_block_time) AS transfer_hour,
    COUNT(*) AS transfer_count
FROM 
    erc20_ethereum.evt_transfer
GROUP BY 
    EXTRACT(hour FROM evt_block_time)
ORDER BY 
    transfer_count DESC
LIMIT 1;

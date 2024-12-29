

SELECT 
   -- extracting hour component from the block timestamp
   EXTRACT(hour FROM evt_block_time) AS transfer_hour,
   
   
   COUNT(*) AS transfer_count

FROM 
   erc20_ethereum.evt_transfer  

GROUP BY 
   EXTRACT(hour FROM evt_block_time)  -- Grouping results by hour

ORDER BY 
   transfer_count DESC  -- Sort by transfer count, highest first

LIMIT 1;  -- Showing  hour with the highest activity.


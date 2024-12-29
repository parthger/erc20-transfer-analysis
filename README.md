# ERC-20 Transfer Analysis

## Overview
This repository contains SQL queries to analyze ERC-20 token transfers on the Ethereum blockchain. The analysis focuses on identifying the busiest hour of transfers and calculating active users (both senders and receivers) per hour.

### Dataset
The dataset is sourced from the `erc20_ethereum.evt_transfer` table, which includes the following key columns:
- `evt_block_time`: Timestamp of the transfer.
- `from`: Address of the sender.
- `to`: Address of the receiver.

### Queries
1. **Busiest Hour**:
   - Identifies the hour of the day with the highest number of token transfers.
   - Query file: `queries/busiest_hour.sql`

2. **Active Users per Hour**:
   - Calculates the number of unique senders, unique receivers, and total unique users for each hour of the day.
   - Query file: `queries/active_users_per_hour.sql`


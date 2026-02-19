/*
================================================================================
Task 2 – SQL Analysis

Please write queries below to answer the following questions.
Assume standard SQL syntax (e.g., PostgreSQL or SQLite).
================================================================================
*/

-- 1. Number of users by region and platform
-- TODO: Write your query here
SELECT Count(user_id) as user_count, region, platform FROM users GROUP BY region, platform;

-- 2. Number of devices per user
-- TODO: Write your query here
SELECT user_id, Count(device_id) FROM devices GROUP BY user_id;
-- assume that user_id+device_id is PK and there is no repeated device for a user --

-- 3. Event volume per device type per day
-- TODO: Write your query here
SELECT count(*) as event_volume, date(e.event_ts) as event_date, d.device_type
FROM events e INTO devices d ON e.device_id = d.device_id
GROUP BY date(e.event_ts), d.device_type;

-- 4. Identify devices with unusually high event volume
-- (Explain your reasoning for "unusually high" in a comment)
-- TODO: Write your query here

-- "Unusual" can be considered in different conditions. --
-- Here, I assume "Unusually High" is Greater than 2 x Average --
-- and in SQL command I want to use:
-- WITH x AS (SELECT ... ) SELECT ... FROM x ...
WITH device_event_count AS (
    SELECT device_id, COUNT(*) AS event_count FROM events GROUP BY device_id)
SELECT device_id, event_count
FROM device_event_count
WHERE event_count > (
    SELECT 2 * AVG(event_count)
    FROM device_event_count )

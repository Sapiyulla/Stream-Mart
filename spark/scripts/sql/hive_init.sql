CREATE DATABASE IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS events (
    event_id STRING,
    event_type STRING,
    timestamp STRING,
    payload STRUCT<
        user_id: INT,
        item_id: INT,
        category: STRING,
        price: FLOAT,
        quantity: INT,
        rating: INT,
        reason: STRING
    >,
    topic STRING,
    date DATE
)
USING DELTA
PARTITIONED BY (topic, date)
LOCATION 's3a://streammart/raw/events';
from pathlib import Path
import duckdb

Path("outputs").mkdir(exist_ok=True)

con = duckdb.connect("citibike.duckdb")

rows = con.execute("""
    SELECT
        station_id,
        station_name,
        departures,
        arrivals,
        avg_net_outflow_per_day
    FROM station_hour_flow
    WHERE day_type = 'weekday'
      AND hour_of_day = 8
      AND departures + arrivals >= 100
    ORDER BY avg_net_outflow_per_day DESC
    LIMIT 10
""").fetchall()

con.execute("""
    COPY (
        SELECT
            station_id,
            station_name,
            departures,
            arrivals,
            avg_net_outflow_per_day
        FROM station_hour_flow
        WHERE day_type = 'weekday'
          AND hour_of_day = 8
          AND departures + arrivals >= 100
        ORDER BY avg_net_outflow_per_day DESC
        LIMIT 10
    )
    TO 'outputs/weekday_8am_top10.csv'
    (HEADER, DELIMITER ',')
""")

for row in rows:
    print(row)

print("\n已生成：outputs/weekday_8am_top10.csv")
con.close()
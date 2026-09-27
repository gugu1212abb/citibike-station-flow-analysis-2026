from pathlib import Path
import duckdb

sql = Path("sql/05_station_flow.sql").read_text(encoding="utf-8")
if not sql.strip():
    raise ValueError("05_station_flow.sql 是空文件，请先粘贴 SQL 并保存")

con = duckdb.connect("citibike.duckdb")
con.execute(sql)

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
    LIMIT 5
""").fetchall()

for row in rows:
    print(row)

con.close()
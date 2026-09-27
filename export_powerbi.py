from pathlib import Path
import duckdb

output = Path("outputs")
output.mkdir(exist_ok=True)

con = duckdb.connect("citibike.duckdb")

con.execute("""
    COPY demand_day_type
    TO 'outputs/demand_day_type.csv'
    (HEADER, DELIMITER ',')
""")

con.execute("""
    COPY station_hour_flow
    TO 'outputs/station_hour_flow.csv'
    (HEADER, DELIMITER ',')
""")

for name in ["demand_day_type.csv", "station_hour_flow.csv"]:
    path = output / name
    print(name, "大小（MB）：", round(path.stat().st_size / 1024**2, 2))

con.close()
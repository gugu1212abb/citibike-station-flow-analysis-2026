from pathlib import Path
from zipfile import ZipFile
import shutil
import duckdb

csv_dir = Path("data/csv")
csv_dir.mkdir(parents=True, exist_ok=True)

with ZipFile("202604-citibike-tripdata.zip") as archive:
    for item in archive.infolist():
        if not item.filename.lower().endswith(".csv"):
            continue

        target = csv_dir / Path(item.filename).name
        if not target.exists() or target.stat().st_size != item.file_size:
            print("解压：", item.filename, flush=True)
            with archive.open(item) as source, target.open("wb") as dest:
                shutil.copyfileobj(source, dest)

print("开始导入数据库，可能需要几分钟……", flush=True)
con = duckdb.connect("citibike.duckdb")
con.execute("""
    CREATE OR REPLACE TABLE rides_raw AS
    SELECT *
    FROM read_csv(
        'data/csv/*.csv',
        union_by_name = true,
        all_varchar = true
    )
""")

result = con.execute("""
    SELECT
        count(*) AS rows,
        count(DISTINCT ride_id) AS unique_ride_ids,
        min(try_cast(started_at AS TIMESTAMP)) AS first_ride,
        max(try_cast(started_at AS TIMESTAMP)) AS last_ride
    FROM rides_raw
""").fetchone()

print("总行数、不同 ride_id 数、最早时间、最晚时间：")
print(result)
con.close()
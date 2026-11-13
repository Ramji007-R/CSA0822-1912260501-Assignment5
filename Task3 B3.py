
import csv
import sqlite3
import time
import random
import cProfile
import pandas as pd

for stations in [1, 12, 120]:
    filename = f"data_{stations}.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "day", "pm25"])

        for s in range(stations):
            for day in range(365):
                for hour in range(24):
                    writer.writerow([
                        f"S{s+1}",
                        day,
                        random.randint(10, 150)
                    ])

    print(filename, "created")

# Generate sample data for comparison
data = []

with open("data_12.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        data.append((
            row["station"],
            int(row["day"]),
            float(row["pm25"])
        ))

# Python loop method
start = time.time()

totals = {}
counts = {}

for station, day, value in data:
    key = (station, day)
    totals[key] = totals.get(key, 0) + value
    counts[key] = counts.get(key, 0) + 1

averages = {
    key: totals[key] / counts[key]
    for key in totals
}

python_time = time.time() - start

# Pandas method
start = time.time()

df = pd.DataFrame(data, columns=["station", "day", "pm25"])
pandas_result = df.groupby(
    ["station", "day"]
)["pm25"].mean()

pandas_time = time.time() - start

# SQL method
conn = sqlite3.connect(":memory:")
df.to_sql("readings", conn, index=False, if_exists="replace")

start = time.time()

sql_result = pd.read_sql_query("""
SELECT station, day, AVG(pm25)
FROM readings
GROUP BY station, day
""", conn)

sql_time = time.time() - start

print("Python Time:", python_time)
print("Pandas Time:", pandas_time)
print("SQL Time:", sql_time)

print("\nProfiling Python:")
cProfile.run("sum(range(100000))")

conn.close()


import csv
import sqlite3
import matplotlib.pyplot as plt

data = [
    ["Station", "PM25"],
    ["S1", "45"],
    ["S2", "60"],
    ["S3", "-10"],
    ["S4", "NA"],
    ["S5", "120"],
    ["S6", "1100"],
    ["S7", "30"]
]

clean_data = []

for row in data[1:]:
    try:
        value = float(row[1])
        if 0 <= value <= 999:
            clean_data.append([row[0], value])
    except ValueError:
        continue

values = [row[1] for row in clean_data]
minimum = min(values)
maximum = max(values)

for row in clean_data:
    row.append((row[1] - minimum) / (maximum - minimum))

print("Cleaned Data:")
for row in clean_data:
    print(row)

conn = sqlite3.connect("air_quality.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS readings(
station TEXT,
pm25 REAL,
normalised REAL
)
""")

cur.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    clean_data
)

conn.commit()

cur.execute("SELECT * FROM readings")
print("\nDatabase Records:")
for row in cur.fetchall():
    print(row)

plt.bar([r[0] for r in clean_data], values)
plt.xlabel("Station")
plt.ylabel("PM2.5")
plt.title("Air Quality Readings")
plt.savefig("air_quality.png")
plt.show()

conn.close()

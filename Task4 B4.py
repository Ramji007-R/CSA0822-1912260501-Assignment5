
import sqlite3
import time
from datetime import date, timedelta

# Sentiment analysis
positive_words = ["good", "clean", "improved", "excellent"]
negative_words = ["bad", "poor", "pollution", "dirty"]

def sentiment(text):
    score = 0

    for word in positive_words:
        if word in text.lower():
            score += 1

    for word in negative_words:
        if word in text.lower():
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# Extractive summariser
def summarise(text):
    sentences = text.split(".")
    return ". ".join(sentences[:2])

complaints = [
    "Air quality is very bad. Pollution is increasing.",
    "The air is clean and good today.",
    "There is too much pollution near the road.",
    "Air quality has improved. The environment is clean.",
    "The area is dirty and polluted."
] * 10

print("Sentiment Analysis Results")

for complaint in complaints:
    print(complaint, "->", sentiment(complaint))

print("\nSummary:")
print(summarise(
    "Air pollution is increasing. People are facing health problems. "
    "More monitoring stations are required."
))

# SQLite database
conn = sqlite3.connect("final_air_quality.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS readings(
station TEXT,
day TEXT,
pm25 REAL
)
""")

start_date = date(2026, 1, 1)
data = []

for station in range(1, 11):
    for day in range(30):
        current_date = start_date + timedelta(days=day)

        data.append((
            f"S{station}",
            current_date.isoformat(),
            30 + station + day
        ))

cur.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    data
)

conn.commit()

# Query without index
start = time.time()

cur.execute("""
SELECT AVG(pm25)
FROM readings
WHERE station = ? AND day = ?
""", ("S1", "2026-01-10"))

print("\nAverage without index:", cur.fetchone()[0])
without_index = time.time() - start

# Create index
cur.execute("""
CREATE INDEX IF NOT EXISTS idx_station_day
ON readings(station, day)
""")

start = time.time()

cur.execute("""
SELECT AVG(pm25)
FROM readings
WHERE station = ? AND day = ?
""", ("S1", "2026-01-10"))

print("Average with index:", cur.fetchone()[0])
with_index = time.time() - start

print("\nQuery Time Without Index:", without_index)
print("Query Time With Index:", with_index)

conn.close()

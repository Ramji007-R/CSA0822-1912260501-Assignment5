
import sqlite3
import csv
from io import StringIO

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("""
CREATE TABLE readings(
station TEXT,
pm25 REAL
)
""")

data = [
    ("S1", 45),
    ("S2", 60),
    ("S3", 30)
]

cur.executemany(
    "INSERT INTO readings VALUES (?, ?)",
    data
)

station = "S1"
cur.execute(
    "SELECT * FROM readings WHERE station = ?",
    (station,)
)

print("Search Result:", cur.fetchall())

# SQL injection test
attack = "' OR '1'='1"

cur.execute(
    "SELECT * FROM readings WHERE station = ?",
    (attack,)
)

print("Injection Test:", cur.fetchall())

# Invalid CSV tests
test_data = [
    "station,pm25\nS1,45\nS2,60",
    "station;pm25\nS1;45",
    "station,pm25\nS1,-20",
    "station,pm25\nS1,abc"
]

for item in test_data:
    print("\nTesting CSV:")
    print(item)

    reader = csv.reader(StringIO(item))
    rows = list(reader)

    for row in rows:
        print(row)

# Sentiment edge cases
complaints = [
    "Good air quality",
    "Bad pollution",
    "",
    "Not good",
    "Very bad air"
]

positive_words = ["good", "clean", "excellent"]
negative_words = ["bad", "poor", "pollution"]

for text in complaints:
    score = 0

    for word in positive_words:
        if word in text.lower():
            score += 1

    for word in negative_words:
        if word in text.lower():
            score -= 1

    print(text, "Score:", score)

conn.close()

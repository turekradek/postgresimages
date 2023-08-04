import json
import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="password",
    host="localhost", # or the Docker Machine's IP if you're using Docker Toolbox
    port="5432"
)
cur = conn.cursor()

# Create table if it doesn't exist
# cur.execute("""
#     CREATE TABLE IF NOT EXISTS database_json(
#         integer INTEGER,
#         name TEXT,
#         date DATE,
#         float FLOAT
#     )
# """)
# conn.commit()

# Open the JSON file and load the data
with open('data.json') as f:
    data = json.load(f)

# For each object in the data, generate and execute an SQL INSERT statement
try:
    for item in data:
        print(f'Inserting: {item["integer"]}, {item["name"]}, {item["date"]}, {item["float"]}')
        cur.execute("INSERT INTO database_json VALUES (%s, %s, %s, %s)",
                    (item['integer'], item['name'], item['date'], item['float']))
    conn.commit()
except Exception as e:
    print("Error occurred while inserting data:", e)

try:
    cur.execute("SELECT * FROM database_json LIMIT 5")
    rows = cur.fetchall()
    print("First 5 rows in the table:")
    for row in rows:
        print(row)
except Exception as e:
    print("Error occurred while selecting data:", e)

conn.commit()
conn.close()
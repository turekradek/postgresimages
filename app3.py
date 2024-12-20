import json
import psycopg2

def check_json_keys(file_path):
    with open(file_path) as f:
        data = json.load(f)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        keys = data[0].keys()
        return keys
    else:
        return None

def insert_data_to_table(cur, conn, data, keys_in_json):
    try:
        placeholders = ', '.join(['%s'] * len(keys_in_json))
        columns = ', '.join(keys_in_json)
        
        for item in data:
            values = [item[key] for key in keys_in_json]
            print(f'Inserting: {", ".join(map(str, values))}')
            
            query = f"INSERT INTO wyniki ({columns}) VALUES ({placeholders})"
            cur.execute(query, values)
        conn.commit()
    except Exception as e:
        print("Error occurred while inserting data:", e)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="radek",
    host="localhost", # or the Docker Machine's IP if you're using Docker Toolbox
    port="5432"
)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS wyniki(
        Id_kierowcy TEXT,
        Punkty INTEGER,
        Id_wyscigu TEXT
    )
""")
conn.commit()

# Open the JSON file and load the data
with open('data3.json') as f:
    data = json.load(f) 
# Usage example
json_file_path = 'data3.json'
keys_in_json = check_json_keys(json_file_path)

if keys_in_json:
    with open(json_file_path) as f:
        data = json.load(f)
    insert_data_to_table(cur, conn, data, keys_in_json)

# Select and print first 5 rows in the table
try:
    cur.execute("SELECT * FROM wyniki  LIMIT 5")
    rows = cur.fetchall()
    print("First 5 rows in the table:")
    for row in rows:
        print(row)
except Exception as e:
    print("Error occurred while selecting data:", e)

conn.commit()
conn.close()
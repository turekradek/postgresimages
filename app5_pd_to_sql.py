import json
import uuid
import random
from datetime import datetime, timedelta
import os 
import sys 
import pandas as pd
import numpy as np
import requests
import zipfile
import xlsxwriter
import  psycopg2
from sqlalchemy import create_engine, inspect
import sqlalchemy as sa
import openpyxl

#table_name = 'kiersql1' #sys.argv[1]
#new_database = 'matura2015'
# postgres_username = 'postgres'
# postgres_password = 'radek'
# postgres_host = 'localhost'
# postgres_port = '5432'
# #postgres_dbname = f'table_name'
# files_json = 'data3.json'
# if n := len( sys.argv) == 2:
#     new_database = sys.argv[1]
#     #file_json = sys.argv[2]
# elif n == 3:
#     new_database = sys.argv[1]
#     table_name = sys.argv[2]
# elif n == 4:
#     new_database = sys.argv[1]
#     table_name = sys.argv[2]
#     files_json = sys.argv[3]
# else:
#     new_database = 'matura2015'
#     table_name = 'kiersql1' #sys.argv[1]
#     file_json = 'data3.json'
#def check_json_keys(file_path):
#    with open(file_path) as f:
#        data = json.load(f)
#    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
#        keys = data[0].keys()
#        return keys
#    else:
#        return None

#def insert_data_to_table(cur, conn, data, keys_in_json):
#    try:
#        placeholders = ', '.join(['%s'] * len(keys_in_json))
#        columns = ', '.join(keys_in_json)
#        
#        for item in data:
#            values = [item[key] for key in keys_in_json]
#            print(f'Inserting: {", ".join(map(str, values))}')
#            
#            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#            cur.execute(query, values)
#        conn.commit()
#    except Exception as e:
#        print("Error occurred while inserting data:", e)
        
def create_dataframe(file_name):
    with open(file_name, 'r') as f:
        data = json.load( f )
    df = pd.DataFrame(data)
    return df 

# data = create_dataframe('data2.json')
# #print( data.head(20))
# #data.to_sql(name='kiersql', con=con)
# # Establish a connection to the PostgreSQL database
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password="radek",
#     host="localhost", # or the Docker Machine's IP if you're using Docker Toolbox
#     port="5432"
# )
# print( 'CONNECTION CREATED')
# cur = conn.cursor()
# print( 'CUR DONE')
def create_database( cur, conn , new_database):
    """Creates a database in PostgreSQL.

    Args:
      engine_database: A SQLAlchemy engine object.
      new_database: The name of the database to create.
    """
    try:
        conn.autocommit = True
        # check id the database already exists
        #cur.execute(f'SELECT 1 FROM pg_database where datname = {new_database};')
        cur.execute("SELECT 1 FROM pg_database WHERE datname=\'{new_database}\';")
        exists = cur.fetchone()
        #for row in exists:
        #    print( f'---- {row}')
        if not exists:
            cur.execute(f"""
                CREATE DATABASE {new_database};
                """)
        #conn.commit()
    except Exception as e:
        print( "Error occured while creating the database: " , e )

def create_table( cur, conn , new_database):
    """Creates a database in PostgreSQL.

    Args:
      engine_database: A SQLAlchemy engine object.
      new_database: The name of the database to create.
    """

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {new_database} (
            Id_kierowcy TEXT,
            Nazwisko TEXT,
            Imie TEXT,
            Kraj TEXT
        );
    """)
    conn.commit()


#engine_database = sa.create_engine( f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/' )
# create_database( cur, conn , new_database ) 
#engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
# print( 'engine CREATED')
#data.to_sql(name='kiersql', con=engine, if_exists='replace',index=False)
# Create table if it doesn't exist  DZIALA ALE TYLKO Z TABELA DLA WYNIKOW
#cur.execute(f"""
#    CREATE TABLE IF NOT EXISTS {table_name}(
#        Id_kierowcy TEXT,
#        Punkty INTEGER,
#        Id_wyscigu TEXT
#    )
#""")
#conn.commit()
#table = sa.Table(table_name,  sa.MetaData(),
#        sa.Column( 'Id_kierowcy', sa.Integer, primary_key=True),
#        sa.Column( 'Nazwisko', sa.String(100)),
#        sa.Column( 'Imie', sa.String(100)),
#        sa.Column( 'Kraj', sa.String(100))
#        )
#table.create(engine)
#data.to_sql( table_name, engine, if_exists='replace', index=False)

# print( 'TABLE CREATED ' )
# Check if the table exists
#insp = inspect(engine)
#if not insp.has_table(f'{table_name}'):
#    print( 'CONDITION IF NOT INS.HAS_TABEL')
#    # Create the table if it doesn't exist
#    data.to_sql(name=table_name, con=engine, index=False)
#    print( 'DATA TO SQL ')
#else:
#    print( 'CONDITION ELSE ')
#    data.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

#data.to_sql(name=table_name, con=engine, if_exists='replace',index=False)
# Open the JSON file and load the data
#with open(f'{file_json}') as f:
#    data = json.load(f) 
# Usage example
#json_file_path = '{}'.format(file_json)
#keys_in_json = check_json_keys(json_file_path)

#if keys_in_json:
#    with open(json_file_path) as f:
#        data = json.load(f)
#    insert_data_to_table(cur, conn, data, keys_in_json)

# Select and print first 5 rows in the table
# def select_print_rows():
#try:
#    cur.execute(f"SELECT * FROM {table_name}  LIMIT 5")
#    rows = cur.fetchall()
#    print("First 5 rows in the table:")
#    for row in rows:
#        print(row)
#except Exception as e:
#    print("Error occurred while selecting data:", e)

# conn.commit()
# conn.close()

# if __name__=='__main__':
#     pass

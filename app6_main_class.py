import json
import uuid
import random
from datetime import datetime, timedelta
import os 
import sys 
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Union, Any, Optional
import requests
import zipfile
import xlsxwriter
import  psycopg2
from sqlalchemy import create_engine, inspect
import sqlalchemy as sa
import openpyxl
import argparse 
# from app5_pd_to_sql import create_database, create_table, create_dataframe
# from json_test_all import read_columns_from_file, create_dictionary, create_data
#table_name = 'kiersql1' #sys.argv[1]
#new_database = 'matura2015'
class PostgresCredentials():
    postgres_credentials = { 
        'postgres_username' : 'postgres',
        'postgres_password' : 'radek',
        'postgres_host' : 'localhost',
        'postgres_port' : '5432',
    }
    
class PostgresConnection(PostgresCredentials):
    def __init__(self,username, password, host,port ):
        super().__init__()
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        
    def get_connection_database(self, database=None):
        conn = psycopg2.connect(
            dbname="postgres",
            user=self.username,
            password=self.password,
            host=self.host , # or the Docker Machine's IP if you're using Docker Toolbox
            port=self.port
        )
        cur = conn.cursor()
        return conn, cur
    
    def get_engine(self ):
        # engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
        engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/')
        return engine 
    
    def get_engine_data_base(self , new_database):
        # engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
        engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{new_database}')
        return engine 
    def commit_connection(self, connection):
        connection.commit()
        
    def close_connection(self,connection, cursor):
        cursor.close()
        connection.close()
        
parser = argparse.ArgumentParser(description='take arguments ')
# Add command-line arguments
parser.add_argument('file_to_read', help='The file to read.')
parser.add_argument('file_name', nargs='?', help='The name of the output file (optional).')
parser.add_argument('new_database', nargs='?', help='The name of the output file (optional).')
# Parse the command-line arguments
args = parser.parse_args()
# Access the values
file_to_read = args.file_to_read
file_name = args.file_name
new_database = args.new_database
print(f'file_to_read = {file_to_read}')
print(f'file_name = {file_name}')
#postgres_dbname = f'table_name'
files_json = 'data3.json'
#if n := len( sys.argv) == 2:
#    new_database = sys.argv[1]
#    #file_json = sys.argv[2]
#elif n == 3:
#    new_database = sys.argv[1]
#    table_name = sys.argv[2]
#elif n == 4:
#    new_database = sys.argv[1]
#    table_name = sys.argv[2]
#    files_json = sys.argv[3]
#else:
#    new_database = 'matura2015'
#    table_name = 'kiersql1' #sys.argv[1]
#    file_json = 'data3.json'
    
    
############ json test all .py 
def read_columns_from_file(file_name, separator ):
    """
    Reads the first line of a text file, which is assumed to contain column names separated by the specified separator,
    and returns the column names as a list.

    Parameters:
    - file_name (str): The name of the file to read from.
    - separator (str): The separator used to split the column names.

    Returns:
    - list of str: A list of column names extracted from the file's first line.

    Example:
    If the file's first line is "Name, Age, Address" and the separator is ",", the function will return
    ['Name', 'Age', 'Address'] as the list of column names.
    """
    file = open( file_name , 'r' )
    columns = file.readline().strip()
    print(f'1 columns {columns}')
    columns = columns.split( separator )
    print(f'2 columns {columns}')
    return columns 

def create_dictionary(  columns: list ):
    """
    Creates a dictionary where each column name is a key, and its corresponding value is set to the same name.

    Parameters:
    - columns (list): A list of column names to be used as keys in the dictionary.

    Returns:
    - dict: A dictionary where each column name is a key, and its value is set to the same name.

    Example:
    If you call create_dictionary(['Name', 'Age', 'Address']), it will return a dictionary like this:
    {'Name': 'Name', 'Age': 'Age', 'Address': 'Address'}
    """
    dictionary = {}
    for name in columns:
        dictionary[name] = name
    return dictionary

def create_data( file_name: str, dictionary: dict ):
    """
    Reads data from a text file using a provided dictionary to interpret the columns, and returns a list of dictionaries
    where each dictionary represents a row of data with column names as keys.

    Parameters:
    - file_name (str): The name of the file to read data from.
    - dictionary (dict): A dictionary that maps column names to their positions in each line of the file.

    Returns:
    - list of dict: A list of dictionaries, where each dictionary represents a row of data with column names as keys.

    Example:
    If you have a file with the following content:
    "Name;Age;Address"
    "John;30;123 Main St"
    "Alice;25;456 Elm St"
    
    And you call create_data('data.txt', {'Name': 0, 'Age': 1, 'Address': 2}), it will return a list like this:
    [{'Name': 'John', 'Age': '30', 'Address': '123 Main St'},
     {'Name': 'Alice', 'Age': '25', 'Address': '456 Elm St'}]
    """
    file = open( file_name ,  'r' )
    content = [  line. strip() for line in  file.readlines() ]
    content = content[1:]    
    data = []
    keys = list( dictionary.keys() )
    print( f'\n\n\nkeys: {keys}')
    for index, linia in enumerate(content):
        resutl = {}
        linia = linia.split(';')
        # print( f'linia : {linia}')
        for i in range(len(keys)):
            resutl[keys[i]] = linia[i]
        data.append( resutl ) 
        result = {}
    print( data[:10], f'\n\n {len(data)}' )
    return  data 

def write_data_to_json(file_name, data1):
    """
    Writes the given data to a JSON file.

    Parameters:
    - file_name (str): The name of the JSON file to write the data to.
    - data1: The data to be written to the JSON file.

    Example:
    If you call write_data_to_json('output.json', {'Name': 'John', 'Age': 30, 'Address': '123 Main St'}),
    it will write the data to 'output.json' in JSON format.
    """
    with open(file_name , 'w') as f:
        json.dump(data1, f)
        
        
############ json test all .py 

############ app6 .py 
def check_json_keys(file_path):
    """
    Reads a JSON file and checks if it contains a list of dictionaries. If so, it returns the keys of the first dictionary.

    Parameters:
    - file_path (str): The path to the JSON file to be checked.

    Returns:
    - list or None: If the JSON file contains a list of dictionaries, it returns the keys of the first dictionary as a list.
      If the JSON file does not match the expected structure, it returns None.

    Example:
    If you have a JSON file 'data.json' with the following content:
    [{"Name": "John", "Age": 30, "Address": "123 Main St"},
     {"Name": "Alice", "Age": 25, "Address": "456 Elm St"}]
     
    Calling check_json_keys('data.json') will return ['Name', 'Age', 'Address'].
    """
    with open(file_path) as f:
        data = json.load(f)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        keys = data[0].keys()
        return keys
    else:
        return None

def insert_data_to_table(cur, conn, data, keys_in_json):
    """
    Inserts data into a database table using a cursor and a database connection.

    Parameters:
    - cur: The database cursor for executing SQL queries.
    - conn: The database connection.
    - data (list of dict): The data to be inserted, where each dictionary represents a row of data.
    - keys_in_json (list of str): The keys to extract values from dictionaries in the 'data' list.
    - table_name (str): The name of the database table to insert data into.

    Example:
    If you have a list of dictionaries 'data' and a list of keys 'keys_in_json' like this:
    data = [{'Name': 'John', 'Age': 30, 'Address': '123 Main St'},
            {'Name': 'Alice', 'Age': 25, 'Address': '456 Elm St'}]
    keys_in_json = ['Name', 'Age', 'Address']

    You can call insert_data_to_table(cur, conn, data, keys_in_json, 'my_table_name') to insert the data into the specified database table.
    """
    try:
        placeholders = ', '.join(['%s'] * len(keys_in_json))
        columns = ', '.join(keys_in_json)
        
        for item in data:
            values = [item[key] for key in keys_in_json]
            print(f'Inserting: {", ".join(map(str, values))}')
            
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cur.execute(query, values)
        conn.commit()
    except Exception as e:
        print("Error occurred while inserting data:", e)
 
############ app6 .py 

####################################
def create_dataframe(file_name):
    with open(file_name, 'r') as f:
        data = json.load( f )
    df = pd.DataFrame(data)
    return df 

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

def read_table( cur, conn , table_name ):
    try:
        cur.execute(f"SELECT * FROM {table_name}  LIMIT 5")
        rows = cur.fetchall()
        print("First 5 rows in the table:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Error occurred while selecting data:", e)
        
###################################
def create_dataframe_from_excel_sheet(file_name, name_sheet):
    result = pd.read_excel(file_name, sheet_name=name_sheet)
    return result

######################
def data_frame_to_sql(data_frame,table_name,  engine):
    data_frame.to_sql(name=table_name, con=engine, if_exists='replace',index=False)
    

######################
#data = create_dataframe('data2.json')
#print( data.head(20))
#data.to_sql(name='kiersql', con=con)
# Establish a connection to the PostgreSQL database
#conn = psycopg2.connect(
#    dbname="postgres",
#    user="postgres",
#    password="radek",
#    host="localhost", # or the Docker Machine's IP if you're using Docker Toolbox
#    port="5432"
#)
#print( 'CONNECTION CREATED')
#cur = conn.cursor()
#print( 'CUR DONE')
# create_database( cur, conn , new_database ) 
# engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')

########################################## DODANE Z app61.py
#engine_database = sa.create_engine( f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/' )
#create_database( cur, conn , new_database ) 
#engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
#print( 'engine CREATED')
#read_table(cur, conn, 'kierowcy')
#df_unavailable_sessions = create_dataframe_from_excel_sheet('unavailable_sessions_.xlsx', 'Unavailable sessions')
#print( df_unavailable_sessions.head(20))
#df_unavailable_sessions_part = df_unavailable_sessions.iloc[:200]
# engine1 = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/exceltest')

#data_frame_to_sql(data_frame,table_name,  engine)
# data_frame_to_sql(df_unavailable_sessions_part ,'test1excel',  engine1)
#
#read_table(cur, conn, 'test1excel')
# create_database( cur, conn , new_database )
# engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')

#################### doane z app61.py 
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

#print( 'TABLE CREATED ' )
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

#conn.commit()
#conn.close()

if __name__=='__main__':
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="radek",
        host="localhost", # or the Docker Machine's IP if you're using Docker Toolbox
        port="5432"
    )
    print( 'CONNECTION CREATED')
    cur = conn.cursor()
    print( 'CUR DONE')
    engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
    #df_unavailable_sessions = create_dataframe_from_excel_sheet('unavailable_sessions_.xlsx', 'Unavailable sessions')
    #print( df_unavailable_sessions.head(20))
    #df_unavailable_sessions_part = df_unavailable_sessions.iloc[:200]
    create_database( cur, conn, new_database)
    engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
    file_excel = None
    if file_to_read.endswith('.xlsx'):
        file_excel = file_to_read
    if file_excel != None:
        excel_file = pd.ExcelFile( file_excel)
        sheets_names = excel_file.sheet_names
        sheets_names = sheets_names[2:]
        #create_database( cur, conn, new_database)
        for sheet in sheets_names:
            df = create_dataframe_from_excel_sheet( file_to_read, sheet)
            print( f'sheet - > {sheet}')
            print( df.head(15) ) 
            data_frame_to_sql( df, sheet, engine)
            # read_tabel( cur, conn, table_name)
    conn.commit()
    conn.close()

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
postgres_username = 'postgres'
postgres_password = 'radek'
postgres_host = 'localhost'
postgres_port = '5432'
parser = argparse.ArgumentParser(description='take arguments ')
# Add command-line arguments
parser.add_argument('dbname',type=str, help='Name of database to connect to')
parser.add_argument('dbuser',type=str, help='Name of user to connect to database')
parser.add_argument('dbpasswd',type=str, help='Password of user to connect to database')
parser.add_argument('dbhost',type=str, help='Name of host to connect to database')
parser.add_argument('dbport',type=int, help='Port to connect to database')
parser.add_argument('file_to_read', help='The file to read.')
parser.add_argument('file_name', nargs='?', help='The name of the output file (optional).')
parser.add_argument('new_database', nargs='?', help='The name of the output file (optional).')
# Parse the command-line arguments
args = parser.parse_args()
# Access the values
dbname = args.dbname
dbuser = args.dbuser
dbpasswd = args.dbpasswd
dbhost = args.dbhost
dbport = args.dbport
file_to_read = args.file_to_read
file_name = args.file_name
new_database = args.new_database
print( f'  dbname =        {dbname}       ')
print( f'  dbuser =        {dbuser}       ')
print( f'  dbpasswd =      {dbpasswd}     ')
print( f'  dbhost =        {dbhost}       ')
print( f'  dbport =        {dbport}       ')
print( f'  file_to_read =  {file_to_read} ')
print( f'  file_name =     {file_name}    ')
print( f'  new_database =  {new_database} ')
#postgres_dbname = f'table_name'
files_json = 'data3.json'

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
def file_text_to_dataframe(file_name):
    df = pd.read_table(file_name, sep=';')#, header=True)
    return df 
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
    

# file_excel = r'unavailable_sessions_LATEST.xlsx'
# file_excel = file_to_read
# excel_file = pd.ExcelFile(file_excel)
# print( dir( excel_file ) )
# sheet_name = excel_file.sheet_names
# print( sheet_name )
# df_unavailable_sessions = create_dataframe_from_excel_sheet(excel_file, 'Unavailable sessions')
# df_unavailable_sessions.index += 1 
# print( df_unavailable_sessions.head() ) 


if __name__=='__main__':
    conn = psycopg2.connect(
        dbname=dbname,
        user=dbuser,
        password=dbpasswd,
        host=dbhost, # or the Docker Machine's IP if you're using Docker Toolbox
        port=dbport
    )
    file_excel = file_to_read
    excel_file = pd.ExcelFile(file_excel)
    print( dir( excel_file ) )
    sheet_name = excel_file.sheet_names
    print( sheet_name )
    sheet_name1 = {  name : name.replace(' ').lower()   for name in sheet_name }
    df_unavailable_sessions = create_dataframe_from_excel_sheet(excel_file, sheet_name1['Unavailable sessions'])
    df_unavailable_sessions.index += 1 
    print( df_unavailable_sessions.head() ) 
    engine = create_engine(f'postgresql://{dbuser}:{dbpasswd}@{dbhost}:{dbport}/{dbname}')
    data_frame_to_sql(df_unavailable_sessions, 'sessions', engine=engine)
    
    show_table2 = pd.read_sql_table( sheet_name1['Unavailable sessions'], engine )
    
    print(  show_table2.iloc[:20])
    
    # conn = psycopg2.connect(
    #     dbname="postgres",
    #     user="postgres",
    #     password="radek",
    #     host="localhost", # or the Docker Machine's IP if you're using Docker Toolbox
    #     port="5432"
    # )
    print( 'CONNECTION CREATED')
    # cur = conn.cursor()
    print( 'CUR DONE')
    # engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
    # engine = create_engine(f'postgresql://{dbuser}:{dbpasswd}@{dbhost}:{dbport}/{dbname}')
    #df_unavailable_sessions = create_dataframe_from_excel_sheet('unavailable_sessions_.xlsx', 'Unavailable sessions')
    #print( df_unavailable_sessions.head(20))
    #df_unavailable_sessions_part = df_unavailable_sessions.iloc[:200]
    # engine = create_engine(f'postgresql://{dbuser}:{dbpasswd}@{dbhost}:{dbport}/{dbname}')
    # create_database( cur, conn, new_database)
    # engine = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/{new_database}')
    # file_excel = None
    # if file_to_read.endswith('.xlsx'):
    #     file_excel = file_to_read
    # if file_excel != None:
    #     excel_file = pd.ExcelFile( file_excel)
    #     sheets_names = excel_file.sheet_names
    #     sheets_names = sheets_names[2:]
    #     #create_database( cur, conn, new_database)
    #     for sheet in sheets_names:
    #         df = create_dataframe_from_excel_sheet( file_to_read, sheet)
    #         print( f'sheet - > {sheet}')
    #         print( df.head(15) ) 
    #         data_frame_to_sql( df, sheet, engine)
    #         # read_tabel( cur, conn, table_name)
    # if file_to_read.endswith('.txt'):
    #     df = file_text_to_dataframe(file_to_read)
    #     table_name = file_to_read.split('.txt')[0].lower()
    #     engine_table = create_engine(f'postgresql://{postgres_username}:{postgres_password}@localhost:5432/')
    #     data_frame_to_sql(df, table_name, engine_table)
        
    conn.commit()
    conn.close()

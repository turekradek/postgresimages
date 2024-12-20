import json
import uuid
import random
from datetime import datetime, timedelta
import os 
import pandas as pd
import numpy as np
import requests
import zipfile
import xlsxwriter
import  psycopg2
from sqlalchemy import create_engine
import openpyxl
# Create a list to store the data
# data = []
columns = []
directory = r'Kierowcy.txt'

def read_columns_from_file(file_name, separator ):
    
    file = open( file_name , 'r' )
    columns = file.readline().strip()
    print(f'1 columns {columns}')
    columns = columns.split( separator )
    print(f'2 columns {columns}')
    return columns 

columns = read_columns_from_file( directory, ';')
print( ' these are columns from txt file {}'.format(columns) )

def create_dictionary(  columns: list ):
    dictionary = {}
    for name in columns:
        dictionary[name] = name
    return dictionary

dictionary = create_dictionary( columns ) 
print( f' dictionar {dictionary}')

def create_data( file_name: str, dictionary: dict ):
    file = open( file_name ,  'r' )
    content = [  line. strip() for line in  file.readlines() ]
    content = content[1:]    
    data = []
    keys = list( dictionary.keys() )
    print( f'\n\n\nkeys: {keys}')
    for index, linia in enumerate(content):
        resutl = {}
        linia = linia.split(';')
        print( f'linia : {linia}')
        resutl[keys[0]] = linia[0]
        # print( f'=== 0 resutl {resutl }')
        resutl[keys[1]] = linia[1]
        # print( f'=== 1 resutl {resutl }')
        resutl[keys[2]] = linia[2]
        # print( f'=== 2 resutl {resutl }')
        resutl[keys[3]] = linia[3]
        # print( f'=== 3 resutl {resutl }')
        data.append( resutl ) 
        # print( f' index {index} \n data _+_+_+_+_+ {data}' )
        result = {}
    print( data, f'\n\n {len(data)}' )
    return  data 


data1 =  create_data(directory, dictionary )

# Write the data to a JSON file
with open('data2.json', 'w') as f:
    json.dump(data1, f)
    
# print( f' data1 {data1}\n\n\n]')
    
# input()
#def create_data( file_name: str,  columns: list ):
    

# Write the data to a JSON file
#with open('data_nazwiska.json', 'w') as f:
#    json.dump(data, f)

import json
import uuid
import random
from datetime import datetime, timedelta
import os 
import sys
import argparse 

parser = argparse.ArgumentParser(description='take arguments ')
# Add command-line arguments
parser.add_argument('file_to_read', help='The file to read.')
parser.add_argument('file_name', nargs='?', help='The name of the output file (optional).')
# Parse the command-line arguments
args = parser.parse_args()
# Access the values
file_to_read = args.file_to_read
file_name = args.file_name
print(f'file_to_read = {file_to_read}')
print(f'file_name = {file_name}')
# args = parser.parse_args()
# print( f'args parser : %s' % args)
# Create a list to store the data
# data = []
columns = []
# directory = r'Wyniki.txt'
# file_name = r'data3.json'
# file_to_read = None
# file_name = None
dicto = { }
# for i in range(len(sys.argv)):
#     print( f' i = {i} arg {sys.argv[i]}')
#     dicto[i] = sys.argv[i]
# print( dicto )
# if n := len(sys.argv) == 2:
#     print('if n == 2')
#     file_to_read = sys.argv[1]
#     print( f' file_to_read = {file_to_read}')
# elif n == 3:
#     file_to_read = sys.argv[1]
#     file_name = sys.argv[2]
#     print('if n == 3')
#     print( f' file_to_read = {file_to_read}')
#     print( f' file_name = {file_name}')
# else:
#     # file_to_read = r'Wyniki.txt'
#     # file_name = r'data3.json'
#     print( len(sys.argv) , 'to jest else ')
    
# print( f'sys.argv =  {sys.argv}')    
# print( f' file_to_read = {file_to_read}')
# print( f' file_name = {file_name}')

def read_columns_from_file(file_name, separator ):
    
    file = open( file_name , 'r' )
    columns = file.readline().strip()
    print(f'1 columns {columns}')
    columns = columns.split( separator )
    print(f'2 columns {columns}')
    return columns 


def create_dictionary(  columns: list ):
    dictionary = {}
    for name in columns:
        dictionary[name] = name
    return dictionary



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
        # print( f'linia : {linia}')
        for i in range(len(keys)):
            resutl[keys[i]] = linia[i]
        # # print( f'=== 0 resutl {resutl }')
        # resutl[keys[1]] = linia[1]
        # # print( f'=== 1 resutl {resutl }')
        # resutl[keys[2]] = linia[2]
        # # print( f'=== 2 resutl {resutl }')
        # #resutl[keys[3]] = linia[3]
        # # print( f'=== 3 resutl {resutl }')
        data.append( resutl ) 
        # print( f' index {index} \n data _+_+_+_+_+ {data}' )
        result = {}
    print( data[:10], f'\n\n {len(data)}' )
    return  data 




# Write the data to a JSON file
def write_data_to_json(file_name, data1):
    with open(file_name , 'w') as f:
        json.dump(data1, f)
        
# columns = read_columns_from_file( file_to_read, ';')
# print( ' these are columns from txt file {}'.format(columns) )
# dictionary = create_dictionary( columns ) 
# print( f' dictionar {dictionary}')
# data1 =  create_data(file_to_read, dictionary )
# write_data_to_json(file_name, data1 )    
# print( f' data1 {data1}\n\n\n]')
    
# input()
#def create_data( file_name: str,  columns: list ):
    

# Write the data to a JSON file
#with open('data_nazwiska.json', 'w') as f:
#    json.dump(data, f)

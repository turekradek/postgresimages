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
import argparse 

class PostgresCredentials:
    postgres_credentials = {
        'postgres_username' : 'postgres',
        'postgres_password' : 'radek',
        'postgres_host' : 'localhost',
        'postgres_port' : '5432',
    }
    

class PostgresConnetion(PostgresCredentials):
    def __init__(self) -> None:
        super().__init__()
        # self.username = postgres_credentials['postgres_username']
        self.username = self.postgres_credentials['postgres_username']
        self.password = self.postgres_credentials['postgres_password']
        self.host = self.postgres_credentials['postgres_host']
        self.port = self.postgres_credentials['postgres_port']
        
    def get_connection_database(self):
        conn = psycopg2.connect(
            dbname='postgres',
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        cur = conn.cursor()
        return conn, cur 
    
    def read_table(self,  cur, conn , table_name ):
        try:
            cur.execute(f"SELECT * FROM {table_name}  LIMIT 5")
            rows = cur.fetchall()
            print("First 5 rows in the table:")
            for row in rows:
                print(row)
        except Exception as e:
            print("Error occurred while selecting data:", e)
    
        
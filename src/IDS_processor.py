import pandas as pd
import db_operations as db_ops
from time import sleep
import datetime
from datetime import date
import sqlite3
from db_operations import DatabaseOperations
import pandas as pd
import pickle
import os 
import re 

COLUMNS = ['ts',	'uid', 'src_ip', 'src_p',	'dst_ip', 'dst_p', 'proto', 'service',	'duration',	'src_bytes', 'dst_bytes',	'conn_state',	'local_orig',	'local_resp',	'missed_bytes',	'history',	'orig_pkts',	'orig_ip_bytes',	'resp_pkts',	'resp_ip_bytes',	'tunnel_parents',	'ip_proto']


def process_data(new_lines):
    ''' Function to process the data from zeek logs '''

    pass

def getData(fp): 
    ''' Function to get data from zeek every n seconds'''
    # File path = /opt/homebrew/Cellar/zeek/7.1.0/logs/current
    data = pd.read_csv(fp, sep='\t', names=COLUMNS, comment="#", dtype={'ts': 'float64'})
    



def main(): 

    # Get Current date
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    # Feel free to replace later
    pattern = r'^conn.*$' 

    file_path = f'/opt/homebrew/Cellar/zeek/7.1.0/logs/{formatted_date}'
    # Number of seconds to wait before getting data again
    n_seconds = 60
    df = pd.DataFrame()
    for filename in os.listdir():
        if re.search(pattern, filename):
            file_path = os.path.join(file_path, filename)
            df = getData(file_path)
            process_data(df)
            df = pd.DataFrame()
            break

main()
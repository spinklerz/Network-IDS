import pandas as pd
from tensorflow import keras
from time import sleep
import datetime
import hashlib
from datetime import date
import sqlite3
import pandas as pd
import pickle
import gzip 
import os 
from sklearn.preprocessing import StandardScaler
import re 
import numpy as np

import sys
sys.path.append('../db/')
import db_operations as db_ops
sys.path.append('../utils/')
import utils 

global TOTAL_PACKETS 
TOTAL_PACKETS = 0

global ANON_PACKETS 
ANON_PACKETS = 0

expected_columns = ['uid', 'src_ip', 'src_p', 'dst_ip', 'dst_p', 'duration', 'missed_bytes',
                'history', 'ip_proto', 'src_bytes/src_pkts', 'dst_bytes/dst_pkts',
                'proto_tcp', 'proto_udp', 'proto_unknown_transport', 'service_ayiya',
                'service_ayiya,quic', 'service_dce_rpc,ntlm,smb,gssapi',
                'service_dce_rpc,smb,gssapi,ntlm', 'service_dhcp', 'service_dns',
                'service_ftp', 'service_ftp-data', 'service_gssapi',
                'service_gssapi,ntlm,smb', 'service_http', 'service_http,ssl',
                'service_krb_tcp', 'service_mqtt', 'service_ntlm',
                'service_ntlm,gssapi,smb', 'service_ntp', 'service_quic',
                'service_quic,ssl', 'service_quic,ssl,ayiya', 'service_smb,gssapi,ntlm',
                'service_smb,ntlm,gssapi', 'service_ssh', 'service_ssl',
                'service_ssl,http', 'service_ssl,quic', 'service_ssl,quic,ayiya',
                'conn_state_REJ', 'conn_state_RSTO', 'conn_state_RSTOS0',
                'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1',
                'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH',
                'conn_state_SHR', 'local_orig_T', 'local_resp_T']

COLUMNS = ['ts', 'uid', 'src_ip', 'src_p',	'dst_ip', 'dst_p', 'proto', 'service',	'duration',	'src_bytes', 'dst_bytes',	'conn_state',	'local_orig',	'local_resp',	'missed_bytes',	'history',	'orig_pkts',	'orig_ip_bytes',	'resp_pkts',	'resp_ip_bytes',	'tunnel_parents',	'ip_proto']
pickle_file_path = '../pkl/preprocess_function.pkl'
loaded_model = keras.models.load_model("../model/model.keras")

with open('../scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def getData(fp): 
    global TOTAL_PACKETS
    global ANON_PACKETS
    ''' Function to get data from zeek every n seconds'''
    # File path = /opt/homebrew/Cellar/zeek/7.1.0/logs/{date}
    # Expects file to be in gzip format
    data = pd.read_csv(fp, sep='\t', names=COLUMNS, comment="#", dtype={'ts': 'float64'}, compression='gzip')
    TOTAL_PACKETS = TOTAL_PACKETS + len(data)
    # After preprocessing
    new_data = utils.preprocessing(data)
    # Align your data with the expected columns
    new_data = new_data.reindex(columns=expected_columns, fill_value=0)

    features_scaled = scaler.transform(new_data)

    # Continue with prediction
    results = loaded_model.predict(features_scaled)
    is_anomaly = np.mean(np.square(results - features_scaled), axis=1)  # was np.sqaure
    threshold = np.percentile(is_anomaly, 95)  # Flag top 5% as anomalous
    data['is_anomaly'] = is_anomaly > threshold
    data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    anon = data[data['is_anomaly'] == True]
    # This will iterate through the Series properly - CORRECT
    # In your getData function, before calling add_record:
    anon = anon.reset_index(drop=True)  # Reset index to 0, 1, 2, ...
    ANON_PACKETS = ANON_PACKETS + len(anon)
    db_ops.add_record(anon['src_ip'], anon['dst_ip'], anon['src_p'], anon['dst_p'], anon['proto'], anon['service'])


def main(): 
    db_ops.init_db()
    # Get Current date
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    # Feel free to replace later
    pattern = r'^conn\..*$' 

    file_path = f'/opt/homebrew/Cellar/zeek/7.1.0/logs/{formatted_date}'
    # Number of seconds to wait before getting data again
    n_seconds = 60
    df = pd.DataFrame()
    for filename in os.listdir(file_path):
        if re.search(pattern, filename):
            print(f"Found file: {filename}")
            full_file_path = os.path.join(file_path, filename)  # Use different variable
            df = getData(full_file_path)
            df = pd.DataFrame()
            # Don't reset file_path here - keep it as the directory
    print(f"Total packets processed: {TOTAL_PACKETS}")
    print(f"Total anomalous packets detected: {ANON_PACKETS}")
main()
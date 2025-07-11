import pandas as pd
import os
import ipaddress
import hashlib
import numpy as np
from sklearn.preprocessing import StandardScaler
    
    
    
    
def preprocessing(df):

        # so pandas resets index whenever it wants i guess...

    # Data Type Assignment
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')  # Convert duration to numeric (coerce invalid values to NaN)
    df['src_bytes'] = pd.to_numeric(df['src_bytes'], errors='coerce')  # Convert orig_bytes to numeric
    df['dst_bytes'] = pd.to_numeric(df['dst_bytes'], errors='coerce')  # Convert resp_bytes to numeric
    df['orig_pkts'] = pd.to_numeric(df['orig_pkts'], errors='coerce')  # Convert orig_pkts to numeric
    df['resp_pkts'] = pd.to_numeric(df['resp_pkts'], errors='coerce')  # Convert resp_pkts to numeric
    df['orig_ip_bytes'] = pd.to_numeric(df['orig_ip_bytes'], errors='coerce')  # Convert orig_ip_bytes to numeric
    df['resp_ip_bytes'] = pd.to_numeric(df['resp_ip_bytes'], errors='coerce')  # Convert resp_ip_bytes to numeric
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')  # Convert duration to numeric


    # Feature Engineering
    f_data = df.copy()
    f_data['dst_bytes_per_orig_pkt'] = (f_data['dst_bytes'] / f_data['orig_pkts']).replace(0, 1)
    f_data['dst_bytes_per_resp_pkt'] = (f_data['dst_bytes'] / f_data['resp_pkts']).replace(0, 1)


        # Replace infinite values with a reasonable fallback
    f_data['dst_bytes_per_orig_pkt'] = f_data['dst_bytes_per_orig_pkt'].replace([np.inf, -np.inf], 0)
        # Drop the component features you've engineered from, but keep src_bytes
    f_data.drop(['orig_pkts', 'dst_bytes', 'resp_pkts', 'orig_ip_bytes', 'resp_ip_bytes'], axis=1, inplace=True)
            # Everything Looks good!
    # Drop Missed_bytes
    f_data = f_data.drop(columns=['missed_bytes'], axis=1 )
    e_data = f_data.copy()

    # Set ip datatype
    temp1 = []
    for x in e_data['src_ip']:
        try:
            temp1.append(int(ipaddress.IPv4Address(x)) % 65535)
        except:
            temp1.append(int(ipaddress.IPv6Address(x)) % 4294967295 )
    e_data['src_ip'] = pd.Series(temp1)

    temp = []
    for x in e_data['dst_ip']:
        try:
            temp.append(int(ipaddress.IPv4Address(x)) % 65535 )
        except:
            temp.append(int(ipaddress.IPv6Address(x)) % 4294967295 )


    e_data['uid'] = hash(str(e_data['uid'])) % 100000
    e_data['history'] = hash(str(e_data['history'])) % 100000

    # One Hot Encode
    e_data = pd.get_dummies(e_data, columns=['proto', 'service', 'conn_state', 'local_orig', 'local_resp' ], drop_first=True, dtype=float)

    e_data['dst_ip'] = pd.Series(temp)
    e_data['src_ip'] = e_data['src_ip'].astype('uint64')
    e_data['dst_ip'] = e_data['dst_ip'].astype('uint64')
    e_data.drop(columns=['ts', 'tunnel_parents'],inplace=True)
    e_data = e_data.fillna(0)
    return e_data
import db
from db import add_data, delete_data, dump_all_activity, init_db

def __init__(db_path="./anomalous_db.db"):
    self.db_path = db_path
    db.init_db(self.db_path)

def add_record( src_ip, dst_ip, sport, dport, proto, service):
    for x in range(len(src_ip)):
        print((str(src_ip[x]), str(dst_ip[x]), int(sport[x]), int(dport[x]), str(proto[x]), str(service[x])))
        add_data(src_ip[x], dst_ip[x], sport[x], dport[x], proto[x], service[x])

def delete_record(src_ip=None, dst_ip=None):
    delete_data(src_ip, dst_ip)

def dump_all_records():
    db.dump_all_activity()

def test_function():
    db_ops = DatabaseOperations()
    db_ops.add_record('192.168.1.1', '192.168.1.20', 12345, 8000, 'TCP', 'HTTP')
    db_ops.dump_all_records()
    pass
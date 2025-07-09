import db
from db import add_data, delete_data, dump_all_activity, init_db



class DatabaseOperations:
    def __init__(self, db_path="./anomalous_db.db"):
        self.db_path = db_path
        db.init_db(self.db_path)

    def add_record(self, src_ip, dst_ip, sport, dport, proto, service):
        add_data(src_ip, dst_ip, sport, dport, proto, service)

    def delete_record(self, src_ip=None, dst_ip=None):
        delete_data(src_ip, dst_ip)

    def dump_all_records(self):
        db.dump_all_activity()

def test_function():
    db_ops = DatabaseOperations()
    db_ops.add_record('192.168.1.1', '192.168.1.20', 12345, 8000, 'TCP', 'HTTP')
    db_ops.dump_all_records()
    pass
test_function()
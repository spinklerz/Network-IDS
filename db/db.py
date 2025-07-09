import sqlite3
import os 

R = "\033[91m"  # Red text
W = "\033[0m"   # Reset to default
G = "\033[92m"  # Green text
B = "\033[94m"  # Blue text
'''
CREATE TABLE table_name (
    column_name data_type constraints,
    column_name data_type constraints,
    ...
);
'''
def init_db(DATABASE="anomalous_db.db"):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor() 
    
    # Simple table for now
    cursor.execute('''CREATE TABLE IF NOT EXISTS anomalous(
        src_ip TEXT NOT NULL,
        dst_ip TEXT NOT NULL, 
        sport INTEGER, 
        dport INTEGER, 
        proto TEXT NOT NULL,
        service TEXT DEFAULT 'unknown'
    )''')
    conn.commit()
    conn.close()
    print(f"{G}Database initialized successfully🥳{W}")

def add_data(src_ip, dst_ip, sport, dport, proto, service, DATABASE="./anomalous_db.db"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO anomalous(src_ip,dst_ip,sport,dport,proto,service) VALUES (?, ?, ?, ?, ?, ?)", (src_ip, dst_ip, sport, dport, proto, service))
    conn.commit()
    conn.close()
    pass

def delete_data(src_ip, dst_ip, DATABASE="anomalous_db.db"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM anomalous WHERE src_ip = ? OR dst_ip = ?", (src_ip, dst_ip))
    if cursor.rowcount == 0:
        print(f"{R}No records found for {src_ip} or {dst_ip}{W}")
    conn.commit()
    conn.close()
    pass

def dump_all_activity(DATABASE="anomalous_db.db"):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anomalous")
    data = cursor.fetchall()
    print(f"\n{G}*****ALL THE FALSE POSITIVES LETS GOO******{W}")
    print(f"{B}{'SRC IP': <15} {'DST IP': <15} {'SRC PORT': <15} {'DST PORT': <15} {'PROTO': <15} {'SERVICE': <5}{W}")
    for x in data:
        print(f"{x[0]: <15} {x[1]: <15} {x[2]: <15} {x[3]: <15} {x[4]: <15} {x[5]: <5}")
    pass
'''
def main():
    init_db()
    add_data(f'192.168.1.1', '192.168.1.20', 12345, 80, 'TCP', 'HTTP')
    dump_all_activity()

# Fully functional v1.0 
main()
'''
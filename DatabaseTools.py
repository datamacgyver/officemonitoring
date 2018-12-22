import pyodbc
import db_deets as db
from datetime import datetime

# TODO: Proper excepts
# TODO: try/catches for failed pushes. What behaviour? . 


def get_time():
    return str(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')) 
        
class DatabaseTools:  

    def __init__(self):
        self.conn_string = ('Driver={SQL Server};' 
                           'Server=%s;'
                           'Database=%s;'
                           'uid=%s;' 
                           'pwd=%s') % (db.url, db.db, db.user, db.passwrd	)

        self.conn = pyodbc.connect(self.conn_string) 
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        print('Connected to database')

    def get_cursor(self):
        try:
            return self.conn.cursor()
        except:    
            self.conn = pyodbc.connect(CONN_STRING) 
            self.conn.autocommit = True
            return self.conn.cursor()

    def db_operation(self, DBstring):
        print(DBstring)
        try:
            self.cursor.execute(DBstring)
        except:
            self.get_cursor()                
            self.cursor.execute(DBstring)

    def push_value(self, vals, table, cols):
      cols = ', '.join(cols)
      vals = ', '.join([str(val) for val in vals])
      
      cmd = "insert into %s (timestamp, %s) values ('%s', %s)" % (table, cols, get_time(), vals)
      self.db_operation(cmd)	
      
    def __del__(self):
        self.conn.close()
        print('Connection Closed')
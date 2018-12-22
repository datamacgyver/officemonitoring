import pyodbc
import cpu_monitor
import db_deets as db

# TODO: Proper excepts
# TODO: try/catches for failed pushes. What behaviour? . 


def get_time():
    return str(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')) 
        
class DatabaseTools:  

    def __init__(self):
        self.conn_string = 'Driver={SQL Server};'
                           'Server=%s;'
                           'Database=%s;'
                           'uid=%s;' 
                           'pwd=%s' % (db.url db.db, db.user, db.passwd)

        self.conn = pyodbc.connect(self.connString) 
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        try:
            return self.conn.cursor()
        except:    
            self.conn = pyodbc.connect(CONN_STRING) 
            self.conn.autocommit = True
            return self.conn.cursor()

    def db_operation(self, DBstring):
        try:
            self.cursor.execute(DBstring)
        except:
            self.getCursor()                
            self.cursor.execute(DBstring)

    def push_value(vals, table, cols):
      cols = ', '.join(cols)
      vals = ', '.join(vals)
      
      cmd = "insert into %s (datetime, %s) values (%s, %s)" % (table, cols, get_time(), vals)
      db_operation(cmd)
      
    def __del__(self):
        self.conn.close()
import pyodbc
from datetime import datetime

from secure.logons import db_passwrd, db_user, db_dsn

# TODO: try/catches for failed Hive actions. What behaviour?


def get_time():
    return str(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')) 


class DatabaseTools:
    def __init__(self):
        self.conn_str = "DSN=%s;UID=%s;PWD=%s" % (db_dsn, db_user, db_passwrd)
        self.conn = pyodbc.connect(self.conn_str)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        print('Connected to database')

    def _get_cursor(self):
        try:
            return self.conn.cursor()
        except:    
            self.conn = pyodbc.connect(self.conn_str)
            self.conn.autocommit = True
            return self.conn.cursor()

    def _db_change(self, db_string):
        print(db_string)
        try:
            self.cursor.execute(db_string)
        except:
            self._get_cursor()
            self.cursor.execute(db_string)
        finally:
            self.cursor.commit()

    def _db_search(self, db_string):
        print(db_string)
        try:
            self.cursor.execute(db_string)
        except:
            self._get_cursor()
            self.cursor.execute(db_string)

    def push_new_reading(self, val, table, col=None):
        col = col if col else table
        val = str(val)
      
        cmd = "insert into %s (timestamp, %s) values ('%s', %s)" % \
              (table, col, get_time(), val)
        self._db_change(cmd)

    def record_hive_command(self, hive_command):
        cmd = "insert into hivecommands (timestamp, %s) values ('%s', %s)" % \
              ('command', get_time(), hive_command)
        self._db_change(cmd)

    def store_latest_value(self, hive_command, val):
        cmd = "select count(*) from lastrecorded where variable = '%s'" % \
              hive_command

        self._db_search(cmd)
        row_count = int(self.cursor.fetchone()[0])

        if row_count > 0:
            cmd = "UPDATE lastrecorded SET timestamp = '%s', reading = %s " \
                  " WHERE variable = '%s';" % (get_time(), val, hive_command)
            self._db_change(cmd)
        else:
            cmd = "insert into lastrecorded (timestamp, variable, reading) " \
                  "values ('%s', '%s', %s)" % (get_time(), hive_command, val)
            self._db_change(cmd)
      
    def __del__(self):
        self.conn.close()
        print('Connection Closed')


if __name__ == "__main__":
    db = DatabaseTools()
    db.store_latest_value('room_temp', 0)

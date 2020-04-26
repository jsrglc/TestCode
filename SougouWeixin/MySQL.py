MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'weixin'

import pymysql

class MySQL():
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE):
        '''Initialize the MySQL database'''
        try:
            self.db = pymysql.connect(host, username, password, database, charset='utf8')
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print('MySQL error: ', e.args)
    
    def insert(self, table, data):
        '''Insert data into table'''
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql_query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print('MySQL error: ', e.args)
            self.db.rollback()
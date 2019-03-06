import mysql.connector
import mysql.connector.pooling


class MySqlClient(object):
    def __init__(self):
        pass

    def get_connection(self, config):
        return mysql.connector.connect(**config)

    def get_connection_pool(self, config):
        return mysql.connector.pooling.MySQLConnectionPool(pool_name='ijob', pool_size=19, **config)

import pymssql


class SansysUser:
    def __init__(self, user, password, server='poseidon', database='sansys_readonly'):
        self.username = user
        self.password = password
        self.server = server
        self.database = database

    def connect(self):
        try:
            conn = pymssql.connect(server=self.server,
                                   database=self.database,
                                   user=f'AGUASJVE\\{self.username}',
                                   password=self.password)
            return conn

        except pymssql.OperationalError:
            return False

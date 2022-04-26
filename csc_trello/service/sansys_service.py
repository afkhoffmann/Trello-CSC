import pandas as pd


class SansysService:
    def __init__(self, connection):
        self.query_ = ""
        self.conn = connection

    def get_sansys_data(self):
        self.conn.execute()

    def build_query(self, protocols):
        self.query_ = f"""
                SELECT ID_SERVICO

                FROM OPE_SERVICO
                WHERE ID_SERVICO IN ({','.join(protocols)})
                AND CH_SITUACAO_SERVICO IN (3,4,6)
        """

    def execute_query(self):
        with self.conn.cursor() as cursor:
            cursor.execute(self.query_)
            data = cursor.fetchall()

        if len(data) == 0:
            return pd.DataFrame(columns=['ID_SERVICO'])
        else:
            return pd.DataFrame(data, columns=['ID_SERVICO'])

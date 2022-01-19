import pymysql.cursors


class MySQLServer:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3307):
        self.connect = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
            port=port
        )

    def close(self):
        self.connect.close()

    def connection(self, host: str, user: str, password: str, database: str, port: int = 3307):
        self.connect = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
            port=port
        )

    def insert(self, name_table: str, data: dict) -> int:
        with self.connect.cursor() as cursor:
            fields = []
            values = []
            for key, value in data.items():
                fields.append(f'`{key}`')
                if type(value) is int: values.append(f'{value}')
                else: values.append(f'"{value}"')
            cmd = f'INSERT INTO `{name_table}` ({",".join(fields)}) VALUES ({",".join(values)})'
            try:
                cursor.execute(cmd)
                self.connect.commit()
                return 0
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                return 1

    def select(self, name_table: str, fields: list, condition: str = '') -> list[dict]:
        with self.connect.cursor() as cursor:
            for field in fields:
                field = f'`{field}`'
            if len(condition) > 0: condition = 'WHERE '+condition
            cmd = f'SELECT {",".join(fields)} FROM {name_table} {condition}'
            cursor.execute(cmd)
            result = cursor.fetchall()
        self.connect.commit()
        return result

    def is_exists(self, name_table: str, condition: str) -> bool:
        with self.connect.cursor() as cursor:
            cmd = f'SELECT 1 FROM {name_table} WHERE {condition}'
            cursor.execute(cmd)
            result = cursor.fetchall()
        self.connect.commit()
        return False if len(result) == 0 else True


#server = MySQLServer('127.0.0.1', 'root', 'root', 'company', 3306)
#result = server.is_exists('user', '`id`>0')
#server.close()
#print(result)

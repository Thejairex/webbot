import sqlite3

class Db:
    def __init__(self) -> None:
        self.conn = sqlite3.Connection("db.db")
        self.cur = self.conn.cursor()
        self.create()
        
        
    def create(self):
        try:
            self.cur.execute('''
                             CREATE TABLE Ordenes(
                                 id_orden INTEGER PRIMARY KEY AUTOINCREMENT,
                                 module VARCHAR(15),
                                 active VARCHAR(15),
                                 time_orden VARCHAR(15),
                                 action VARCHAR(15),
                                 dia VARCHAR(15),
                                 estado INTEGER
                             )
                             ''')
            
            self.cur.execute('''
                             CREATE TABLE Executedos(
                                 id_executed INTEGER PRIMARY KEY AUTOINCREMENT,
                                 id_orden INTEGER,
                                 result VARCHAR(15),
                                 amount REAL
                             )
                             ''')

            self.conn.commit()
            
        except Exception as e:
            if str(e) == "table Ordenes already exists":
                pass
            
            else:
                print(str(e))
                self.conn.rollback()
            
    def init_thread(self):
        conn = sqlite3.Connection("db.db")
        cur = conn.cursor()
        return conn, cur
        
    def table_info(self, table: str, cur):
        "Return columns and placeholders without the ID of the table."

        cur.execute(f"PRAGMA table_info({table})")
        columnas = cur.fetchall()
        columnas.pop(0)
        columnas_str = ', '.join([columna[1] for columna in columnas])
        # print(columnas_str)
        placeholders = ', '.join(['?' for _ in columnas]) 
        # print(placeholders)
        return columnas_str, placeholders
    
    def table_info_v2(self, table: str, cur):
        "Return columns and placeholders with the ID of the table."
        cur.execute(f"PRAGMA table_info({table})")
        columnas = cur.fetchall()
        columnas_str = ', '.join([columna[1] for columna in columnas])
        placeholders = ', '.join(['?' for _ in columnas]) 
        return columnas_str, placeholders
    
    def get_id_table(self, table: str, cur):
        "Return the first column uniquely."
        cur.execute(f"PRAGMA table_info({table})")
        columnas = cur.fetchall()
        return columnas[0][1]
    
    def insert(self, table: str, values):
        conn, cur = self.init_thread()
        columnas, placeholders = self.table_info(table, cur)
        query = f"INSERT INTO {table} ({columnas}) VALUES ({placeholders})"
        cur.execute(query, values)
        conn.commit()
        conn.close()
        
    def insert_many(self, table: str, values):
        columnas, placeholders = self.table_info(table)
        placeholders = ', '.join(['?' for _ in range(len(values[0]))])  # Crear los placeholders para los valores
        query = f"INSERT INTO {table} ({columnas}) VALUES (null,{placeholders})"
        self.cur.execute(query, values)
        self.conn.commit()
    
    def select_all(self, table):
        conn, cur = self.init_thread()
        query = f"SELECT * FROM {table} ORDER BY id_orden DESC"
        cur.execute(query)
        datas = cur.fetchall()
        conn.close()
        return datas
    
    def select_last_data(self, table) -> tuple:
        conn, cur = self.init_thread()
        id_table = self.get_id_table(table, cur)
        query = f"SELECT * FROM {table} WHERE {id_table} = (SELECT max({id_table}) FROM {table})"
        cur.execute(query)
        data = cur.fetchone()
        conn.close()
        return data
    
    def merge_table(self, query):
        conn, cur = self.init_thread()
        cur.execute(query)
        conn.commit()
        conn.close()
        
if __name__ == "__main__":
    data = Db()
    columnas = data.select_last_data("Ordenes")
    print(columnas)
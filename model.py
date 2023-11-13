import sqlite3

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error  as e:
            print(f"Error connecting to the database: {e}")
            raise e

    def create_table(self, table_name, columns):
        try:
            columns_string =  ", ".join([f"{field} {type}" for field, type in columns.items()])
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_string})")
        except sqlite3.Error as e:
            print(f"Error creating the table: {e}")
            raise e

    def update_data(self, table_name, data, condition):
        try:
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

            self.cursor.execute(query, list(data.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            raise e

    def insert_data(self, table_name, data):
        try:
            placeholders = "null, " + ", ".join(["?"] * len(data))  # Null here autogenerates the ID
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            self.cursor.execute(query, data)
            self.conn.commit()

            # Get the ID of the inserted row
            inserted_id = self.cursor.lastrowid
            return inserted_id
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            raise e

    def get_data(self, data, table_name, conditions = None, joins = None):
        query =  f"SELECT {', '.join(data)} FROM {table_name} "

        if joins:
            for join_table, connection in joins.items():
                query += f"LEFT JOIN {join_table} ON {join_table}.{connection}={table_name}.{connection} "

        if conditions:
            query += f"WHERE {' AND '.join(conditions)} "

        return self.query_data(query)

    def query_data(self, query):
        try:
            self.cursor.execute(query)

            columns = [column[0] for column in self.cursor.description]
            results = []

            for row in self.cursor.fetchall():
                row_dict = dict(zip(columns, row))
                results.append(row_dict)

            return results

        except sqlite3.Error as e:
            print(f"Error querying data: {e}")
            raise e

    def delete_row(self, table_name, condition):
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting row: {e}")
            raise e

    def delete_table(self, table_name):
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting table: {e}")
            raise e

    def close(self):
        if self.conn:
            self.conn.close()

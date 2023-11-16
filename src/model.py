import sqlite3

class DatabaseHandler:
    def __init__(self, db_path, verbose = False):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.verbose = verbose

    def create_table(self, table_name, attributes):
        try:
            attributes_string =  ", ".join([f"{field} {type}" for field, type in attributes.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({attributes_string})"
            if self.verbose:
                print(query)
            self.cursor.execute(query)
            return None
        except sqlite3.Error as e:
            print(f"Error creating the table: {e}")
            return e

    def update_data(self, table_name, data, condition):
        try:
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            if self.verbose:
                print(query)
                print(list(data.values()))

            self.cursor.execute(query, list(data.values()))
            self.conn.commit()
            return None
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            return e

    def insert_data(self, table_name, data):
        try:
            placeholders = "null, " + ", ".join(["?"] * len(data))  # Null here autogenerates the ID
            query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            if self.verbose:
                print(query)
                print(data)

            self.cursor.execute(query, data)
            self.conn.commit()

            inserted_id = self.cursor.lastrowid
            return inserted_id, None
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return None, e

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
            if self.verbose:
                print(query)
            self.cursor.execute(query)

            attributes = [column[0] for column in self.cursor.description]
            results = []

            for row in self.cursor.fetchall():
                row_dict = dict(zip(attributes, row))
                results.append(row_dict)

            return results, None

        except sqlite3.Error as e:
            print(f"Error querying data: {e}")
            return None, e

    def delete_row(self, table_name, condition):
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            if self.verbose:
                print(query)
            self.cursor.execute(query)
            self.conn.commit()
            return None
        except sqlite3.Error as e:
            print(f"Error deleting row: {e}")
            return e

    def delete_table(self, table_name):
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            if self.verbose:
                print(query)
            self.cursor.execute(query)
            self.conn.commit()
            return None
        except sqlite3.Error as e:
            print(f"Error deleting table: {e}")
            return e

    def close(self):
        if self.conn:
            self.conn.close()

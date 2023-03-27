import sqlite3

class SQLiteWrapper:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Create a table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS facialrecognition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metadata TEXT,
                name TEXT
            )
        """)
    
    def create_table(self, table_name, columns):
        """
        Creates a new table in the database.
        
        :param table_name: The name of the table to be created.
        :param columns: A list of strings representing the columns of the table in the format "name type constraints"
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(query)
        self.conn.commit()
    
    def insert(self, table_name, values):
        """
        Inserts a new row into the specified table.
        
        :param table_name: The name of the table to insert the data into.
        :param values: A list of values to be inserted into the table.
        """
        placeholders = ', '.join('?' * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def update(self, table_name, values, conditions):
        """
        Updates existing rows in the specified table.
        
        :param table_name: The name of the table to update the data in.
        :param values: A dictionary of column names and new values to update.
        :param conditions: A dictionary of column names and values to select the rows to update.
        """
        set_clause = ', '.join([f"{k} = ?" for k in values.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        self.cursor.execute(query, list(values.values()) + list(conditions.values()))
        self.conn.commit()

    def delete(self, table_name, conditions):
        """
        Deletes existing rows in the specified table.

        :param table_name: The name of the table to delete the data from.
        :param conditions: A dictionary of column names and values to select the rows to delete.
        """
        where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        self.cursor.execute(query, list(conditions.values()))
        self.conn.commit()

    def select(self, table_name, columns='*', condition=''):
        """
        Selects data from the given table.

        :param table_name: name of the table
        :param columns: a string containing column names separated by commas. Example: 'column_name, column_name, ...'
        :param condition: a string containing the condition for selecting the data. Example: 'id = 5'
        :return: a list of tuples containing the selected data.
        """
        query = f"SELECT {columns} FROM {table_name} {'WHERE ' + condition if condition else ''}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete(self, table_name, condition):
        """
        Deletes data from the given table.
        :param table_name: name of the table
        :param condition: a string containing the condition for eleting the data. Example: 'id = 5'
        """
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()
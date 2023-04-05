import mysql.connector

class db_operations():

    # constructor with connection back to database
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", 
                               user="root",
                               password="cpsc408",
                               auth_plugin='mysqlnative_password',
                               database="RideShare"
                               )
        self.cursor = self.connection.cursor()
        print("Connection made...")

    def create_database_tables(self):
        query = '''
        CREATE TABLE songs(
            songID VARCHAR(22) NOT NULL PRIMARY KEY,
            Name VARCHAR(20),
            Artist VARCHAR(20),
            Album VARCHAR(20),
            releaseDate DATETIME,
            Genre VARCHAR(20),
            Explicit BOOLEAN,
            Duration DOUBLE,
            Energy DOUBLE,
            Danceability DOUBLE,
            Acousticness DOUBLE,
            Liveness DOUBLE,
            Loudness DOUBLE
        );
        '''
        self.cursor.execute(query)
        print("Table Created")

    # function to retrieve a single value from a table
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    # function to bulk insert records
    def bulk_insert(self, query, records):
        self.cursor.executemany(query, records)
        self.connection.commit()
        print("query executed...")

    # function that returns the values of a single attribute
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    def name_placeholder_query(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # function that retrieves a single tuple
    def single_tuple(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # function to update table
    def update_table(self, update_query, new_data):
        self.cursor.executemany(update_query, new_data)
        self.connection.commit()

    # function to delete row from table
    def delete_entry(self, delete_query):
        self.cursor.execute(delete_query)
        self.connection.commit()

    # destructor that closes connection to database
    def destructor(self):
        self.connection.close()
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
        # Creates rider table
        query = '''
        CREATE TABLE riders(
            riderID VARCHAR(22) NOT NULL PRIMARY KEY
        );
        '''
        self.cursor.execute(query)

        # Creates driver table
        query2 = '''
        CREATE TABLE drivers(
            driverID VARCHAR(22) NOT NULL PRIMARY KEY,
            driverRating DOUBLE,
            driverMode VARCHAR(20)
        );
        '''
        self.cursor.execute(query2)

        # Creates ride table
        query3 = '''
        CREATE TABLE rides(
            rideID VARCHAR(22) NOT NULL PRIMARY KEY,
            driverID VARCHAR(22) NOT NULL,
            riderID VARCHAR(22) NOT NULL,
            pickupLocation VARCHAR(40),
            dropoffLocation VARCHAR(40)
        );
        '''
        self.cursor.execute(query3)

        print("Tables Created")

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
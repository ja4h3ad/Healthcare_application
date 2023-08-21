import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
from dotenv import load_dotenv
import os

#  Load the environment variables from .env file
load_dotenv()

class Database:
    '''
    1. class called Database that takes in the necessary connection parameters in the constructor method (init).
    2. two methods: create_database() and create_table().
    3. The create_database() method takes a name parameter and creates a new database with the specified name.
    4. The create_table() method takes a file_path parameter and creates a new table in the specified database with the schema defined in the function. It also inserts the data from the specified CSV file into the new table.
    5. To use this class, create an instance of the Database class and call its create_database() and create_table() methods:'''

    def __init__(self):
        self.host = os.environ.get('DB_HOST')
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self.port = os.environ.get('DB_PORT')
        self.database = os.environ.get('DB_DATABASE')

    def connect(self):
        try:
            conn = mysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conn.is_connected():
                print("Successfully connected to MySQL.")
                return conn
        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None

    def create_database(self, name):
        try:
            conn = mysql.connect(host=self.host, port=self.port, user=self.user, password=self.password)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE {name}")
                print("Database created successfully.")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_patient_table(self, file_path):
        df = pd.read_csv(file_path, index_col=False, delimiter=',')
        print("Port:", self.port)
        try:
            conn = mysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('DROP TABLE IF EXISTS patientData;')
                print('Creating table....')
                cursor.execute(
                    "CREATE TABLE patientData(id INT NOT NULL AUTO_INCREMENT, firstName VARCHAR(50), lastName VARCHAR(500), "
                    "dob DATE, mobileNumber VARCHAR(15), accountNumber VARCHAR(15), streetAddress VARCHAR(30), city VARCHAR(60), "
                    "state VARCHAR(2), postCode VARCHAR (10), createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                    "updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id));")
                print("Table is created....")
                for i,row in df.iterrows():
                    sql = "INSERT INTO patientData (firstName, lastName, dob, mobileNumber, accountNumber, " \
                          "streetAddress, city, state, postCode) " \
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, tuple(row))
                    print("Record inserted")
                    conn.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_doctor_table(self, file_path):
        # read the file into pandas
        df = pd.read_csv(file_path, index_col=False, delimiter=',')
        # Strip double quotes from the specialty column
        df['specialty'] = df['specialty'].str.strip('"')
        print("Port:", self.port)
        try:
            conn = mysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('DROP TABLE IF EXISTS doctorData;')
                print('Creating table....')
                cursor.execute(
                    "CREATE TABLE doctorData(id INT NOT NULL AUTO_INCREMENT, firstName VARCHAR(50), lastName VARCHAR(100), "
                    "specialty VARCHAR(1000), createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                    "updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id));")
                print("Table is created....")
                for i,row in df.iterrows():
                    sql = "INSERT INTO doctorData (firstName, lastName, specialty)" \
                          "VALUES (%s,%s,%s)"
                    cursor.execute(sql, tuple(row))
                    print("Record inserted")
                    conn.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)

    def create_scheduling_table(self):
        try:
            conn = mysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                 database=self.database)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('DROP TABLE IF EXISTS appointments;')
                print('Creating table....')
                cursor.execute(
                    "CREATE TABLE appointments(appointmentId INT NOT NULL AUTO_INCREMENT, patientID INT,"
                    "appointmentDateTime DATETIME, doctorID INT, appointmentType VARCHAR(200), duration VARCHAR(15), "
                    "status VARCHAR(30), reason VARCHAR(60), "
                    "createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                    "updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, "
                    "PRIMARY KEY (appointmentId), "
                    "FOREIGN KEY (patientID) REFERENCES patientData(id), "
                    "FOREIGN KEY (doctorID) REFERENCES doctorData(id));"
                )
                print("Table is created....")
                conn.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)

    def get_patient_appointments(self, patient_id):
        try:
            conn = self.connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM appointments WHERE patientID = %s", (patient_id,)
                )
                appointments = cursor.fetchall()
                return appointments
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()












"""
An app allowing submission and viewership of free social services in Portland.
This app uses an sqlite3 backend to store the data. 

create table soc_services(name text, services text, location text, hours text, phone text, review text)


"""
from datetime import date
from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from soc_services")
        except sqlite3.OperationalError:
            cursor.execute("create table soc_services(name text, services text, location text, hours text, phone text, review text)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: name, services, location, hours, phone, review 
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM soc_services")
        return cursor.fetchall()

    def insert(self, name, services, location, hours, phone, review):
        """
        Inserts entry into database
        :param name: String
        :param services: String
        :param location: String
        :param hours: String
        :param phone: String
        :param review: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'name':name, 'services':services, 'location':location, 'hours':hours, 'phone':phone, 'review':review}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into soc_services (name, services, location, hours, phone, review) VALUES (:name, :services, :location, :hours, :phone, :review)", params)

        connection.commit()
        cursor.close()
        return True

# Imports
from tools.logger import Logger
import sqlite3
import os


class Database:

    def __init__(self, test=False):
        # Vars;
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.location_database_test = (self.scriptDir + os.path.sep + "../files/database/database_test.db")
        self.location_database = (self.scriptDir + os.path.sep + "../files/database/database.db")
        self.test = test
        self.connection = None

        # Objects;
        self.logger = Logger("database", "database.log", "debug")

    def connect(self):
        try:
            if self.test:
                self.connection = sqlite3.connect(self.location_database_test)
            else:
                self.connection = sqlite3.connect(self.location_database)

            # Debug;
            self.logger.print_logger("info", "Connected to database successfully!")

        except sqlite3.Error as error:
            # Debug;
            self.logger.print_logger("error", f"Unable to connect to database! Error: {error}")

            # Set connection to None;
            self.connection = None

        return self.connection

    def execute_query(self, connection, query):
        # Vars;
        cursor = None

        try:
            # Create cursor;
            cursor = connection.cursor()

            # Execute query;
            cursor.execute(query)

            # Commit changes;
            connection.commit()

            # Debug;
            self.logger.print_logger("debug", "Query executed successfully")

        except sqlite3.Error as error:
            # Debug;
            self.logger.print_logger("error", f"Error executing query: {error}")

            # Rollback changes in database connection;
            self.connection.rollback()

        finally:
            cursor.close()

    def select_data(self, query):
        # Vars;
        cursor = None

        try:
            # Create cursor;
            cursor = self.connection.cursor()

            # Execute query;
            cursor.execute(query)

            # Get rows changed;
            rows = cursor.fetchall()

            # Debug;
            self.logger.print_logger("info", f"Selected {len(rows)} rows.")

            return rows

        except sqlite3.Error as error:
            # Debug;
            self.logger.print_logger("error", f"Error selecting query: {error}")

        finally:
            cursor.close()


# if __name__ == "__main__":
#     # Test
#     database = Database()
#     database.connect()

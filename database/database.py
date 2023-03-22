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
            # Rollback changes in database connection;
            self.connection.rollback()

            # Debug;
            self.logger.print_logger("error", f"Error executing query: {error}")

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

    def add_peer(self, ip, port):
        # Vars;
        cursor = None

        try:
            # Create cursor;
            cursor = self.connection.cursor()

            # Checks if the peer database exists, if it doesn't exist, creates it;
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='peers'")

            # Get result;
            result = cursor.fetchone()

            if result is None:
                cursor.execute("CREATE TABLE peers (id INTEGER PRIMARY KEY, ip TEXT, port INTEGER)")

                # Debug;
                self.logger.print_logger("info", "Table 'peers' created successfully")

            # Insert new peer in database;
            cursor.execute(f"INSERT INTO peers (ip, port) VALUES ('{ip}', {port})")

            # Commit changes;
            self.connection.commit()

            # Debug;
            self.logger.print_logger("info", f"Peer {ip}:{port} added successfully")

        except sqlite3.Error as error:
            # Rollback changes in database connection;
            self.connection.rollback()

            # Debug;
            self.logger.print_logger("error", f"Error adding peer: {error}")

        finally:
            cursor.close()

    def remove_peer(self, ip, port):
        # Vars;
        cursor = None

        try:
            # Create cursor;
            cursor = self.connection.cursor()

            # Remove peer with specified ip and port from database;
            cursor.execute(f"DELETE FROM peers WHERE ip = '{ip}' AND port = {port}")

            # Commit changes;
            self.connection.commit()

            # Debug;
            self.logger.print_logger("info", f"Peer {ip}:{port} removed successfully")

        except sqlite3.Error as error:
            # Rollback changes in database connection;
            self.connection.rollback()

            # Debug;
            self.logger.print_logger("error", f"Error removing peer: {error}")

        finally:
            cursor.close()

    def select_peer(self, ip, port):
        # Vars;
        cursor = None

        try:
            #  Selects the peer with the specified ip and port of the database;
            cursor = self.connection.cursor()

            # Checks if the peer database exists, if it doesn't exist, creates it;
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='peers'")

            # Get result;
            result = cursor.fetchone()

            if result is not None:
                cursor.execute(f"SELECT * FROM peers WHERE ip = '{ip}' AND port = {port}")
                row = cursor.fetchone()

                # Verify if peer exists;
                if row is not None:
                    # print(f"Peer {ip}:{port} found")
                    return True
                else:
                    # print(f"Peer {ip}:{port} not found")
                    return False

            else:
                return False

        except sqlite3.Error as error:
            self.logger.print_logger("error", f"Error selecting peer: {error}")

        finally:
            cursor.close()


# if __name__ == "__main__":
#     # Test
#     database = Database()
#     database.connect()

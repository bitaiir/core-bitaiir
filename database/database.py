# Imports
import sqlite3
import sys
import os


class Database:

    def __init__(self):

        # Vars;
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.locationDB_Test = (self.scriptDir + os.path.sep + "../user/database/database_test.db")
        self.locationDB = (self.scriptDir + os.path.sep + "../user/database/database.db")

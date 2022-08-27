import os
import sqlite3


class DBClient:
    def __init__(self):
        self.cconn = sqlite3.connect(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "/db/comps.db")
        )
        self.gconn = sqlite3.connect(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "/db/guilds.db")
        )
        self.comps_cur = self.cconn.cursor()
        self.guilds_cur = self.gconn.cursor()

database = DBClient()
import sqlite3
from settings import dbfile


class Database(object):
    """ DB initialization """
    def __init__(self, database=dbfile):
        self.cursor = None
        self.connection = None
        self.connected = False
        self.print = False
        self.database = database

    def __enter__(self):
        pass

    def connect(self):
        """Connects to DB"""
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connected = True

    def close(self):
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def execute(self, query=None):
        output = None
        if not query:
            return "No query specified"
        if not self.connected:
            self.connect()
        try:
            output = self.cursor.execute(query).fetchall()
        except sqlite3.Error as e:
            print("Error encountered: {}".format(e.args[0]))
            print("Running query: {}".format(query))
        if self.print:
            for row in output:
                print(row)
        else:
            return output

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def instance_and_run(query):
    dbo = Database()
    with dbo:
        out = dbo.execute(query)
    return out


def get_affix_from_id(affix_id):
    affix_id = int(affix_id)
    query = "SELECT * FROM affixes WHERE affix_id = '{}'".format(affix_id)
    return instance_and_run(query)


def get_affix_from_effect(effect_simple):
    query = "SELECT * FROM affixes WHERE effect_simple = '{}'".format(effect_simple)
    return instance_and_run(query)


def get_affix_all():
    query = "SELECT * FROM affixes"
    return instance_and_run(query)


def get_currency_list():
    query = "SELECT * FROM currencies"
    return instance_and_run(query)

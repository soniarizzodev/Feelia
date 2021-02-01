import sqlite3 as sql
import logging

from webapp.const import SQL_DB


class DBManager():
    """SQLite3 DB Managemant Interface

    Attributes
        db      Database object
        cursor  Database cursor
    """

    def __init__(self):
        self.db = None
        self.cursor = None

    def open(self):
        """ Open a new DB connection
        """
        self.db = sql.connect(SQL_DB)
        self.cursor = self.db.cursor()
        logging.info("DB - OPEN")

    def insert(self, query, values):
        """Insert a new row

        Params
            query(string)   Insert query
            value(tuple)    Insert query parameter

        Return
            (result (boolean), Error (string))
        """

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            logging.info("DB - QUERY EXECUTED")
            return (True, "")
        except Exception as error:
            self.db.close()
            logging.error("DB - QUERY (INSERT) FAILED")
            return(False, "Query Failed! Error:{}".format(str(error)))
        finally:
            self.db.close()
            logging.info("DB - CLOSE")

    def select(self, query, values):
        """Select rows by parameter

        Params
            query(string)   Select query
            value(tuple)    Select query parameter

        Return
            selected rows
        """

        try:
            self.cursor.execute(query, values)
            logging.info("DB - QUERY (SELECT) EXECUTED")
            return self.cursor.fetchall()
        except Exception as error:
            self.db.close()
            logging.error("DB - QUERY FAILED {}".format(str(error)))
            return []
        finally:
            self.db.close()
            logging.info("DB - CLOSE")

    def delete(self, query, values):
        """Delete a row

        Params
            query(string)   Delete query
            value(tuple)    Delete query parameter

        Return
            (result (boolean), Error (string))
        """

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            logging.info("DB - QUERY (DELETE) EXECUTED")
            return (True, "")
        except Exception as error:
            self.db.close()
            logging.error("DB - QUERY FAILED {}".format(str(error)))
            return (False, "QueryFailed! Error:{}".format(str(error)))
        finally:
            self.db.close()
            logging.info("DB - CLOSE")

    def update(self, query, values):
        """Update a row

        Params
            query(string)   Update query
            value(tuple)    Update query parameter

        Return
            (result (boolean), Error (string))
        """

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            logging.info("DB - QUERY (UPDATE) EXECUTED")
            return (True, "")
        except Exception as error:
            self.db.close()
            logging.error("DB - QUERY FAILED {}".format(str(error)))
            return (False, "QueryFailed! Error:{}".format(str(error)))
        finally:
            self.db.close()
            logging.info("DB - CLOSE")



    def close(self):
        """Close DB connection
        """
        self.db.close()
        logging.info("DB - CLOSE")


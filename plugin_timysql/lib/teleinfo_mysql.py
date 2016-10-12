#!/usr/bin/python3
# -*-coding:Utf-8 -*

import sys
import pymysql

class MysqlConnectCfg():
    ### config database access ###

    def __init__(self):
        self._host="localhost"
        self._login="teleinfo_ro"
        self._pwd="teleinforeadonly"
        self._dbname="teleinfo"
        self._tablename="teleinfo"

    def __repr__(self):        
        isDbPwdSet = self._pwd is not ""
        msg = "db.host(\"{}\"), db_login(\"{}\", " + \
                "db_pwd_isSet(\"{}\"), db_dbname(\"{}\") " + \
                "db_tablename(\"{}\")" \
                .format(self._host, self._login, isDbPwdSet, self._dbname, self._tablename)
        return msg

    def _get_host(self):
        return self._host

    def _get_login(self):
        return self._login

    def _get_pwd(self):
        return self._pwd

    def _get_dbname(self):
        return self._dbname

    def _get_tablename(self):
        return self._tablename

    # creating property (getter)
    host = property(_get_host)
    login = property(_get_login)
    pwd = property(_get_pwd)
    dbname = property(_get_dbname)
    tablename = property(_get_tablename)



class TeleinfoMysql():

    ### global var ###
    #db = pymysql.connections.Connection
    def __init__(self):
        print("Init of class TeleinfoMysql()")
        
        self.dbcfg = MysqlConnectCfg();        
        self.dbcon = self.mysql_connect()


    def __del__(self):
        """ Need to disconnect from Mysql when closing !"""
        print("Destruct. of TeleinfoMysql()")
        self.mysql_disconnect()


    def mysql_connect(self):
        """ try to connect to mysql database with given config """

        print("Testing MySQL connection...",  end ="")
        try:
            db = pymysql.connect(self.dbcfg.host, self.dbcfg.login, self.dbcfg.pwd, self.dbcfg.dbname)
        except pymysql.err.OperationalError as emsg:
            print("\n\n######### ERROR DURING CONNECTION TO MYSQL DB  #########")
            print(emsg)
            sys.exit(1)
        else:
            print(" success :-)")
            return db


    def mysql_disconnect(self):
        """ Disconnect from mysql database """

        print("Disconnecting from MYSQL server... ", end="")
        try:
            self.dbcon.close()
        except Exception as e:
            print("\n\n!!! Error while disconnecting from DB server !!!")
            print(e)
        else:
            print("success :-)")


    def fetch_last_teleinfo_line(self):
        """ Select the last entry in teleinfo table """
        db_table = self.dbcfg.tablename
        nb_row = "1"

        sql = "SELECT * FROM " +  db_table + \
                " ORDER BY TIMESTAMP DESC LIMIT " + nb_row
        cursor = self.dbcon.cursor()

    #    msg = "Try to fetch the l
        print("Trying to fetch the " + nb_row + " row(s) in " + \
                str(db_table) + " table...", end="")
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            print("\n\n######### ERROR WHILE FETCHING DATA #########")
            print(e)
            sys.exit(1)
        else:
            print(" success :-)")
            return results


if __name__ == "__main__":
    print("Test execution timysql")
    t = TeleinfoMysql()
    sql_res = t.fetch_last_teleinfo_line()

    cur_row = sql_res[0]

    timestamp = cur_row[0]
    rec_date = cur_row[1]
    rec_time = cur_row[2]
    optarif = cur_row[3]
    hchp = cur_row[4]
    hchc = cur_row[5]
    ptec = cur_row[6]
    inst1 = cur_row[7]
    imax1 = cur_row[8]
    papp = cur_row[9]

    print("\n------------------- RESULT ------------------------")
    print("\tThe last rec_date is " + str(rec_date) + " " + str(rec_time))
    print("---------------------------------------------------\n")

    # Fetch a single row using fetchone() method.
    #data = cursor.fetchone()


    # disconnect from server
    del t
    #    mysql_disconnect(db)
    #db.close()


    sys.exit(0)

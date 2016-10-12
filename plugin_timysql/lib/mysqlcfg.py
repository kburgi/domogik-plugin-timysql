#!/usr/bin/python3
# -*-coding:Utf-8 -*

class MysqlConnectCfg():
    """ Mysql database access config """

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


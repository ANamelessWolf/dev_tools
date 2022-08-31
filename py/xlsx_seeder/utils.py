import json
import re
from os.path import exists

def get_connection_string(connection):
    f = open('settings.json', encoding='utf-8')
    data = json.load(f)
    conn_string = None
    if connection in data["connections"]:
        dbname = data["connections"][connection]["dbName"]
        user = data["connections"][connection]["user"]
        password = data["connections"][connection]["password"]
        host = data["connections"][connection]["host"]
        port = data["connections"][connection]["port"]
        conn_string = "dbname=%s user=%s password=%s host=%s port=%s" % (dbname, user, password,host, port)
    return conn_string

def get_table(table_name):
    if(not exists('tables\\' + table_name + '.json')):
        raise Exception("No existe configuración para la tabla " + table_name)
    f = open('tables\\' +table_name+ '.json', encoding='utf-8')
    data = json.load(f)
    return data

def words_only(value):
    return re.sub(r'[^a-zA-Z]', '', value)

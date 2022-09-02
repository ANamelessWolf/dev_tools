import json
import os
import re
from tqdm import tqdm
from openpyxl import load_workbook
from os.path import exists
from unittest import result

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

def load_excel(file, table):
    if not exists(file):
        raise Exception("No existe el archivo en la ruta; " + file)
    extension = get_extension(file)
    if extension not in ["XLSX"]:
        raise Exception("Al parecer el archivo '" + file + "' no es un archivo de Excel(XLSX) válido")
    try:
        wb = load_workbook(file, read_only=True)
        ws = wb.get_sheet_by_name(wb.sheetnames[0])
        data = {}
        cols = []
        columns = list(table["map"].keys())
        for r in tqdm(ws.iter_rows(), "Leyendo Excel.."):
            if r[0].row == 1:
                for colIndex in range(len(r)):
                    if r[colIndex].value in columns:
                        cols.append(colIndex)
                        data[colIndex] = []
            else:
                for colIndex in cols:
                    data[colIndex].append(r[colIndex].value)
        return data
    except Exception as e:
        raise Exception("Error al leer el archivo: "+ str(e))

def get_table(table_name):
    if not exists('tables\\' + table_name + '.json'):
        raise Exception("No existe configuración para la tabla " + table_name)
    f = open('tables\\' +table_name+ '.json', encoding='utf-8')
    data = json.load(f)
    return data

def table_exists(data, cursor):
    table_name = data['table']
    sql = "SELECT column_name FROM information_schema.columns WHERE table_name='" + table_name +"'"
    cursor.execute(sql)
    records = cursor.fetchall()
    flag = True if len(records) > 0 else False
    result = flag, records
    return result

def create_table(data, cursor):
    table_name = data['table']
    sql = "CREATE TABLE " + table_name + " ($fields$)"
    fields = []
    for field in data['fields']:
       fields.append(field +" "+ (data['fields'][field]['type']+"("+str(data['fields'][field]['length'])+")" if data['fields'][field]['length'] is not None else data['fields'][field]['type']) + ( " NULL " if data['fields'][field]['nullabe'] else " NOT NULL" ))
    field = ", ".join(fields)
    sql = sql.replace('$fields$', field)
    cursor.execute(sql)
    # Se obtienen las columnas
    sql = "SELECT column_name FROM information_schema.columns WHERE table_name='" + table_name +"'"
    cursor.execute(sql)
    records = cursor.fetchall()
    return records

def drop_table(data, cursor):
    table_name = data['table']
    sql = "DROP TABLE " + table_name 
    cursor.execute(sql)

def truncate_table(data, cursor):
    table_name = data['table']
    sql = "TRUNCATE TABLE " + table_name 
    cursor.execute(sql)

def validate_table(data, records, cursor):
    cols = list(map(lambda x: x[0], records))
    missing =[]
    for field in data['fields']:
        if field not in cols:
            missing.append(field)
    if len(missing) > 0:
        drop_table(data, cursor)
        create_table(data, cursor)

def words_only(value):
    return re.sub(r'[^a-zA-Z]', '', value)

def get_extension(file):
    split = os.path.splitext(file)
    if len(split)>1:
        extension = split[1].upper()[1:]
    else:
        raise Exception("El archivo '"+file+"' no tiene extensión")
    return extension

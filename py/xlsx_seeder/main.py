import psycopg2
import json
import utils
connection = 'development'
table = 'RegistrosLeenRechazo'
file = "C:\\Users\\miguel.alanis\\Desktop\\Migracion EXcel\\Inmuebles validados LEEN - 23.08.22.xlsx"

try:
    table = utils.get_table('RegistrosLeenRechazo')

    conn_string = utils.get_connection_string(connection)
    if conn_string is None:
        raise Exception("En el archivo de settings.json, no existe la conexión '" + connection + "'")
    conn = psycopg2.connect(conn_string)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM c002_entidad")
        records = cur.fetchall()
    print(records)
except Exception as e:
    print(e[0])

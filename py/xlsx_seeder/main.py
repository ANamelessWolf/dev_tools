import psycopg2
from tqdm import tqdm
import utils
connection = 'development'
table = 'RegistrosLeenRechazo'
file = "C:\\Users\\miguel.alanis\\Desktop\\Migracion EXcel\\Inmuebles validados LEEN - 23.08.22.xlsx"
batchSize = 100

try:
    table = utils.get_table('RegistrosLeenRechazo')

    conn_string = utils.get_connection_string(connection)
    if conn_string is None:
        raise Exception("En el archivo de settings.json, no existe la conexión '" + connection + "'")

    #Se extrae la data del Excel
    excelData = utils.load_excel(file, table)
    if len(excelData.keys()) != len(table["map"].keys()):
        raise Exception("Las columnas mapeadas no coinciden con el archivo de mapeo")

    #Envio a la base de datos    
    conn = psycopg2.connect(conn_string)
    with conn.cursor() as cur:
        try:
            #Se obtienen los registros de la tabla destino, si no existe se crea
            exists, records = utils.table_exists(table, cur)
            if not exists:
                records = utils.create_table(table, cur)
            else:
                utils.validate_table(table, records, cur)
                utils.truncate_table(table)
            #Se construye el insert
            values = []
            columns = list(excelData.keys())
            row_count = range(0, len(excelData[columns[0]]))
            for index in tqdm(row_count, desc="Creando insert values"):
                row = list(map(lambda x: '' if excelData[x][index] is None else excelData[x][index], columns))
                values.append("('" + "', '".join(row) + "')")
                if len(values)== batchSize:
                    print(values)
            conn.commit()
        except Exception as e:
            conn.rollback()

    print(records)
except Exception as e:
    print(e[0])

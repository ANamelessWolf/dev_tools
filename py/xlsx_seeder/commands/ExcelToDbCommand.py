from commands.BaseCommand import BaseCommand
import utils

class ExcelToDbCommand(BaseCommand):

    @property
    def Connection(self):
        """Devuelve el nombre de la conexión actual
        """
        return self._Connection

    @Connection.setter
    def Connection(self, value):
        """Establece el valor de la conexión actual
        Args:
            value (string): El valor asignar
        """
        self._Connection = value    

    @property
    def TableDefinition(self):
        """Devuelve el nombre de la definición de tabla a usar
        """
        return self._TableDefinition

    @TableDefinition.setter
    def TableDefinition(self, value):
        """Establece el nombre de la tabla de definición
        Args:
            value (string): El valor asignar
        """
        self._TableDefinition = value 

    @property
    def BatchSize(self):
        """Devuelve el tamaño del batch usado para insertar
        """
        return self._BatchSize

    @BatchSize.setter
    def BatchSize(self, value):
        """Establece el nombre de la tabla de definición
        Args:
            value (int): El tamaño del batch para insertar
        """
        self._BatchSize =  int(value)

    @property
    def ExcelFile(self):
        """Devuelve la ruta del archivo a exportar
        """
        return self._ExcelFile

    @ExcelFile.setter
    def ExcelFile(self, value):
        """Establece la ruta del archivo a exportar
        Args:
            value (file): La ruta del archivo a exportar
        """
        self._ExcelFile = value                

    def run(self):
        try:
            #1: Se obtiene la definición de la tabla a exportar
            table = utils.get_table(self.TableDefinition)
            #2: Se extraen los datos del Excel
            excelData = utils.load_excel(self.ExcelFile, table)
            #3: Se revisa que el excel coincida con la definición de la tabla
            if len(excelData.keys()) != len(table["map"].keys()):
                raise Exception("Las columnas mapeadas no coinciden con el archivo de mapeo")
            #4: Se envian los datos a la base de datos
            conn = utils.get_connection(self.Connection)
            with conn.cursor() as cur:
                try:
                    #4.1: Se obtienen los registros de la tabla destino
                    exists, records = utils.table_exists(table, cur)
                    #4.2: Si no existe la tabla se crea
                    if not exists:
                        records = utils.create_table(table, cur)
                    else:
                        #4.3: Se valida la tabla existente contra la definición de la tabla
                        utils.validate_table(table, records, cur)
                        #4.4: Se limpia la tabla
                        utils.truncate_table(table, cur)
                    #4.5: Se inserta el excel en la base de datos
                    utils.insert(table, excelData, self.BatchSize, cur)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
        except Exception as e:
            print(e.args[0])
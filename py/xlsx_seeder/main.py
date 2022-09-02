import sys
import time
from datetime import timedelta
from commands.BaseCommand import BaseCommand
from commands.ExcelToDbCommand import ExcelToDbCommand
sys.argv = ["", "export", "-c", "development", "-t", "RegistrosLeenRechazo", "-b", "100", "-f", "C:\\Users\\miguel.alanis\\Desktop\\Migracion EXcel\\Inmuebles validados LEEN - 23.08.22.xlsx"]

argLen = len(sys.argv)
cmd = " ".join(sys.argv)

start = time.time()

try:
    cmd = None
    #1: Selecciona un comando
    if sys.argv[1] == "export":
        cmd = ExcelToDbCommand()
        cmd.Connection = BaseCommand.get_parameter(sys.argv, "-c")
        cmd.TableDefinition = BaseCommand.get_parameter(sys.argv, "-t")
        cmd.BatchSize = BaseCommand.get_optional_parameter(sys.argv, "-b", 100)
        cmd.ExcelFile = BaseCommand.get_parameter(sys.argv, "-f")
    else:
        raise Exception("Comando incorrecto")
    #2: Ejecuta el commando
    if cmd is not None:
        cmd.run()
except Exception as e:
    print(str(e))

end = time.time()
sec = (end - start)
td = timedelta(seconds=sec)
print("Tiempo de ejecución " + str(td) + ", proceso finalizado.")

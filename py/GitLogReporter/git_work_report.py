from ast import Try
from fileinput import filename
import sys
from GitReport import GitReport

#Example
#filename = r'D:\01MAAM\dev\py\GitWorkReport\log.txt'
try:
    if len(sys.argv)<2:
        raise Exception("No se proporciono la ruta del archivo log")        
    elif len(sys.argv)<3:
        raise Exception("No se proporciono ninguna tarea")
    else:
        task = sys.argv[1]
        reportname = sys.argv[2]
        report = GitReport(filename, reportname)
        if task == "-ls":
            report.process()
            report.list_users()
        elif task == "-ru":
            if len(sys.argv)<4:
                raise Exception("No se proporciono el nombre del reporte")
            username = sys.argv[3]
            report = GitReport(filename, reportname)
            report.save(username)
        elif task == "-ra":
            report = GitReport(filename, reportname)
            report.save_all()
except Exception as e:
    print(e)
    print(GitReport.list_commands())

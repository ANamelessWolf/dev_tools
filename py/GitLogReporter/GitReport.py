from sympy import content
from GitEntry import GitEntry
from GitAuthorReport import GitAuthorReport

class GitReport:

    def __init__(self, logPath, reportPath):
        self.log_path = logPath
        self.report_path = reportPath
        self.content = {}
        self.authors = []

    def __report_block(self, block):
        return GitEntry(block)

    def append(self, entry):
        username, email = entry.get_author()
        if username not in self.authors:
            author = GitAuthorReport(entry)
            self.authors.append(username)
            self.content[username] = author
        else:
            self.content[username].add_entry(entry)
        
    def process(self):
        #1: Read file
        with open(self.log_path, encoding='utf8') as file:
            lines = file.readlines()
            #2: Process file
            block = []
            for line in lines:
                if 'commit' in line:
                    block.append(line)
                    entry = self.__report_block(block)
                    if entry.is_valid():
                        self.append(entry)
                    block = []
                else:
                    block.append(line)
        #2: Se guarda la última entrada
        if len(block)>1:
            entry = self.__report_block(block)
            if entry.is_valid():
                self.append(entry)

    def list_users(self):
        for author in self.authors:
            print(author)

    def save(self, author):
        if author in self.authors:
            data = self.content[author]
            with open(self.report_path, 'w', encoding='utf8') as file:
                file.write(data.report())
        else:
            print("No se encontro el usuario: {}".format(author))

    def save_all(self):
        content = "# Reporte todos los usuarios\n\n"
        with open(self.report_path, 'w', encoding='utf8') as file:
            for author in self.authors:
                data = self.content[author]
                content += data.report()
            else:
                print("No se encontro el usuario: {}".format(author))
            file.write(content)

    def list_commands():
        msg = [
            "Lista de comandos disponibles:",
            "git_work_report -ls <log_path>\tLista los nombres de usuarios contenidos en el archivo de git log",
            "git_work_report -ru <log_path> <user_name>\tImprime el reporte de commits del usuario dado en formato md",
            "git_work_report -ra <log_path>\tImprime el reporte de todos los commits agrupados por usuarios en un formato md",
        ]
        return "\n\n".format(msg)

    def get_short_demo():
        return 'assets\\log_short.txt'

    def get_short_demo():
        return 'assets\\log.txt'
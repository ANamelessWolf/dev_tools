class GitAuthorReport:

    def __init__(self, entry):
        self.username, self.email = entry.get_author()
        self.author = entry.author
        self.entries = []
        self.add_entry(entry)

    def add_entry(self, entry):
        self.entries.append(entry)

    def report(self):
        report ="## Commits de "+ self.username+"\n\n"
        report +="**Correo:** " + self.email+"\n\n"
        report +="|commit|fecha|descripción|\n"
        report +="|---|---|---|\n"
        for entry in self.entries:
            report+= "{}\n".format(entry.report())
        return report
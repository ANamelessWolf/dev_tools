from dateutil.parser import parse

class GitEntry:

    def __init__(self, block):
        self.commit = ""
        self.author = ""
        self.date = ""
        self.merge = ""
        self.detail = ""
        detail = []
        if len(block)>0:
            for line in block:
                if 'commit' in line:
                    self.commit = self.__clean_line(line.split("commit", 1)[1])
                elif 'Author:' in line:
                    self.author = self.__clean_line(line.split("Author:", 1)[1])
                elif 'Date:' in line:
                    self.date = self.__clean_line(line.split('Date:', 1)[1])
                    self.date = self.__parse_date(self.date)
                elif 'Merge:' in line:
                    self.merge = self.__clean_line(line.split('Merge:', 1)[1])
                else:
                    line = self.__clean_line(line)
                    if len(line) > 0:
                        detail.append(line)
            self.detail = '<br>'.join(detail)

    def is_valid(self):
        return len(self.author) > 0

    def report(self):
        time = self.date.strftime("%d/%m/%Y, %H:%M:%S")
        report = "|{}|{}|{}|".format(self.commit, time, self.detail)
        return report

    def get_author(self):
        return self.author.split(' <')[0], self.author.split(' <')[1].replace('>',"")

    def __clean_line(self, line):
        return line.strip().replace("\n", "").replace("\r", "")

    def __parse_date(self, dateStr):
        dt = parse(dateStr)
        return dt

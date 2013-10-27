__author__ = 'Jacques Supcik'

# Caveats: This is a just a quick and dirty way to generate the list of
# all keywords for the ARM Assembler

import yaml
import re
from jinja2 import Environment, FileSystemLoader

class KeywordList:

    result = set()

    def __init__(self, data):
        self.result = set()
        self.data = data

    def add(self, instruction):
        m = re.search(r'<(\w+)>', instruction)
        if m:
            x = m.group(1)
            for i in self.data[x]:
                self.add(re.sub(r'<' + x + '>', i, instruction, count=1))
            return

        m = re.search(r'\{(\w+)\}', instruction)
        if m:
            x = m.group(1)
            self.add(re.sub(r'\{' + x + '\}', '', instruction, count=1))
            for i in self.data[x]:
                self.add(re.sub(r'\{' + x + '\}', i, instruction, count=1))
            return

        self.result.add(instruction)

    def add_all(self, list):
        for i in list:
            self.add(i)

    def output(self, prefix):
        out = ""
        line = prefix
        kw = sorted(list(self.result))
        for i in range(0, len(kw)):
            if len(line) + len(kw[i]) + 2 < 78:
                line = line + kw[i].lower()
                if i < len(kw)-1:
                    line += ","
            else:
                line += " " * (78 - len(line))
                out = out + line + "%\n"
                line = "      " + kw[i].lower()
                if i < len(kw)-1:
                    line += ","

        out = out + line + "},%"
        return(out)


data = yaml.load(open("arm.yaml"))

keywords = KeywordList(data);
keywords.add_all(data['instructions'])
k1 = keywords.output('   {morekeywords={')

keywords2 = KeywordList(data);
keywords2.add_all(data['directives'])
k2 = keywords2.output('    morekeywords=[2]{')

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('lstlangarm.jinja2')
f = open("lstlangarm.sty", mode="w")
f.write(template.render(keywords=k1, keywords2=k2))
f.close()
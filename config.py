from utilpy.file import File
from utilpy.regex import Regex

class Config:

    def __init__(self, fileName:str):
        self.item = dict()

        r = Regex(r'[ \t]*([a-zA-Z0-9-]*)[ \t]*=[ \t]*([a-zA-Z0-9-+*\/=?!@#$%&()_{}\[\]<>:;,.~^`"\' ]*)[ \t]*')

        for m in r.getMatches(File(fileName).read()):
            self.item[m[1]] = m[2]

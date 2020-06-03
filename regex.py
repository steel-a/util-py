import re

class Regex:

    def __init__(self, pattern:str):
        self.pattern = pattern

    def getMatches(self, text:str):
        lst = re.findall('('+self.pattern+')', text)
        if lst != []:
            if isinstance(lst[0],tuple):
                return lst
            else:
                lst2 = []
                for e in lst:
                    lst2.append((e,))
                return lst2
        return lst

    def getValue(self, text:str, i:int=0):
        match = re.match(self.pattern, text)
        if match is not None:
            try:
                return match[i]
            except:
                return None
        return None

import re

def getMatches(pattern:str, text:str):
    lst = re.findall(pattern, text)
    if lst != []:
        if isinstance(lst[0],tuple):
            return lst
        else:
            lst2 = []
            for e in lst:
                lst2.append([e])
            return lst2
    return lst

def getValue(pattern:str, text:str, i:int=0):
    match = re.match(pattern, text)
    if match is not None:
        try:
            return match[i]
        except:
            return None
    return None

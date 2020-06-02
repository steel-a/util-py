import re

def getMatches(pattern:str, text:str):
    return re.findall(pattern, text)

def getValue(pattern:str, text:str, i:int=0):
    match = re.match(pattern, text)
    if match is not None:
        try:
            return match[i]
        except:
            return None
    return None

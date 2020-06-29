def isOneOfThisWordsOnString(wordList:str, string:str, separator:str=';')->bool:
    '''
    If one word of wordList is in string, return True, else return False
    '''
    for word in wordList.split(separator):
        if word in string:
            return True
    return False
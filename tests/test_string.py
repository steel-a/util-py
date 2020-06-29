from utilpy.string import isOneOfThisWordsOnString

def test_string():

    assert isOneOfThisWordsOnString('book;cat;dog;egg;table','the book is on the table') == True
    assert isOneOfThisWordsOnString('book;cat;dog;egg;table','the baak is on the tabla') == False


if __name__ == '__main__':
    test_string()
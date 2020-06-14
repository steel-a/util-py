from utilpy.file import File

def test_file():

    try: File('notExist.txt').read()
    except: pass
    
    f = File('I tried to open the file [notExist.txt] here.txt')
    assert f.exists() == True
    f.remove()
    assert f.exists() == False


    f = File('test.txt')
    f.write('test text!\ntest text2!')
    assert f.isClose() == False
    f.close()
    assert f.isClose() == True

    assert f.exists() == True
    assert f.exists('test.txt') == True
    assert f.exists('tests2.txt') == False
    assert f.isClose() == True

    f = File('test.txt')
    lines = f.readLines()
    assert lines[0] == 'test text!\n'
    assert lines[1] == 'test text2!'
    assert f.isClose() == True


    f = File('test.txt')
    assert f.read() == 'test text!\ntest text2!'
    assert f.isClose() == True

    f.remove()
    assert f.exists('test.txt') == False




if __name__ == '__main__':
    test_file()
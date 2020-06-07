from utilpy.config import Config
from utilpy.file import File

def test_config():

    f = File('test.ini')
    f.write('connectionString = Server=localhost;Port=3306;Database=test;Uid=root;Pwd=49rjfdklfkdfj#(*$*(%&$*%)%*$&@)(%(#)#&&@&!*~);\nconnectionString2=fsojojdojsojsoijsfijfs=dsfsfssffs=')
    f.close()

    c = Config('test.ini')
    assert c.item['connectionString'] == 'Server=localhost;Port=3306;Database=test;Uid=root;Pwd=49rjfdklfkdfj#(*$*(%&$*%)%*$&@)(%(#)#&&@&!*~);'
    assert c.item['connectionString2'] == 'fsojojdojsojsoijsfijfs=dsfsfssffs='



if __name__ == '__main__':
    test_config()
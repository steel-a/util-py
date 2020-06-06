from utilpy.config import Config
from utilpy.file import File

def test_config():

    f = File('test.ini')
    f.write('connectionString = Server=localhost;Port=3306;Database=test;Uid=root;Pwd=49rjfdklfkdfj#(*$*(%&$*%)%*$&@)(%(#)#&&@&!*~);\nconnectionString2=fsojojdojsojsoijsfijfs=dsfsfssffs=')
    f.close()

    c = Config('test.ini')
    assert c.config['connectionString'] == 'Server=localhost;Port=3306;Database=test;Uid=root;Pwd=49rjfdklfkdfj#(*$*(%&$*%)%*$&@)(%(#)#&&@&!*~);'
    assert c.config['connectionString2'] == 'fsojojdojsojsoijsfijfs=dsfsfssffs='
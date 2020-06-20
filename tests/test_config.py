from utilpy.config import Config
from utilpy.file import File

def test_config():

    f = File('test.ini')
    f.write('connectionString = ABCDEF;\nconnectionString2=123456=')
    f.close()

    c = Config('test.ini')
    assert c.item['connectionString'] == 'ABCDEF;'
    assert c.item['connectionString2'] == '123456='

    File('test.ini').remove()

if __name__ == '__main__':
    test_config()
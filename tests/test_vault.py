from utilpy.vault import Vault
from utilpy.file import File

def test_vault():
    v = Vault('test.db')
    f = File('test.db')

    assert f.exists() == True
    v.put('a','a1','a2')
    v.put('b','b1','b2')
    k = v.get('a')
    assert (k[0] == 'a1' and k[1] == 'a2')
    v.put('a','a3','a4')
    k = v.get('a')
    assert (k[0] == 'a3' and k[1] == 'a4')
    k = v.get('c')
    assert k == None

    f.remove()

if __name__ == '__main__':
    test_vault()
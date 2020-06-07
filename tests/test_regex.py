from utilpy.regex import Regex

def test_regex():
    pattern = '([0-9]*) (results)'
    text = '123 results, 234 results'

    r1  = Regex(pattern)
    lst = r1.getMatches(text)
    assert lst[0][0] == '123 results'
    assert lst[0][1] == '123'
    assert lst[0][2] == 'results'
    assert lst[1][0] == '234 results'
    assert lst[1][1] == '234'
    assert lst[1][2] == 'results'


    r2 = Regex('[0-9]{3}')
    lst = r2.getMatches(text)
    assert lst[0][0] == '123'
    assert lst[1][0] == '234'

    lst = r1.getMatches('aaaaaaaaaa')
    assert lst == []

    assert r1.getValue(text) == '123 results'
    assert r1.getValue(text,1) == '123'
    assert r1.getValue(text,2) == 'results'
    assert r1.getValue(text,3) is None
    assert r1.getValue('aaaaaaaaaaa') is None


if __name__ == '__main__':
    test_regex()
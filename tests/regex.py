import utilpy.regex as regex

def test_regex():
    pattern = '([0-9]*) (results)'
    text = '123 results, 234 results'

    lst = regex.getMatches(pattern, text)
    assert lst[0][0] == '123'
    assert lst[0][1] == 'results'
    assert lst[1][0] == '234'
    assert lst[1][1] == 'results'

    lst = regex.getMatches('[0-9]{3}', text)
    assert lst[0][0] == '123'
    assert lst[1][0] == '234'

    lst = regex.getMatches(pattern, 'aaaaaaaaaa')
    assert lst == []

    assert regex.getValue(pattern, text) == '123 results'
    assert regex.getValue(pattern, text,1) == '123'
    assert regex.getValue(pattern, text,2) == 'results'
    assert regex.getValue(pattern, text,3) is None
    assert regex.getValue(pattern, 'aaaaaaaaaaa') is None



import utilpy.numbers as numbers

def test_toFloat():
    # function toFloat
    for s in ('1,000,000,000.765','1000000000.765','1.000.000.000,765', '1000000000,765'):
        assert numbers.toFloat(s) == 1000000000.765

    for s in ('1,000.765','1000.765','1.000,765', '1000,765'):
        assert numbers.toFloat(s) == 1000.765

    for s in ('1,000,000,000.76','1000000000.76','1.000.000.000,76', '1000000000,76'):
        assert numbers.toFloat(s) == 1000000000.76

    for s in ('1,000,000,000.7','1000000000.7','1.000.000.000,7','1000000000,7'):
        assert numbers.toFloat(s) == 1000000000.7

    for s in ('1,000,000,000','1.000.000.000','1000000000'):
        assert numbers.toFloat(s) == 1000000000

    assert numbers.toFloat('10') == 10
    assert numbers.toFloat('1,1') == 1.1
    assert numbers.toFloat('1.0') == 1.0
    assert numbers.toFloat('1,11') == 1.11
    assert numbers.toFloat('1.01') == 1.01

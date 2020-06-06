from utilpy.date import Date

def test_date():
    assert Date('11/03/2020').toString() == '2020-03-11'
    assert Date('11/03/2020 22:10:37', timeFormat='%H:%M:%S').toString() == '2020-03-11'
    assert Date('11/03/2020 22:10:37', timeFormat='%H:%M:%S').toString('%Y-%m-%d %H:%M:%S') == '2020-03-11 22:10:37'
    assert Date('03/11/2020 22:10:37', language='en', timeFormat='%H:%M:%S').toString('%Y-%m-%d %H:%M:%S') == '2020-03-11 22:10:37'


from utilpy.execControl import ExecControl

def test_execControl():
    ec = ExecControl("user='root', password='dff8989(*6gF%Gdiud*(7%GgHgIiu67565665%T^&76GGHD6565IHjLKJhHhjkui87656434321890*(*7w',host='172.30.192.1', port='33062',database='tests'",
                'TableCtl_Test', 1)
    ec._dropTableCtrl()
    ec._createTableCtrl()
    ec._createNewRegister('test')
    ec.getProcessToExec()
    assert ec.processName == 'test'
    assert ec.id == 1
    assert ec.statusLastExecution == 'P'
    assert ec.triesWithError == 0
    ec.updateError('Er mess')
    assert ec.statusLastExecution == 'E'
    assert ec.triesWithError == 1
    ec.getProcessToExec()
    assert ec.statusLastExecution == 'P'
    assert ec.triesWithError == 1
    assert ec.error == 'Er mess'
    ec.updateError('Er mess2')
    assert ec.statusLastExecution == 'E'
    assert ec.triesWithError == 2
    ec.getProcessToExec()
    assert ec.statusLastExecution == 'P'
    assert ec.triesWithError == 2
    assert ec.error == 'Er mess2'
    ec.updateSuccess(5,7)
    assert ec.statusLastExecution == 'S'
    assert ec.triesWithError == 0
    assert ec.error == ''
    assert ec.numHardRegistersLast == 0
    assert ec.numHardRegisters == 5
    assert ec.numSoftRegisters == 7

    ec._dropTableCtrl()




if __name__ == '__main__':
    test_execControl()
import dbpy.db_mysql as database
from dbpy.db_mysql import f
from datetime import datetime
import re
from utilpy.date import Date

class ExecControl:
    """
    -> Use instructions:
        Call getProcessToExec: load a candidate to be executed 
        Call start: try to checkout the candidate updating status to 'P' and verify return
            if True, process
            if success, call updateSuccess function
            if error, call updateError function
    """

    def __init__(self, conStr:str, table:str):
        self.table = table
        self.db = database.DB(conStr)


    def __enter__(self):
        return self


    def __exit__(self, type, value, tb):
        if tb is None:
            self.endSuccess()
        else:
            self.endError(value)


    def getProcessToExec(self, processName:str=None) -> bool:
        """
        -> loads a candidate to be executed and try to start.
            If it can't start, it will load another process.
            It loads values to self.* variables
        :return: True if load a candidate
                 False if does not have a candidate to load or error
        """
        hourMin = re.search(' ([0-9]{2}:[0-9]{2}):[0-9]{2}',
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[1]

        if processName is None:
            queryCandidate = f"""
                select *
                from {self.table}
                where
                (statusLastExecution != 'S'
                    and (hourStart <= '{hourMin}' or hourStart2 <= '{hourMin}')
                    and     hourEnd >= '{hourMin}'
                ) or
                (statusLastExecution = 'E')
                """
        else:
            queryCandidate = f"""
                select * from {self.table} where statusLastExecution != 'P'
                and processName = '{processName}'
                """

        dic = self.db.getRowDic(queryCandidate)
        if dic is None:
            return False

        # Rules to not execute
        if processName==None:
            p = dic['periodicity']
            dtSuccess = Date(dic['dateLastSuccess'])
            dtExec = Date(dic['timeLastExecution'])
            today = Date()
            minSinceSuccess = round((today.date-dtSuccess.date).seconds/60)
            minSinceExec = round((today.date-dtExec.date).seconds/60)
            repeat = dic['repeatMinutes']
            status = dic['statusLastExecution']
            dayWeek = today.date.weekday()+1
            businessDay = (dayWeek <= 5)
            executedToday = (today.toString() == dtSuccess.toString())
            day = dic['day']
            tries = dic['triesWithError']
            maxTries = dic['maxTriesWithError']
            minsAfterTries = dic['minsAfterMaxTries']

            # Repeat = 0 -> execute once a day      # Repeat > 0 -> exec even x minutes
            if((repeat == 0 and executedToday) or (repeat > 0 and (minSinceSuccess < repeat))):
                return False

            # Periodicity criteria
            elif status == 'S':
                if ((p=='B' and not businessDay)
                 or (p=='W' and day != dayWeek)
                 or (p=='M' and day != today.date.day)
                ):
                    return False

            # After maxTries, exec every 30 minutes
            elif status == 'E' and tries >= maxTries and minSinceExec <= minsAfterTries:
                return False

        self.id = dic['id']
        self.processName = dic['processName']
        self.idUser = dic['idUser']
        self.periodicity = dic['periodicity']
        self.day = dic['day']
        self.hourStart = dic['hourStart']
        self.hourStart2 = dic['hourStart2']
        self.hourEnd = dic['hourEnd']
        self.repeatMinutes = dic['repeatMinutes']
        self.dateLastSuccess = dic['dateLastSuccess']
        self.statusLastExecution = dic['statusLastExecution']
        self.timeLastExecution = dic['timeLastExecution']
        self.triesWithError = dic['triesWithError']
        self.maxTriesWithError = dic['maxTriesWithError']
        self.minsAfterMaxTries = dic['minsAfterMaxTries']
        self.error = dic['error']
        self.numHardRegisters = dic['numHardRegisters']
        self.numHardRegistersLast = dic['numHardRegistersLast']
        self.numSoftRegisters = dic['numSoftRegisters']
        self.fk = dic['fk']

        return True


    def start(self):
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.db.exec(f"""
            update {self.table} set
                statusLastExecution = 'P'
            ,   timeLastExecution = '{dt}'
            where statusLastExecution != 'P' and id = {self.id}
            """) > 0:
            self.statusLastExecution = 'P'
            self.timeLastExecution = dt
            return True
        return False


    def endSuccess(self, numHardRegisters:int=0, numSoftRegisters:int=0):
        self.statusLastExecution = 'S'
        self.triesWithError = 0
        self.error = ''
        self.numHardRegistersLast = self.numHardRegisters
        self.numHardRegisters = numHardRegisters
        self.numSoftRegisters = numSoftRegisters
        mysql = f"""
            update {self.table}
            set statusLastExecution = '{self.statusLastExecution}'
            ,   triesWithError = {self.triesWithError}
            ,   error = ''
            ,   numHardRegisters = {self.numHardRegisters}
            ,   numSoftRegisters = {self.numSoftRegisters}
            ,   numHardRegistersLast = {self.numHardRegistersLast}
            where id = {self.id}
            """
        self.db.reconnect()
        self.db.exec(mysql)


    def endError(self, errorMessage:str):
        self.statusLastExecution = 'E'
        self.triesWithError+=1
        self.error = errorMessage
        self.numHardRegistersLast = self.numHardRegisters
        self.numHardRegisters = 0
        self.numSoftRegisters = 0

        mysql = f"""
            update {self.table}
            set statusLastExecution = '{self.statusLastExecution}'
            ,   triesWithError = {self.triesWithError}
            ,   error = '{self.error}'
            ,   numHardRegisters = {self.numHardRegisters}
            ,   numSoftRegisters = {self.numSoftRegisters}
            ,   numHardRegistersLast = {self.numHardRegistersLast}
            where id = {self.id}
            """
        self.db.reconnect()
        self.db.exec(mysql)



if __name__ == '__main__':
    import utilpy.tests.test_execControl as test_execControl
    test_execControl.test_execControl()
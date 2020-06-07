import dbpy.db_mysql as database
from dbpy.db_mysql import f
from datetime import datetime
import re

class ExecControl:
    """
    -> Use instructions:
        Call getProcessToExec: load a candidate to be executed 
        and try to start. If it can't start, it will load another 
        process. It loads values to self.* variables
    ->      if True, process
    ->      if success, call updateSuccess function
    ->      if error, call updateError function
    """

    def __init__(self, conStr:str, table:str, idUser:int):
        self.table = table
        self.db = database.DB(conStr)
        self.idUser = idUser


    def getProcessToExec(self) -> bool:
        """
        -> loads a candidate to be executed and try to start.
            If it can't start, it will load another process.
            It loads values to self.* variables
        :return: True if load a candidate
                 False if does not have a candidate to load or error
        """
        started = False
        while not started:
            if self.__loadCandidate() == False:
                return False
            started = self.__start()


    def __loadCandidate(self) -> bool:
        hourMin = re.search(' ([0-9]{2}:[0-9]{2}):[0-9]{2}',
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[1]
        queryCandidate = f"""
            select *
              from {self.table}
             where statusLastExecution != 'P'
               and (hourStart <= '{hourMin}' or
                    hourStart2 <= '{hourMin}')
               and hourEnd >= '{hourMin}'
               and triesWithError < maxTriesWithError
               and periodicity = 'D' """

        dic = self.db.getRowDic(queryCandidate)
        if dic is None:
            return False

        self.id = dic['id']
        self.idUser = dic['idUser']
        self.periodicity = dic['periodicity']
        self.day = dic['day']
        self.hourStart = dic['hourStart']
        self.hourStart2 = dic['hourStart2']
        self.hourEnd = dic['hourEnd']
        self.repeatMinutes = dic['repeatMinutes']
        self.dateLastSuccess = dic['dateLastSuccess']
        self.statusLastExecution = dic['statusLastExecution']
        self.triesWithError = dic['triesWithError']
        self.maxTriesWithError = dic['maxTriesWithError']
        self.error = dic['error']
        self.numHardRegisters = dic['numHardRegisters']
        self.numHardRegistersLast = dic['numHardRegistersLast']
        self.numSoftRegisters = dic['numSoftRegisters']
        self.fk = dic['fk']

        return True


    def __start(self):
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


    def updateSuccess(self, numHardRegisters, numSoftRegisters):
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
        self.db.exec(mysql)


    def updateError(self, errorMessage:str):
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
        self.db.exec(mysql)


    def _createNewRegister(self, processName:str):
        self.processName = processName
        self.periodicity = 'D'
        self.day = 'null'
        self.hourStart = '07:00'
        self.hourStart2 = 'null'
        self.hourEnd = '19:00'
        self.repeatMinutes = 0
        self.dateLastSuccess = 'null'
        self.statusLastExecution = 'I'
        self.timeLastExecution = 'null'
        self.triesWithError = 0
        self.maxTriesWithError = 3
        self.error = 'null'
        self.numHardRegisters = 0
        self.numHardRegistersLast = 0
        self.numSoftRegisters = 0
        self.fk = 'null'

        mysql = f"""
            INSERT INTO {self.table}
            (
            `processName`,
            `idUser`,
            `periodicity`,
            `day`,
            `hourStart`,
            `hourStart2`,
            `hourEnd`,
            `repeatMinutes`,
            `dateLastSuccess`,
            `statusLastExecution`,
            `timeLastExecution`,
            `triesWithError`,
            `maxTriesWithError`,
            `error`,
            `numHardRegisters`,
            `numHardRegistersLast`,
            `numSoftRegisters`,
            `fk`
            )
            VALUES
            (
            {f(self.processName)},
            {f(self.idUser)},
            {f(self.periodicity)},
            {f(self.day)},
            {f(self.hourStart)},
            {f(self.hourStart2)},
            {f(self.hourEnd)},
            {f(self.repeatMinutes)},
            {f(self.dateLastSuccess)},
            {f(self.statusLastExecution)},
            {f(self.timeLastExecution)},
            {f(self.triesWithError)},
            {f(self.maxTriesWithError)},
            {f(self.error)},
            {f(self.numHardRegisters)},
            {f(self.numHardRegistersLast)},
            {f(self.numSoftRegisters)},
            {f(self.fk)}
            );
            """.replace('\n','')

        self.db.exec(mysql)


    def _dropTableCtrl(self):
        self.db.exec(f"drop table if exists {self.table}")


    def _createTableCtrl(self):
        # Necessary table: getWebDataCtl
        # ProcessName (str 30): Process Name
        # Periodicity (str 1) H (Hourly), D (diary), W (weekly),
        #          M (monthly),
        #          B (business day diary but not saturday or sunday)
        # Day (int): Day number - 1 (Monday) to 7 (Saturday)
        #            for Weekly or month day number for M
        # HourStart: Hour to first try
        # HourStart2: Hour to first try
        # HourEnd: Not to execute after this hour
        # RepeatMinutes: After start in this day, repeat every x min
        # DateLastSuccess (date): Last time exec result in Success
        # StatusLastExecution (str 1): S, P, E
        # TimeLastExecution (str 1): S, P, E
        # TriesWithError: int
        # MaxTriesWithError: int
        # Error (str 1000): Last Error Message
        # NumHardRegisters
        # NumHardRegistersLast
        # NumSoftRegisters

        mysql =f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `processName` varchar(50) DEFAULT NULL,
        `idUser` int NOT NULL,
        `periodicity` char(1) NOT NULL,
        `day` tinyint(4) DEFAULT NULL,
        `hourStart` char(5) NOT NULL,
        `hourStart2` char(5),
        `hourEnd` char(5) NOT NULL,
        `repeatMinutes` tinyint(4) DEFAULT NULL,
        `dateLastSuccess` datetime DEFAULT NULL,
        `statusLastExecution` char(1) DEFAULT NULL,
        `timeLastExecution` datetime DEFAULT NULL,
        `triesWithError` tinyint(4) DEFAULT NULL,
        `maxTriesWithError` tinyint(4) DEFAULT NULL,
        `error` varchar(1000) DEFAULT NULL,
        `numHardRegisters` int(11) DEFAULT NULL,
        `numHardRegistersLast` int(11) DEFAULT NULL,
        `numSoftRegisters` int(11) DEFAULT NULL,
        `fk` varchar(50) DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `getWebDataCtl_unique_index` (`processName`
                                                ,`periodicity`
                                                ,`day`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
        """
        self.db.exec(mysql)




if __name__ == '__main__':
    import utilpy.tests.test_execControl as test_execControl
    test_execControl.test_execControl()
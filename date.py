from datetime import datetime

class Date:
    """
    :param dt: now or utc or string in format '%d/%m/%Y' (pt) or '%m/%d/%Y' (en)
    :param language: 'pt' or 'en'
    :param timeFormat: time: %H=H24, %I=H12, %p=PM/AM or pm/am, %M=min, %S=sec
    """

    def __init__(self, dt:str='now', language:str='pt', timeFormat:str=None):
        if dt == 'now':  self.date = datetime.now()
        elif dt == 'utc': self.date = datetime.utcnow()

        if timeFormat is None: time = ''
        else: time = ' '+timeFormat

        if language=='pt':
            if '/' in dt: self.date = datetime.strptime(dt, '%d/%m/%Y'+time)
            elif '-' in dt: self.date = datetime.strptime(dt, '%d-%m-%Y'+time)
        elif language=='en':
            if '/' in dt: self.date = datetime.strptime(dt, '%m/%d/%Y'+time)
            elif '-' in dt: self.date = datetime.strptime(dt, '%m-%d-%Y'+time)
        else:
            raise NotImplementedError(language+' is not implemented yet')        


    def toString(self, format:str='%Y-%m-%d') -> str:
        return self.date.strftime(format)

    def toDatetimeString(self, format:str='%Y-%m-%d %H:%M:%S') -> str:
        return self.date.strftime(format)

def mapMonthFromNumber(num:int, upperCase:bool=None, language:str='pt') -> str:
    if language == 'pt':
        if num ==1 : month = "Janeiro"
        if num ==2 : month = "Fevereiro"
        if num ==3 : month = "Março"
        if num ==4 : month = "Abril"
        if num ==5 : month = "Maio"
        if num ==6 : month = "Junho"
        if num ==7 : month = "Julho"
        if num ==8 : month = "Agosto"
        if num ==9 : month = "Setembro"
        if num ==10 : month = "Outubro"
        if num ==11 : month = "Novembro"
        if num ==12 : month = "Dezembro"
        if num ==0 : month = "Dezembro"
    elif language == 'en':
        if num ==1 : month = "January"
        if num ==2 : month = "February"
        if num ==3 : month = "March"
        if num ==4 : month = "April"
        if num ==5 : month = "May"
        if num ==6 : month = "June"
        if num ==7 : month = "July"
        if num ==8 : month = "August"
        if num ==9 : month = "September"
        if num ==10 : month = "October"
        if num ==11 : month = "November"
        if num ==12 : month = "December"
        if num ==0 : month = "December"
    else:
        return None
    
    if upperCase is None:
        return month
    if upperCase == True:
        return month.upper()
    if upperCase == False:
        return month.lower()
    

def mapMonthFromText(month:str) -> int:
    month = month.upper()
    if month =="JAN" or month == 'JANEIRO' or month == 'JANUARY' : return 1
    if month =="FEV" or month == 'FEB' or month == 'FEVEREIRO' or month == 'FEBRUARY': return 2
    if month =="MAR" or month == 'MARÇO' or month == 'MARCH' : return 3
    if month =="ABR" or month == 'APR' or month == 'ABRIL' or month == 'APRIL': return 4
    if month =="MAI" or month == 'MAY' or month == 'MAIO': return 5
    if month =="JUN" or month == 'JUNHO' or month == 'JUNE': return 6
    if month =="JUL" or month == 'JULHO' or month == 'JULY': return 7
    if month =="AGO" or month == 'AUG' or month == 'AGOSTO' or month == 'AUGUST': return 8
    if month =="SET" or month == 'SEP' or month == 'SETEMBRO' or month == 'SEPTEMBER': return 9
    if month =="OUT" or month == 'OCT' or month == 'OUTUBRO' or month == 'OCTOBER': return 10
    if month =="NOV" or month == 'NOVEMBRO' or month == 'NOVEMBER': return 11
    if month =="DEZ" or month == 'DEC' or month == 'DEZEMBRO' or month == 'DECEMBER': return 12

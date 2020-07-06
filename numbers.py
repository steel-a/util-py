
def toFloat(value:str) -> float:
    """
    -> Convert a input string in US or Europe/BRL format to float
    ##### Maximum decimal places of input string: 2
    Possible inputs:
    '1,000,000,000.76','1,000,000,000.7','1000000000.76','1000000000.7','1.000.000.000,76','1.000.000.000,7'
    ,'1000000000,76','1000000000,7','1,000,000,000','1.000.000.000','1000000000', '10', '1,1', '1.0', '1,11', '1.01'
    ,1,000,000,000.765','1000000000.765','1.000.000.000,765', '1000000000,765,'1,000.765','1000.765','1.000,765', '1000,765'
    """
    div = 1 if value.count('%')==0 else 100
    value = value.replace('$','').replace('USD','').replace('US','').replace('BRL','').replace('BR','').replace('EUR','').replace('R','').replace(' ','').replace('%','')
    num_coma = value.count(',')
    num_dot = value.count('.')

    try:

        if num_coma>1: # US Format
            return float(value.replace(',',''))/div
        elif num_dot>1: # European Format
            return float(value.replace('.','').replace(',','.'))/div
        elif num_coma==1 and num_dot==1:
            if(value.find(',')<value.find('.')): # US Format
                return float(value.replace(',',''))/div
            else: # European format
                return float(value.replace('.','').replace(',','.'))/div
        elif num_coma==1: # European Format
            return float(value.replace(',','.'))/div
        elif num_dot==1 or (num_coma==0 and num_dot==0): # US Format
            return float(value)/div
    except:
        return None
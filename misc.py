import pandas as pd

# convert NoneType to empty string
xstr = lambda s: s or ' '   

def check_for_any_missing_values(data):
    """
    This function checks for any missing values in a dataframe
    and return a boolean (True/False). 
    Args:
        data: pandas Dataframe 
    """
    return data.isnull().values.any()



def convert_date(data):
    """
    This function converts date from string to datetime objects
    Arg:
        data: pandas Series
    """

    data = pd.to_datetime(data, format='%Y-%m-%d')
    return data

# translate Czech to English
trans_type = lambda s: 'credit' if s == 'PRIJEM' else 'withdrawal' 
disp_type = lambda s: 'owner' if s == "OWNER" else 'user'

def trans_operation(x):
    if x == 'VYBER KARTOU':
        return 'credit card withdrawal'
    elif x == 'VKLAD':
        return 'credit in cash'
    elif x == 'PREVOD Z UCTU':
        return 'from another bank'
    elif x == 'VYBER':
        return 'withdrawal in cash'
    elif x == 'PREVOD NA UCET':
        return 'to another bank'
    else:
        return 'unknown'

def trans_ksymbol(x):
    if x == "POJISTNE":
        return 'insurance'
    elif x == "SLUZBY":
        return 'statement'
    elif x == "UROK":
        return 'interest credited'
    elif x == "SANKC. UROK":
        return 'sanction interest'
    elif x == "SIPO":
        return 'household'
    elif x == "DUCHOD":
        return 'pension'
    elif x == "UVER":
        return 'loan'
    elif x == "LEASING":
        return 'leasing'
    else:
        return "unknown"
    
def account_freq(x):
    if x == "POPLATEK MESICNE":
        return 'monthly'
    elif x == "POPLATEK TYDNE":
        return 'weekly'
    elif x == "POPLATEK PO OBRATU":
        return 'after transaction'
    else:
        return "unknown"

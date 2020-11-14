import pandas as pd
import sqlite3 as sql
from misc import *

def load_original_dataset():
    """ 
    This function loads 8 tables from financial.db using sqlite3
    and returns 8 pandas dataframes in this specific order:
    account, card, client, disp, district, loan, order, trans
    """

    # load data from financial.db
    conn   = sql.connect('financial.db')
    c      = conn.cursor()

    # Convert SQL tables to pandas dataframes to explore the data
    query_account   = "SELECT * FROM account"
    query_client    = "SELECT * FROM client"
    query_disposition = "SELECT * FROM disp"
    query_order     = "SELECT * FROM [order]"
    query_trans     = "SELECT * FROM trans"
    query_loan      = "SELECT * FROM loan"
    query_card      = "SELECT * FROM card"
    query_district  = "SELECT * FROM district"

    account = pd.read_sql_query(query_account, conn)
    card    = pd.read_sql_query(query_card, conn)
    client  = pd.read_sql_query(query_client, conn)
    disp    = pd.read_sql_query(query_disposition, conn)
    district = pd.read_sql_query(query_district, conn)
    loan    = pd.read_sql_query(query_loan, conn)
    order   = pd.read_sql_query(query_order, conn)
    trans   = pd.read_sql_query(query_trans, conn)

    return account, card, client, disp, district, loan, order, trans

def load_clean_dataset():
    """ 
    This function returns a clean dataset with the following 
    modification made.

    account: 
    - translate frequency from Czech to English
    - replace date from string to datetime objects

    card:
    - replace date from string to datetime objects

    client:
    - replace date from string to datetime objects

    disp:
    - translate type from Czech to English

    order:
    - translate k_symbol from Czech to English

    trans:
    - replace date from string to datetime objects
    - translate type, operation, k_symbol from Czech to English
    - operation, k_symbol, bank, account

    loan:
    - replace date from string to datetime objects

    district:
    - A12, A15: missing value
    """

    account, card, client, disp, district, loan, order, trans = load_original_dataset()

    account['date'] = convert_date(account['date'])
    account['frequency'] = account['frequency'].apply(account_freq) 

    card['issued'] = convert_date(card['issued'])
    client['birth_date'] = convert_date(client['birth_date'])
    disp['type'] = disp['type'].apply(disp_type)
    order['k_symbol'] = order['k_symbol'].apply(trans_ksymbol)
    
    trans['k_symbol'] = trans['k_symbol'].apply(trans_ksymbol)
    trans['type'] = trans['type'].apply(trans_type)
    trans['operation'] = trans['operation'].apply(trans_operation)

    loan['date'] = convert_date(loan['date'])

    return account, card, client, disp, district, loan, order, trans

# def load_clean_numerical_dataset():
#     """
#     This function returns numerical only dataset (good for ML models that 
#     only take in numerical values)
    
#     """

#     account, card, client, disp, district, loan, order, trans = load_clean_dataset()


#     return account, card, client, disp, district, loan, order, trans

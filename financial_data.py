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
    - drop "bank_to" and "account_to" columns

    trans:
    - replace date from string to datetime objects
    - translate type, operation, k_symbol from Czech to English
    - drop "bank" and "account" columns


    loan:
    - replace date from string to datetime objects

    district:
    - replace missing values in A12, A15 with average value
    """

    account, card, client, disp, district, loan, order, trans = load_original_dataset()

    account['date'] = convert_date(account['date'])
    account         = account.rename(columns={'date': 'account_date'})
    account['frequency'] = account['frequency'].apply(account_freq) 

    card['issued']  = convert_date(card['issued'])
    card            = card.rename(columns={'issued': 'issued_date', 
                                    'type': 'card_type'})

    client['birth_date'] = convert_date(client['birth_date'])

    disp['type']    = disp['type'].apply(disp_type)
    disp            = disp.rename(columns={'type': 'disp_type'})

    order['k_symbol'] = order['k_symbol'].apply(trans_ksymbol)
    order           = order.rename(columns={'k_symbol': 'order_k_symbol'})
    order           = order.drop(columns=["bank_to", "account_to"])
    order           = normalize(order, 'order_amount')
    
    trans['k_symbol'] = trans['k_symbol'].apply(trans_ksymbol)
    trans['type']   = trans['type'].apply(trans_type)
    trans['operation'] = trans['operation'].apply(trans_operation)
    trans['date']   = convert_date(trans['date'])
    trans           = trans.drop(columns=["bank", "account"])
    trans           = trans.rename(columns={"k_symbol": "trans_k_symbol", 
                            "type": "trans_type", "operation": "trans_operation",
                            "date": "trans_date"})
    trans           = normalize(trans, "trans_amount", "trans_balance")

    loan['date']    = convert_date(loan['date'])
    loan            = loan.rename(columns = {"date": "loan_date"})
    loan = normalize(loan, "loan_amount", "duration", "payments")

    district['A12'] = district['A12'].fillna(eliminate_outliers(district['A12']).mean())
    district['A15'] = district['A15'].fillna(eliminate_outliers(district['A15']).mean())

    district = normalize(district, 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11',
        'A12', 'A13', 'A14', 'A15', 'A16')

    district        = district.rename(columns = {"A2": "district_name", 
        "A3": "region", "A4": "no_of_inhibitants", 
        "A5": "no_of_municipalities_with_inhabitants_less_than_499",
        "A6": "no_of_municipalities_with_inhabitants_between_500_to_1999",
        "A7": "no_of_municipalities_with_inhabitants_between_1000_to_9999",
        "A8": "no_of_municipalities_with_inhabitants_greater_than_10000",
        "A9": "no_of_cities", "A10": "ratio_of_urban_inhabitants",
        "A11": "average_salary", "A12": "unemployment_rate_95",
        'A13': "unemployment_rate_96", "A14": "no_of_enterpreneurs_per_1000_inhabitants",
        "A15": "no_of_commited_crimes_95", "A16": "no_of_commited_crimes_96"})

    return account, card, client, disp, district, loan, order, trans

def load_clean_numerical_dataset():
    """
    This function returns numerical only dataset (good for ML models that 
    only take in numerical values) by using label encoding for categorical data.

    account:
    - frequency (account_id, district_id, date)

    card:
    - type (card_id, disp_id, issued)

    client:
    - gender (client_id, birth_date, district_id)

    disp:
    - type (disp_id, client_id, account_id)

    district:
    - A2:district name, A3:region (district_id)

    loan:
    - status (loan_id, account_id, date)

    order:
    - k_symbol (order_id, account_id)

    trans:
    - type, operation, k_symbol (trans_id, account_id, date)

    """

    account, card, client, disp, district, loan, order, trans = load_clean_dataset()

    account['frequency'] = account['frequency'].astype('category').cat.codes
    card['card_type']   = card['card_type'].astype('category').cat.codes
    client['gender']    = client['gender'].astype('category').cat.codes
    disp['disp_type']   = disp['disp_type'].astype('category').cat.codes

    district['district_name'] = district['district_name'].astype('category').cat.codes
    district['region']  = district['region'].astype('category').cat.codes

    loan['status']      = loan['status'].astype('category').cat.codes
    order['order_k_symbol'] = order['order_k_symbol'].astype('category').cat.codes
    trans['trans_type']     = trans['trans_type'].astype('category').cat.codes
    trans['trans_operation'] = trans['trans_operation'].astype('category').cat.codes
    trans['trans_k_symbol'] = trans['trans_k_symbol'].astype('category').cat.codes

    return account, card, client, disp, district, loan, order, trans

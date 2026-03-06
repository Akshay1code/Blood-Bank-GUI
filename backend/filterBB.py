from backend import db

def fetching_urgentBB_list():
    bank_list=db.fetch_all_blood_banks()
    for stock in bank_list:
        if(stock['a_positive']>5):
            del stock['a_positive']
        if(stock['a_negative']>5):
            del stock['a_negative']
        if(stock['o_positive']>5):
            del stock['o_positive']
        if(stock['o_negative']>5):
            del stock['o_negative']
        if(stock['ab_positive']>5):
            del stock['ab_positive']
        if(stock['ab_negative']>5):
            del stock['ab_negative']
        if(stock['b_positive']>5):
            del stock['b_positive']
        if(stock['b_negative']>5):
            del stock['b_negative']

    return bank_list
        
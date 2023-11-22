from .models import Dminstitution, Dmproject
from . import db
import datetime
# from sqlalchemy import col

def institutions():
    # SQA 1.x style query        
    query = db.session.query(Dminstitution.__table__).all()
    result = lambda lst: [(x[1], x[2]) for x in lst]
    # Returns elements (1, 2) e.g. ('EXIM', 'Eximbank')
    return result(query)

def format_date(date_str):
    time = map(int, date_str.split('-'))
    dt = datetime.datetime(*time).strftime('%d-%b-%y')
    return dt.upper()

def projects():
    # SQA 1.x style query
    query = db.session.query(Dmproject.__table__).all()
    result = lambda lst: [(x[0], x[3]) for x in lst]
    return result(query)

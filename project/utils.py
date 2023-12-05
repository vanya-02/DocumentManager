from .models import Dminstitutions, Dmprojects
from . import db
from sqlalchemy import text
import datetime
import json

def institutions():
    # SQA 1.x style query        
    query = db.session.query(Dminstitutions.__table__).all()
    result = lambda lst: [(x[1], x[2]) for x in lst]
    # Returns elements (1, 2) e.g. ('EXIM', 'Eximbank')
    return result(query)

def format_date(date_str):
    time = map(int, date_str.split('-'))
    dt = datetime.datetime(*time).strftime('%d-%b-%y')
    return dt.upper()

def projects():
    # SQA 1.x style query
    query = db.session.query(Dmprojects.__table__).all()
    result = lambda lst: [(x[0], x[3]) for x in lst]
    return result(query)

def placeholder_query(value):
    query = f"select name, instcode, additionalinfo from dminstitutions where instcode = '{value}'"
    result = db.session.execute(text(query)).first()
    print(result, type(result))

    x = json.dumps(list(result))
    print(x, type(x))
    return x

RawSQL = {
    '0': None,
    'INSTITUTIONS': 'select instcode, name, additionalinfo from dminstitutions',
    'DOCUMENTS': '''
    select d.name, p.name as Project, i.name as Institution, t.typedscr as Document_Type, d.additionalinfo, d.uploaddate
    from dmdocuments d
    join dmprojects p on d.idproject = p.id  
    join dminstitutions i on d.idinstitution = i.id
    join dmdocumenttypes t on d.idtype = t.id
    '''
}

    

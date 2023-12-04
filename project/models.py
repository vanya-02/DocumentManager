# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, VARCHAR, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()
metadata = Base.metadata


class Dmdocumenttype(Base):
    __tablename__ = 'dmdocumenttypes'

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False)
    name = Column(VARCHAR(32), nullable=False)
    typedscr = Column(VARCHAR(1000), nullable=False)
    ismacro = Column(VARCHAR(20), nullable=False)
    isdategrouped = Column(VARCHAR(20), nullable=False)

    parents = relationship(
        'Dmdocumenttype',
        secondary='dmdocumenttypelerarchy',
        primaryjoin='Dmdocumenttype.id == dmdocumenttypelerarchy.c.idmacro',
        secondaryjoin='Dmdocumenttype.id == dmdocumenttypelerarchy.c.idmicro'
    )


class Dminstitution(Base):
    __tablename__ = 'dminstitutions'

    id = Column(Integer, primary_key=True)
    instcode = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(32), nullable=False)
    additionalinfo = Column(VARCHAR(256))


class Dmdocument(Base):
    __tablename__ = 'dmdocuments'

    id = Column(Integer, primary_key=True)
    idinstitution = Column(ForeignKey('dminstitutions.id'), nullable=False)
    iduser = Column(ForeignKey('dmusers.id'), nullable=False)
    idtype = Column(ForeignKey('dmdocumenttypes.id'), nullable=False)
    idproject = Column(ForeignKey('dmprojects.id'), nullable=False)
    name = Column(VARCHAR(260), nullable=False)
    savedpath = Column(VARCHAR(256), nullable=False)
    uploaddate = Column(DateTime, nullable=False)
    additionalinfo = Column(VARCHAR(1000), nullable=False)
    groupingdate = Column(DateTime, nullable=False)

    dminstitution = relationship('Dminstitution')
    dmproject = relationship('Dmproject')
    dmdocumenttype = relationship('Dmdocumenttype')
    dmuser = relationship('Dmuser')


class Dmuserrole(Base):
    __tablename__ = 'dmuserroles'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(32), nullable=False)

    dmusers = relationship('Dmuser', secondary='dmusertorole')


t_dmdocumenttypelerarchy = Table(
    'dmdocumenttypelerarchy', metadata,
    Column('idmacro', ForeignKey('dmdocumenttypes.id'), primary_key=True, nullable=False),
    Column('idmicro', ForeignKey('dmdocumenttypes.id'), primary_key=True, nullable=False)
)


class Dmuser(UserMixin, Base):
    __tablename__ = 'dmusers'

    id = Column(Integer, primary_key=True)
    idinstitution = Column(ForeignKey('dminstitutions.id'))
    username = Column(VARCHAR(32), nullable=False)
    password = Column(VARCHAR(256), nullable=False)
    email = Column(VARCHAR(32), nullable=False)
    isenabled = Column(VARCHAR(32), nullable=False, server_default=text("'True' "))
    name = Column(VARCHAR(32))
    surname = Column(VARCHAR(32))
    patronymic = Column(VARCHAR(32))

    dminstitution = relationship('Dminstitution')


class Dmproject(Base):
    __tablename__ = 'dmprojects'

    id = Column(Integer, primary_key=True)
    idinstitution = Column(ForeignKey('dminstitutions.id'), nullable=True)
    iduser = Column(ForeignKey('dmusers.id'), nullable=True)
    name = Column(VARCHAR(256), nullable=True)
    datefrom = Column(DateTime, nullable=True)
    datetill = Column(DateTime, nullable=True)
    additionalinfo = Column(VARCHAR(1000), server_default=text("NULL"), nullable=True)
    isactive = Column(VARCHAR(20), server_default=text("'True'"))

    dminstitution = relationship('Dminstitution')
    dmuser = relationship('Dmuser')


t_dmusertorole = Table(
    'dmusertorole', metadata,
    Column('iduser', ForeignKey('dmusers.id'), primary_key=True, nullable=False),
    Column('idrole', ForeignKey('dmuserroles.id'), primary_key=True, nullable=False)
)
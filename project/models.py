from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, Table, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

from flask_login import UserMixin

Base = declarative_base()
metadata = Base.metadata


class Dmdocumenttypes(Base):
    __tablename__ = 'dmdocumenttypes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dmdocumenttypes_pk'),
    )

    id = mapped_column(Integer)
    code = mapped_column(Integer, nullable=False)
    name = mapped_column(VARCHAR(32), nullable=False)
    typedscr = mapped_column(VARCHAR(1000), nullable=False)
    ismacro = mapped_column(VARCHAR(20), nullable=False)
    isdategrouped = mapped_column(VARCHAR(20), nullable=False)

    dmdocumenttypes: Mapped['Dmdocumenttypes'] = relationship('Dmdocumenttypes', secondary='dmdocumenttypelerarchy', primaryjoin=lambda: Dmdocumenttypes.id == t_dmdocumenttypelerarchy.c.idmacro, secondaryjoin=lambda: Dmdocumenttypes.id == t_dmdocumenttypelerarchy.c.idmicro, back_populates='dmdocumenttypes_')
    dmdocumenttypes_: Mapped['Dmdocumenttypes'] = relationship('Dmdocumenttypes', secondary='dmdocumenttypelerarchy', primaryjoin=lambda: Dmdocumenttypes.id == t_dmdocumenttypelerarchy.c.idmicro, secondaryjoin=lambda: Dmdocumenttypes.id == t_dmdocumenttypelerarchy.c.idmacro, back_populates='dmdocumenttypes')
    dmdocuments: Mapped[List['Dmdocuments']] = relationship('Dmdocuments', uselist=True, back_populates='dmdocumenttypes')


class Dminstitutions(Base):
    __tablename__ = 'dminstitutions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dminstitutions_pk'),
    )

    id = mapped_column(Integer)
    instcode = mapped_column(VARCHAR(20))
    name = mapped_column(VARCHAR(32))
    additionalinfo = mapped_column(VARCHAR(256))

    dmusers: Mapped[List['Dmusers']] = relationship('Dmusers', uselist=True, back_populates='dminstitutions')
    dmprojects: Mapped[List['Dmprojects']] = relationship('Dmprojects', uselist=True, back_populates='dminstitutions')
    dmdocuments: Mapped[List['Dmdocuments']] = relationship('Dmdocuments', uselist=True, back_populates='dminstitutions')


class Dmuserroles(Base):
    __tablename__ = 'dmuserroles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dmuserroles_pk'),
    )

    id = mapped_column(Integer)
    name = mapped_column(VARCHAR(32), nullable=False)

    dmusers: Mapped['Dmusers'] = relationship('Dmusers', secondary='dmusertorole', back_populates='dmuserroles')


t_dmdocumenttypelerarchy = Table(
    'dmdocumenttypelerarchy', metadata,
    Column('idmacro', Integer, nullable=False),
    Column('idmicro', Integer, nullable=False),
    ForeignKeyConstraint(['idmacro'], ['dmdocumenttypes.id'], name='dmdocumenttypelerarchy_fk1'),
    ForeignKeyConstraint(['idmicro'], ['dmdocumenttypes.id'], name='dmdocumenttypelerarchy_fk2'),
    PrimaryKeyConstraint('idmacro', 'idmicro', name='dmdocumenttypelerarchy_pk')
)


class Dmusers(UserMixin, Base):
    __tablename__ = 'dmusers'
    __table_args__ = (
        ForeignKeyConstraint(['idinstitution'], ['dminstitutions.id'], name='dmusers_fk1'),
        PrimaryKeyConstraint('id', name='dmusers_pk')
    )

    id = mapped_column(Integer)
    username = mapped_column(VARCHAR(32), nullable=False)
    password = mapped_column(VARCHAR(256), nullable=False)
    email = mapped_column(VARCHAR(32), nullable=False)
    isenabled = mapped_column(VARCHAR(32), nullable=False, server_default=text("'True' "))
    idinstitution = mapped_column(Integer)
    name = mapped_column(VARCHAR(32))
    surname = mapped_column(VARCHAR(32))
    patronymic = mapped_column(VARCHAR(32))

    dmuserroles: Mapped['Dmuserroles'] = relationship('Dmuserroles', secondary='dmusertorole', back_populates='dmusers')
    dminstitutions: Mapped[Optional['Dminstitutions']] = relationship('Dminstitutions', back_populates='dmusers')
    dmprojects: Mapped[List['Dmprojects']] = relationship('Dmprojects', uselist=True, back_populates='dmusers')
    dmdocuments: Mapped[List['Dmdocuments']] = relationship('Dmdocuments', uselist=True, back_populates='dmusers')


class Dmprojects(Base):
    __tablename__ = 'dmprojects'
    __table_args__ = (
        ForeignKeyConstraint(['idinstitution'], ['dminstitutions.id'], name='dmprojects_fk2'),
        ForeignKeyConstraint(['iduser'], ['dmusers.id'], name='dmprojects_fk1'),
        PrimaryKeyConstraint('id', name='dmprojects_pk')
    )

    idinstitution = mapped_column(Integer, nullable=False)
    id = mapped_column(NUMBER(asdecimal=False), Identity(always=True, on_null=False, start=1, increment=1, minvalue=1, maxvalue=9999999999, cycle=False, cache=20, order=False))
    iduser = mapped_column(Integer)
    name = mapped_column(VARCHAR(256))
    datefrom = mapped_column(DateTime)
    datetill = mapped_column(DateTime)
    additionalinfo = mapped_column(VARCHAR(1000), server_default=text('NULL '))
    isactive = mapped_column(VARCHAR(20), server_default=text("'True' "))

    dminstitutions: Mapped['Dminstitutions'] = relationship('Dminstitutions', back_populates='dmprojects')
    dmusers: Mapped[Optional['Dmusers']] = relationship('Dmusers', back_populates='dmprojects')
    dmdocuments: Mapped[List['Dmdocuments']] = relationship('Dmdocuments', uselist=True, back_populates='dmprojects')


t_dmusertorole = Table(
    'dmusertorole', metadata,
    Column('iduser', Integer, nullable=False),
    Column('idrole', Integer, nullable=False),
    ForeignKeyConstraint(['idrole'], ['dmuserroles.id'], name='dmusertorole_fk1'),
    ForeignKeyConstraint(['iduser'], ['dmusers.id'], name='dmusertorole_fk2'),
    PrimaryKeyConstraint('iduser', 'idrole', name='dmusertorole_pk')
)


class Dmdocuments(Base):
    __tablename__ = 'dmdocuments'
    __table_args__ = (
        ForeignKeyConstraint(['idinstitution'], ['dminstitutions.id'], name='dmdocuments_fk2'),
        ForeignKeyConstraint(['idproject'], ['dmprojects.id'], name='dmdocuments_fk3'),
        ForeignKeyConstraint(['idtype'], ['dmdocumenttypes.id'], name='dmdocuments_fk1'),
        ForeignKeyConstraint(['iduser'], ['dmusers.id'], name='dmdocuments_fk4'),
        PrimaryKeyConstraint('id', name='dmdocuments_pk')
    )

    id = mapped_column(Integer)
    idinstitution = mapped_column(Integer, nullable=False)
    iduser = mapped_column(Integer, nullable=False)
    idtype = mapped_column(Integer, nullable=False)
    idproject = mapped_column(Integer, nullable=False)
    name = mapped_column(VARCHAR(260), nullable=False)
    savedpath = mapped_column(VARCHAR(256), nullable=False)
    uploaddate = mapped_column(DateTime, nullable=False)
    additionalinfo = mapped_column(VARCHAR(1000))
    groupingdate = mapped_column(DateTime)

    dminstitutions: Mapped['Dminstitutions'] = relationship('Dminstitutions', back_populates='dmdocuments')
    dmprojects: Mapped['Dmprojects'] = relationship('Dmprojects', back_populates='dmdocuments')
    dmdocumenttypes: Mapped['Dmdocumenttypes'] = relationship('Dmdocumenttypes', back_populates='dmdocuments')
    dmusers: Mapped['Dmusers'] = relationship('Dmusers', back_populates='dmdocuments')
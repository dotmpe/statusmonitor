"""
SQL schema w.i.p.
::

  Record >---.--- Job >---.--- Script ---< Extract
   - key     |            |     - path      - key
   - value   |            |                 - regex
           Host         Schedule
            - name       - cronstr
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Text, \
    ForeignKey, Table, Index, DateTime, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

SqlBase = declarative_base()

class Record(SqlBase):
    __tablename__ = 'records'
    record_id = Column('id', Integer, primary_key=True)
    key = Column(String, index=True, unique=True, nullable=False)
    datatype = Column(String, nullable=False, default="str")
    value = Column(String, nullable=False)
    host_id = Column(ForeignKey("hosts.id"))
    job_run = Column(DateTime)
    job_id = Column(ForeignKey('jobs.id'))

class Job(SqlBase):
    __tablename__ = 'jobs'
    job_id = Column('id', Integer, primary_key=True)
    schedule_id = Column(ForeignKey("schedules.id"))
    script_id = Column(ForeignKey("scripts.id"))
    is_running = Column(Boolean, default=False)
    last_run = Column(DateTime)

class Host(SqlBase):
    __tablename__ = 'hosts'
    host_id = Column('id', Integer, primary_key=True)
    hostname = Column(String)

    records = relationship(Record,
            primaryjoin=Record.host_id==host_id,
            backref='host')

class Schedule(SqlBase):
    __tablename__ = 'schedules'
    schedule_id = Column('id', Integer, primary_key=True)
    cronstring = Column(String, unique=True, index=True, nullable=False)

    jobs = relationship(Job,
            primaryjoin=Job.schedule_id==schedule_id,
            backref='schedule')

class Script(SqlBase):
    __tablename__ = 'scripts'
    script_id = Column('id', Integer, primary_key=True)
    path = Column(String, unique=True, index=True)

    jobs = relationship(Job,
            primaryjoin=Job.script_id==script_id,
            backref='script')

    extracts = relationship('Extract',
            primaryjoin='scripts.id == extracts.script_id',
            backref='script')

class Extract(SqlBase):
    __tablename__ = 'extracts'
    extract_id = Column('id', Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey('scripts.id'))
    regex = Column('regex', String, index=True, nullable=False)
    key = Column(String, index=True, nullable=False)


def get_session(dbref, create=False):
    engine = create_engine(dbref, encoding='utf8')
    if create:
        SqlBase.metadata.create_all(engine)  # issue DDL create
        #print 'Updated schema'
    session = sessionmaker(bind=engine)()
    return session


if __name__ == '__main__':
    import rc
    print ">>> dbref =", rc.dbref
    print ">>> get_session(dbref, create=True)"
    print get_session(rc.dbref, create=True)

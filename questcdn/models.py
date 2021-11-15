from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Column, Table, MetaData, Integer, String, DateTime, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def db_connect():
    """
        Performs database connection using database settings from settings.py.
        Returns sqlalchemy engine instance
        """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    page_url=Column("page_url",String(100))
    city_name = Column("city_name", String(100))
    agent_name = Column('agent_name', String(100))
    project_name = Column('project_name', String(100))
    project_number = Column('project_number', Integer)
    bid_due_date = Column('bid_due_date', DateTime)
    bid_open_date = Column('bid_open_date', DateTime)
    estimated_start_date = Column('estimated_start_date', DateTime)
    estimated_completion_date = Column('estimated_completion_date', DateTime)
    percent_completion = Column('percent_completion', Numeric)
    contract_amt = Column('contract_amt', Numeric)
    project_cntractor = Column('project_cntractor', String(100))
    constr_year = Column('constr_year', Integer)
    constr_type = Column('constr_type', String(100))
    district = Column('district', String(100))

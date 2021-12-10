from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Date, Time, BigInteger, ForeignKey, \
    Numeric, FLOAT
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

Base = automap_base()


def db_connect():
    """
        Performs database connection using database settings from settings.py.
        Returns sqlalchemy engine instance
        """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class DataAggregatorAgent(Base):
    __tablename__ = 'data_aggregator_agent'
    id = Column('data_aggregator_agent_id', Integer, primary_key=True)
    agent_name = Column('agent_name', String(200))
    site_url = Column('site_url', String(200))
    owner = Column('owner', String(200))
    last_run_date = Column('last_run_date', DateTime)
    source_system_id = Column('source_system_id', Integer)
    state_code = Column('state_code', String(100))
    auto_flag = Column('auto_flag', String(100))
    time_zone_id = Column('time_zone_id', Integer)
    tracking = relationship("Tracking")


class Error(Base):
    __tablename__ = 'agent_error'
    id = Column('agent_error_id', Integer, primary_key=True)
    error_code = Column('error_code', String(100))
    error_info = Column('error_info', String(1000))
    error_url = Column('error_url', String(200))
    tracking_id = Column('tracking_id', ForeignKey('agent_tracking.agent_tracking_id'))


class Tracking(Base):
    __tablename__ = 'agent_tracking'
    id = Column('agent_tracking_id', Integer, primary_key=True)
    spider_name = Column('spider_name', String(100))
    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime)
    total_records = Column('total_records', Integer)
    final_status = Column('final_status', String(100))
    extra_info = Column('extra_info', String(1000))
    data_aggregator_agent_id = Column('data_aggregator_agent_id',
                                      ForeignKey('data_aggregator_agent.data_aggregator_agent_id'))
    error = relationship("Error")


class ProjectStage(Base):
    __tablename__ = 'project_stage'
    id = Column(Integer, primary_key=True)
    plan_url = Column('plan_url', String(100))
    page_url = Column('page_url', String(100))
    bid_date = Column('bid_date', Date)
    bid_time = Column('bid_time', Time)
    job_description = Column('job_description', String(10000))
    bid_date_utc = Column('bid_date_utc', DateTime)
    state_code = Column('state_code', String(100))
    time_zone_id = Column('time_zone_id', String(100))
    owner = Column('owner', String(100))
    solicitor = Column('solicitor', String(100))
    contact_first_name = Column('contact_first_name', String(100))
    contact_last_name = Column('contact_last_name', String(100))
    phone_number = Column('phone_number', String(100))
    email_address = Column('email_address', String(100))
    county = Column('county', String(100))
    estimated_value = Column('estimated_value', BigInteger)
    owner_project_no = Column('owner_project_no', String(100))


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    page_url = Column("page_url", String(100))
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
    project_contractor = Column('project_contractor', String(100))
    constr_year = Column('constr_year', Integer)
    constr_type = Column('constr_type', String(100))
    district = Column('district', String(100))

# Base.prepare(db_connect(),reflect=True)

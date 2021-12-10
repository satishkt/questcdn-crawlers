from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Date, Time, BigInteger, ForeignKey
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
    agent_name = Column('agent_name', String)
    site_url = Column('site_url', String)
    owner = Column('owner', String)
    last_run_date = Column('last_run_date', DateTime)
    source_system_id = Column('source_system_id', Integer)
    state_code = Column('state_code', String)
    auto_flag = Column('auto_flag', String)
    time_zone_id = Column('time_zone_id', Integer)
    tracking = relationship("Tracking")


class Error(Base):
    __tablename__ = 'agent_error'
    id = Column('agent_error_id', Integer, primary_key=True)
    error_code = Column('error_code', String)
    error_info = Column('error_info', String)
    error_url = Column('error_url', String)
    tracking_id = Column('tracking_id', ForeignKey('agent_tracking.id'))


class Tracking(Base):
    __tablename__ = 'agent_tracking'
    id = Column('agent_tracking_id', Integer, primary_key=True)
    spider_name = Column('spider_name', String(100))
    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime)
    total_records = Column('total_records', Integer)
    final_status = Column('final_status', String(100))
    extra_info = Column('extra_info', String(1000))
    data_aggregator_agent_id = Column('data_aggregator_agent_id', ForeignKey('data_aggregator_agent.id'))
    error = relationship("Error")


class ProjectStage(Base):
    __tablename__ = 'project_stage'
    id = Column(Integer, primary_key=True)
    plan_url = Column('plan_url', String)
    page_url = Column('page_url', String)
    bid_date = Column('bid_date', Date)
    bid_time = Column('bid_time', Time)
    job_description = Column('job_description', String)
    bid_date_utc = Column('bid_date_utc', DateTime)
    state_code = Column('state_code', String)
    time_zone_id = Column('time_zone_id', String)
    owner = Column('owner', String)
    solicitor = Column('solicitor', String)
    contact_first_name = Column('contact_first_name', String)
    contact_last_name = Column('contact_last_name', String)
    phone_number = Column('phone_number', String)
    email_address = Column('email_address', String)
    county = Column('county', String)
    estimated_value = Column('estimated_value', BigInteger)
    owner_project_no = Column('owner_project_no', String)

# Base.prepare(db_connect(),reflect=True)

from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Date, Time, BigInteger
from sqlalchemy.ext.automap import automap_base

Base = automap_base()


def db_connect():
    """
        Performs database connection using database settings from settings.py.
        Returns sqlalchemy engine instance
        """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


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


class Error(Base):
    __tablename__ = 'agent_error'
    id = Column('agent_error_id', Integer, primary_key=True)
    created_date_time = Column('created_date_time', DateTime)
    created_by = Column('created_by', String)
    last_update_date_time = Column('last_update_date_time', DateTime)
    last_update_date_by = Column('last_update_date_by', String)
    run_id = Column('run_id', Integer)
    error_code = Column('error_code', String)
    error_info = Column('error_info', String)


class Setting(Base):
    __tablename__ = 'agent_setting'
    id = Column('agent_setting_id', Integer, primary_key=True)
    created_date_time = Column('created_date_time', DateTime)
    created_by = Column('created_by', String(100))
    last_update_date_time = Column('last_update_date_time', DateTime)
    last_update_date_by = Column('last_update_date_by', String)
    setting = Column('setting', String)


class Tracking(Base):
    __tablename__ = 'agent_tracking'
    id = Column('agent_tracking_id', Integer, primary_key=True)
    site_url = Column('site_url', String(100))
    created_date_time = Column('created_date_time', DateTime)
    created_by = Column('created_by', String(100))
    last_update_date_time = Column('last_update_date_time', DateTime)
    last_update_date_by = Column('last_update_date_by', String)
    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime)
    total_records = Column('total_records', Integer)


class Tracking_Info(Base):
    __tablename__ = 'agent_tacking_info'
    id = Column('agent_tracking_info_id', Integer, primary_key=True)
    created_date_time = Column('created_date_time', DateTime)
    created_by = Column('created_by', String(100))
    last_update_date_time = Column('last_update_date_time', DateTime)
    last_update_date_by = Column('last_update_date_by', String)
    tracking_info = Column('tracking_info', String)


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    page_url = Column("page_url", String(100))
    city_name = Column("city_name", String(100))
    agent_name = Column('agent_name', String(100))
    project_name = Column('project_name', String(100))
    project_number = Column('project_number', String(20))
    bid_due_date = Column('bid_due_date', DateTime)
    bid_open_date = Column('bid_open_date', DateTime)
    estimated_start_date = Column('estimated_start_date', DateTime)
    estimated_completion_date = Column('estimated_completion_date', DateTime)
    percent_completion = Column('percent_completion', Float)
    contract_amt = Column('contract_amt', Float)
    project_contractor = Column('project_contractor', String(100))
    constr_year = Column('constr_year', Integer)
    constr_type = Column('constr_type', String(100))
    district = Column('district', String(100))


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

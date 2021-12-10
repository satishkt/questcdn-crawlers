# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import datetime

import pytz
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker, Session

from questcdn.items import PlanetBidItem, QuestcdnItem
from questcdn.models import Project, ProjectStage


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)


class QuestcdnPipeline:

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        spider.log(f"Processing item from spider {spider.name} for url ={item['page_url']} ", logging.INFO)
        # Session = sessionmaker(bind=spider.engine)
        # session = Session()
        if isinstance(item, PlanetBidItem):
            self.create_project_stage_item(item)
        elif isinstance(item, QuestcdnItem):
            project = self.create_project_for_city_of_madison_item(item, spider)
        else:
            raise LookupError("Unknown item exception = " + type(item))

        return item

    def create_project_stage_item(self, item: PlanetBidItem, spider):
        project_stage = ProjectStage()
        project_stage.page_url = self.get_item_val_or_none('page_url', spider, item)
        project_stage.plan_url = self.get_item_val_or_none('main_url', spider, item)
        project_stage.job_description = self.get_item_val_or_none('job_description', spider, item)
        project_stage.bid_date = self.__get_date_from_date(self.get_item_val_or_none('bid_due_date', spider, item))
        project_stage.bid_time = self.__get_time_from_date(self.get_item_val_or_none('bid_due_date', spider, item))
        project_stage.bid_date_utc = self.__get_date_utc_from_date(
            self.get_item_val_or_none('bid_due_date', spider, item))
        project_stage.state_code = self.get_item_val_or_none('state_code', spider, item)
        project_stage.time_zone_id = self.__get_time_zone_id(self.get_item_val_or_none('bid_due_date', spider, item))
        project_stage.owner = self.get_item_val_or_none('owner', spider, item)
        project_stage.solicitor = self.get_item_val_or_none('solicitor', spider, item)
        project_stage.contact_last_name = self.get_item_val_or_none('contact_first_name', spider, item)
        project_stage.contact_last_name = self.get_item_val_or_none('contact_last_name', spider, item)
        project_stage.phone_number = self.get_item_val_or_none('contact_ph_no', spider, item)
        project_stage.email_address = self.get_item_val_or_none('contact_email_id', spider, item)
        project_stage.county = self.get_item_val_or_none('county', spider, item)
        project_stage.estimated_value = self.get_item_val_or_none('estimated_val', spider, item)
        project_stage.owner_project_no = self.get_item_val_or_none('owner_project_no', spider, item)
        line = json.dumps(project_stage.__dict__, cls=DateTimeEncoder) + "\n"
        self.file.write(line)

        pass

    @staticmethod
    def __get_time_zone_id(date_time):
        if date_time is not None:
            return date_time.tzinfo.tzname()

    @staticmethod
    def __get_date_from_date(date_time):
        if date_time is not None:
            return date_time.date()

    @staticmethod
    def __get_time_from_date(date_time):
        if date_time is not None:
            return date_time.time()

    @staticmethod
    def __get_date_utc_from_date(date_time):
        if date_time is not None:
            return date_time.astimezone(pytz.UTC)

    def create_project_for_city_of_madison_item(self, item, spider):
        """
        Database specific item for city of madison items.
        :param item:
        :param spider:
        :return:
        """
        project = Project()
        project.page_url = self.get_item_val_or_none('page_url', spider, item)
        project.city_name = self.get_item_val_or_none('city_name', spider, item)
        project.agent_name = self.get_item_val_or_none('agent_name', spider, item)
        project.project_number = self.get_item_val_or_none('project_number', spider, item)
        project.project_name = self.get_item_val_or_none('project_name', spider, item)
        project.bid_due_date = self.get_item_val_or_none('bid_due_date', spider, item)
        project.bid_open_date = self.get_item_val_or_none('bid_open_date', spider, item)
        project.constr_type = self.get_item_val_or_none('constr_type', spider, item)
        project.constr_year = self.get_item_val_or_none('constr_year', spider, item)
        project.contract_amt = self.get_item_val_or_none('contract_amt', spider, item)
        project.estimated_start_date = self.get_item_val_or_none('estimated_start_date', spider, item)
        project.estimated_completion_date = self.get_item_val_or_none('estimated_completion_date', spider, item)
        project.percent_completion = self.get_item_val_or_none('percent_completion', spider, item)
        project.project_contractor = self.get_item_val_or_none('project_contractor', spider, item)
        project.district = self.get_item_val_or_none('district', spider, item)
        return project

    @staticmethod
    def get_item_val_or_none(key, spider, item):
        if key in item:
            return item[key]
        else:
            spider.log(f"Unable to find {key} for {item} in spider {spider.name} for url {item['page_url']}",
                       logging.WARN)
            return None

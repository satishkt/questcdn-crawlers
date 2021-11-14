# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker

from questcdn.models import db_connect, create_table, Project


class QuestcdnPipeline:

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        project = Project()
        project.city_name = item['city_name']
        project.agent_name = item['agent_name']
        project.project_number = item['project_number']
        project.project_name = item['project_name']
        project.bid_due_date = item['bid_due_date']
        project.bid_open_date = item['bid_open_date']
        project.constr_type = item['constr_type']
        project.constr_year = item['constr_year']
        project.contract_amt = item['contract_amt']
        project.estimated_start_date = item['estimated_start_date']
        project.estimated_completion_date = item['estimated_completion_date']
        project.percent_completion = item['percent_completion']
        project.district = item['district']

        try:
            session.add(project)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
        # pass

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from sqlalchemy.orm import sessionmaker

from questcdn.models import Project


class QuestcdnPipeline:

    def process_item(self, item, spider):
        spider.log(f"Processing item from spider {spider.name} for url ={item['page_url']} ", logging.INFO)
        session = sessionmaker(bind=spider.engine)
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

    def get_item_val_or_none(self, key, spider, item):
        if key in item:
            return item[key]
        else:
            spider.log(f"Unable to find {key} for {item} in spider {spider.name} for url {item['page_url']}",
                       logging.WARN)
            return None

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import logging
from scrapy import signals


class QuestcdnPipeline:

    def __init__(self):
        self.create_connection()
        self.items = []
        # self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'mpassword',
            database = 'crawling'
        )
        self.curr = self.conn.cursor()

    # def create_table(self):
    #     self.curr.execute("""create table scraped_info1(
    #                     title text,
    #                     author text,
    #                     tag text
    #                     )""")

    def process_item(self, item, spider):
        # item['agent_name'] = item['agent_name'] if item['agent_name'] is not None else 'NA'
        # item['bid_due_date'] = item['bid_due_date'] if item['bid_due_date'] != 'Not Available' else 'NA'
        # item['contract_amt'] = item['contract_amt'][1:].replace(',', '') if item['contract_amt'] != 'Not Available' else '0.00',
        # item['estimated_start_date'] = item['estimated_start_date'] if item['estimated_start_date'] != 'Not Available' else 'NA'

        # item['agent_name'] = item['agent_name'] if item['agent_name'] is not None else 'NA',
        # item['project_name'] = item['project_name'] if item['project_name'] is not None else 'NA',
        # item['project_number'] = item['project_number'] if item['project_number'] is not None else 'NA',
        # item['bid_due_date'] = item['bid_due_date'] if item['bid_due_date'] is not None else 'NA',
        # item['bid_open_date'] = item['bid_open_date'] if item['bid_open_date'] is not None else 'NA',
        # item['estimated_start_date'] = item['estimated_start_date'] if item['estimated_start_date'] is not None else 'NA',
        # item['estimated_completion_date'] = item['estimated_completion_date'] if item['estimated_completion_date'] is not None else 'NA',
        # item['percent_completion'] = item['percent_completion'] if item['percent_completion'] is not None else 'NA',
        # item['contract_amt'] = item['contract_amt'] if item['contract_amt'] is not None else 'NA',
        # item['project_cntractor'] = item['project_cntractor'] if item['project_cntractor'] is not None else 'NA',
        # item['constr_year'] = item['constr_year'] if item['constr_year'] is not None else 'NA',
        # item['constr_type'] = item['constr_type'] if item['constr_type'] is not None else 'NA',
        # item['district'] = item['district'] if item['district'] is not None else 'NA'

        self.store_db(item, spider)
        return item
        # pass

    def store_db(self, item, spider):
        # self.placholders = ', '.joins(['%s'] * len(item))
        # self.columns = ', '.join(item.keys())
        # self.query = "INSERT INTO %s (%s) VALUES (%s)" % ("scraped_info1", self.columns, self.placeholders)
        #
        # self.items.extend([item.values()])
        #
        # spider.cursor.executemany(self.query, self.items)
        # self.items = []
        # print("insert into scraped_info values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (item['agent_name'],
        #                                                                                     item['bid_due_date'],
        #                                                                                     item['bid_open_date'],
        #                                                                                     item['constr_year'],
        #                                                                                     item['constr_type'],
        #                                                                                     item['contract_amt'],
        #                                                                                     item['district'],
        #                                                                                     item[
        #                                                                                         'estimated_completion_date'],
        #                                                                                     item[
        #                                                                                         'estimated_start_date'],
        #                                                                                     item['percent_completion'],
        #                                                                                     item['project_cntractor'],
        #                                                                                     item['project_name'],
        #                                                                                     item['project_number']
        #                                                                                     ))

        self.curr.execute("""insert into scraped_info1 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item['agent_name'],
            item['bid_due_date'],
            item['bid_open_date'],
            item['constr_year'],
            item['constr_type'],
            item['contract_amt'],
            item['district'],
            item['estimated_completion_date'],
            item['estimated_start_date'],
            item['percent_completion'],
            item['project_cntractor'],
            item['project_name'],
            item['project_number'],

        ))
        self.conn.commit()

        # q = """insert into scraped_info values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        #
        # try:
        #     self.curr.executemany(q, item)
        #     self.conn.commit()
        # except:
        #     self.conn.rollback()



    # def store_db(self,item):
    #     self.curr.execute("""insert into scraped_info values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,(
    #         item['agent_name'] = item['agent_name'] if item['agent_name'] is not None else 'NA',
    #         item['project_name'] = item['project_name'] if item['project_name'] is not None else 'NA',
    #         item['project_number'] = item['project_number'] if item['project_number'] is not None else 'NA',
    #         item['bid_due_date'] = item['bid_due_date'] if item['bid_due_date'] is not None else 'NA',
    #         item['bid_open_date'] = item['bid_open_date'] if item['bid_open_date'] is not None else 'NA',
    #         item['estimated_start_date'] = item['estimated_start_date'] if item['estimated_start_date'] is not None else 'NA',
    #         item['estimated_completion_date'] = item['estimated_completion_date'] if item['estimated_completion_date'] is not None else 'NA',
    #         item['percent_completion'] = item['percent_completion'] if item['percent_completion'] is not None else 'NA',
    #         item['contract_amt'] = item['contract_amt'] if item['contract_amt'] is not None else 'NA',
    #         item['project_cntractor'] = item['project_cntractor'] if item['project_cntractor'] is not None else 'NA',
    #         item['constr_year'] = item['constr_year'] if item['constr_year'] is not None else 'NA',
    #         item['constr_type'] = item['constr_type'] if item['constr_type'] is not None else 'NA',
    #         item['district'] = item['district'] if item['district'] is not None else 'NA'
    #     ))
    #     self.conn.commit()

    # def process_item(self, item, spider):
    #     self.placeholders = ', '.join(['%s'] * len(item))
    #     self.columns = ', '.join(item.keys())
    #     self.query = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("scraped_info", self.columns, self.placeholders)
    #
    #     self.items.extend([item.values()])
    #
    #     if len(self.items) >= 1:
    #
    #         try:
    #             spider.curr.executemany(self.query, self.items)
    #             self.items = []
    #         except Exception as e:
    #             if 'MySQL server has gone away' in str(e):
    #                 # spider.connectDB()
    #                 spider.curr.executemany(self.query, self.items)
    #                 self.items = []
    #             else:
    #                 raise e
    #
    #
    #     return item
    #
    #
    # def close_spider(self, spider):
    #     try:
    #         spider.curr.executemany(self.query, self.items)
    #         self.items = []
    #     except Exception as e:
    #         if 'MySQL server has gone away' in str(e):
    #             # spider.connectDB()
    #             spider.cursor.executemany(self.query, self.items)
    #             self.items = []
    #         else:
    #             raise e
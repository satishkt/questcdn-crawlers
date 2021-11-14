# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestcdnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    agent_name = scrapy.Field()
    project_name = scrapy.Field()
    project_number = scrapy.Field()
    bid_due_date = scrapy.Field()
    bid_open_date = scrapy.Field()
    estimated_start_date = scrapy.Field()
    estimated_completion_date = scrapy.Field()
    percent_completion = scrapy.Field()
    contract_amt = scrapy.Field()
    project_cntractor = scrapy.Field()
    constr_year = scrapy.Field()
    constr_type = scrapy.Field()
    district = scrapy.Field()
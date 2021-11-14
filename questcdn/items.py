# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item
from itemloaders.processors import MapCompose, TakeFirst


def remove_spaces(text):
    return text.strip()


class QuestcdnItem(Item):
    # define the fields for your item here like:
    city_name=Field()
    agent_name = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    project_name = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    project_number = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    bid_due_date = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    bid_open_date = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    estimated_start_date = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    estimated_completion_date = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    percent_completion = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    contract_amt = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    project_cntractor = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    constr_year = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    constr_type = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    district = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())

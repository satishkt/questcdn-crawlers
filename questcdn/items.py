# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime, date
from re import sub
from decimal import Decimal


def parse_date_format1(text):
    if text in ['Not Available', 'Future Project']:
        return date(year=9999, month=12, day=31)
    else:
        return datetime.strptime(text, '%m/%d/%y')


def parse_date_format2(text):
    if text in ['Not Available', 'Future Project']:
        return date(year=9999, month=12, day=31)
    else:
        return datetime.strptime(text, '%m/%d/%Y')


def fix_unavailable_date(text):
    if text in ['Not Available', 'Future Project'] or text is None:
        return date(year=9999, month=12, day=31)
    else:
        return datetime.strptime(text, '%m/%d/%Y')


def fix_percent_complete(text):
    if 'Not Available' in text:
        return 9999.99
    elif '%' in text:
        return float(text.replace('%', '').strip())
    else:
        return float(text.strip('"'))


def fix_dollar_value(text):
    if 'Not Available' in text:
        return Decimal(0)
    elif '$' in text:
        value = Decimal(sub(r'[^\d.]', '', text))
        return value
    else:
        return Decimal(text)


def remove_spaces(text):
    return text.strip()


class QuestcdnItem(Item):
    # define the fields for your item here like:
    page_url=Field(output_processor=TakeFirst())
    city_name = Field(output_processor=TakeFirst())
    agent_name = Field(output_processor=TakeFirst())
    project_name = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    project_number = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    bid_due_date = Field(input_processor=MapCompose(remove_spaces, parse_date_format1), output_processor=TakeFirst())
    bid_open_date = Field(input_processor=MapCompose(remove_spaces, parse_date_format2), output_processor=TakeFirst())
    estimated_start_date = Field(input_processor=MapCompose(remove_spaces, parse_date_format2),
                                 output_processor=TakeFirst())
    estimated_completion_date = Field(input_processor=MapCompose(remove_spaces, fix_unavailable_date),
                                      output_processor=TakeFirst())
    percent_completion = Field(input_processor=MapCompose(remove_spaces, fix_percent_complete),
                               output_processor=TakeFirst())
    contract_amt = Field(input_processor=MapCompose(remove_spaces, fix_dollar_value), output_processor=TakeFirst())
    project_contractor = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    constr_year = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    constr_type = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    district = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())

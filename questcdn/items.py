# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import pytz
import pyap

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


def find_state(text):
    addresses = pyap.parse(text, country='US')
    if len(addresses) > 0:
        get_add_1 = addresses[0]
        return get_add_1.as_dict()['region']


def parse_bid_posting_date(text):
    """
    bid posting date looks like '09/29/2021 11:16 AM (PST)'
    Remove the (PST) string before parsing
    :param text:
    :return:
    """
    fmt = '%m/%d/%Y %I:%M %p'
    if 'PST' in text:
        bid_p_date = text[:-5].strip()
        pst_tz = pytz.timezone("America/Los_Angeles")
        return pst_tz.localize(datetime.strptime(bid_p_date, fmt))
    elif 'EST' in text:
        bid_p_date = text[:-5].strip()
        est_tz = pytz.timezone("US/Eastern")
        return est_tz.localize(datetime.strptime(bid_p_date, fmt))
    return datetime.strptime(text, fmt)


def clean_up_first_last_name(text):
    email = parse_email_from_contact_deets(text)
    phone_no = parse_ph_no_from_contact_details(text)
    text = text.replace(email, '').strip()
    text = text.replace(phone_no, '').strip()
    return text


def parse_email_from_contact_deets(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    if match is not None:
        return match.group(0)
    else:
        return ''


def parse_ph_no_from_contact_details(text):
    match = re.search(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b", text)
    if match is None:
        return ''
    return match.group(0)


class QuestcdnItem(Item):
    # define the fields for your item here like:
    page_url = Field(output_processor=TakeFirst())
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


class PlanetBidItem(Item):
    main_url = Field(output_processor=TakeFirst())
    page_url = Field(output_processor=TakeFirst())
    project_title = Field(input_processor=MapCompose(remove_spaces, output_processor=TakeFirst()))
    job_description = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    bid_due_date = Field(input_processor=MapCompose(remove_spaces, parse_bid_posting_date),
                         output_processor=TakeFirst())
    state_code = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    owner = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    solicitor = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    contact_first_name = Field(input_processor=MapCompose(remove_spaces, clean_up_first_last_name),
                               output_processor=TakeFirst())
    contact_last_name = Field(input_processor=MapCompose(remove_spaces, clean_up_first_last_name),
                              output_processor=TakeFirst())
    contact_ph_no = Field(input_processor=MapCompose(remove_spaces, parse_ph_no_from_contact_details),
                          output_processor=TakeFirst())
    contact_email_id = Field(input_processor=MapCompose(remove_spaces, parse_email_from_contact_deets),
                             output_processor=TakeFirst())
    county = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    estimated_val = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    owner_project_no = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())
    bid_posting_date = Field(output_processor=TakeFirst(),
                             input_processor=MapCompose(remove_spaces, parse_bid_posting_date))
    project_stage = Field(input_processor=MapCompose(remove_spaces), output_processor=TakeFirst())

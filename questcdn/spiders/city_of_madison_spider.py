import scrapy
from scrapy.loader import ItemLoader

from questcdn.items import QuestcdnItem
from questcdn.spiders.base_spider import BaseQuestCDNSpider


class CityOfMadisonSpider(BaseQuestCDNSpider):
    name = "city_of_madison"
    start_urls = ["https://cityofmadison.com/business/pw/contracts/"]

    def __init__(self, **kwargs):
        super(CityOfMadisonSpider, self).__init__(**kwargs)

    def parse(self, response, **kwargs):
        for page_href in response.xpath("//table[@class='border']/tr/td/a/@href").getall():
            if 'details.cfm?ContractNumber' in page_href:
                self.logger.info(f"Processing child page - {page_href} ")
                yield response.follow(page_href, callback=self.parse_child_page)
            else:
                self.logger.warn(f'Not a valid child page url {page_href}')

    def parse_child_page(self, response):
        data_table = response.xpath("//div[@class='box']/div[@class='box_body']/table")
        loader = ItemLoader(item=QuestcdnItem(), selector=data_table)
        loader.add_value("page_url", response.request.url)
        loader.add_value("city_name", "city_of_madison")
        loader.add_value('agent_name', 'city_of_madison')
        loader.add_xpath('project_name', './tr[1]/td[2]/text()')
        loader.add_xpath('project_number', './tr[2]/td[2]/text()')
        loader.add_xpath('bid_due_date', './tr[3]/td[2]/text()')
        loader.add_xpath('bid_open_date', './tr[4]/td[2]/text()')
        loader.add_xpath('estimated_start_date', './tr[5]/td[2]/text()')
        loader.add_xpath('estimated_completion_date', './tr[6]/td[2]/text()')
        loader.add_xpath('percent_completion', './tr[7]/td[2]/text()')
        loader.add_xpath('contract_amt', './tr[8]/td[2]/text()')
        loader.add_xpath('project_contractor', './tr[9]/td[2]/text()')
        loader.add_xpath('constr_year', './tr[10]/td[2]/text()')
        loader.add_xpath('constr_type', './tr[11]/td[2]/text()')
        loader.add_xpath('district', './tr[12]/td[2]/text()')
        yield loader.load_item()

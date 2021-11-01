import scrapy

from questcdn.items import QuestcdnItem


class CityOfMadisonSpider(scrapy.Spider):
    name = "city_of_madison"
    start_urls = ["https://cityofmadison.com/business/pw/contracts/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for page_href in response.xpath("//table[@class='border']/tr/td/a/@href").getall():
            yield response.follow(page_href, callback=self.parse_child_page)

    def parse_child_page(self, response):
        data_table = response.xpath("//div[@class='box']/div[@class='box_body']/table")
        item = QuestcdnItem()
        item['agent_name'] = self.name
        item['project_name'] = data_table.xpath('./tr[1]/td[2]/text()').extract_first().strip()
        item['project_number'] = data_table.xpath('./tr[2]/td[2]/text()').extract_first().strip()
        item['bid_due_date'] = data_table.xpath('./tr[3]/td[2]/text()').extract_first().strip()
        item['bid_open_date'] = data_table.xpath('./tr[4]/td[2]/text()').extract_first().strip()
        item['estimated_start_date'] = data_table.xpath('./tr[5]/td[2]/text()').extract_first().strip()
        item['estimated_completion_date'] = data_table.xpath('./tr[6]/td[2]/text()').extract_first().strip()
        item['percent_completion'] = data_table.xpath('./tr[7]/td[2]/text()').extract_first().strip()
        item['contract_amt'] = data_table.xpath('./tr[8]/td[2]/text()').extract_first().strip()
        item['project_cntractor'] = data_table.xpath('./tr[9]/td[2]/text()').extract_first().strip()
        item['constr_year'] = data_table.xpath('./tr[10]/td[2]/text()').extract_first().strip()
        item['constr_type'] = data_table.xpath('./tr[11]/td[2]/text()').extract_first().strip()
        item['district'] = data_table.xpath('./tr[12]/td[2]/text()').extract_first().strip()
        yield item

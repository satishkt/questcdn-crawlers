import os
from typing import List

from scrapy import Request
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from questcdn.spiders.base_spider import BaseQuestCDNSpider


class PlanetBidSpider(BaseQuestCDNSpider):
    name = 'planet_bid_spider'
    start_urls = ['https://pbsystem.planetbids.com/portal/24054/bo/bo-search']

    def __init__(self, **kwargs):
        super(PlanetBidSpider, self).__init__(self.name, **kwargs)
        binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        options = webdriver.FirefoxOptions()
        options.add_argument("headless")
        to_capabilities = options.to_capabilities()
        self.driver = webdriver.Firefox(firefox_binary=binary,
                                        executable_path="D:\\WebDrivers\\geckodriver.exe",
                                        desired_capabilities=to_capabilities)

    def start_requests(self):
        self.logger.info(f'Starting the spider - {self.name}')
        for url in self.start_urls:
            self.logger.info(f"Checking if the url {url} is enabled for scraping ")
            should_scrape = True  # self.check_if_agent_is_to_be_scraped(url)
            if should_scrape:
                yield Request(url=url, callback=self.parse)
            else:
                self.logger.warning(f"URL {url}  is not enabled for scraping, exiting")

    def parse(self, response, **kwargs):
        try:
            print(f"Fetching data from url {response.url}")
            self.driver.get(response.url)
            self.driver.implicitly_wait(10)
            bidding_invitation_elements:List[WebElement] = self.driver.find_elements(By.XPATH,
                                                                    '//tr[@class="row-highlight  stageStr-bidding byInvitation-false ember-view"]')
            closed_invitation_elements:List[WebElement] = self.driver.find_elements(By.XPATH,
                                                                   '//tr[@class="row-highlight  stageStr-closed byInvitation-false ember-view"]')

            canceled_invitation_elements:List[WebElement] = self.driver.find_elements(By.XPATH,
                                                                     '//tr[@class="row-highlight  stageStr-canceled byInvitation-false ember-view"]')

            awarded_invitation_elements:List[WebElement] = self.driver.find_elements(By.XPATH,
                                                                    '//tr[@class="row-highlight  stageStr-awarded byInvitation-false ember-view"]')


            for element in bidding_invitation_elements:
                columns:[WebElement] =element.find_elements_by_tag_name("td")
                for value in columns:
                    col_val = value.get_attribute("title")
                    print(col_val)

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()

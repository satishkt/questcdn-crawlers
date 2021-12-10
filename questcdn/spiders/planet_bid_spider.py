from typing import List

from scrapy import Request
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.remote.webelement import WebElement

from questcdn.items import PlanetBidItem
from questcdn.spiders.base_spider import BaseQuestCDNSpider


class PlanetBidSpider(BaseQuestCDNSpider):
    name = 'planet_bid_spider'
    start_urls = ['https://pbsystem.planetbids.com/portal/15927/bo/bo-search']

    def __init__(self, **kwargs):
        super(PlanetBidSpider, self).__init__(self.name, **kwargs)

    def create_web_driver(self):
        binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_binary=binary,
                                   executable_path="D:\\WebDrivers\\geckodriver.exe",
                                   options=options)
        return driver

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
        driver = self.create_web_driver()
        try:
            self.logger.info(f"Fetching data from url {response.url} for main page")
            driver.get(response.url)
            driver.implicitly_wait(10)
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

            bidding_invitation_elements: List[WebElement] = driver.find_elements(By.XPATH,
                                                                                 '//tr[@class="row-highlight  stageStr-bidding byInvitation-false ember-view"]')
            closed_invitation_elements: List[WebElement] = driver.find_elements(By.XPATH,
                                                                                '//tr[@class="row-highlight  stageStr-closed byInvitation-false ember-view"]')

            canceled_invitation_elements: List[WebElement] = driver.find_elements(By.XPATH,
                                                                                  '//tr[@class="row-highlight  stageStr-canceled byInvitation-false ember-view"]')

            awarded_invitation_elements: List[WebElement] = driver.find_elements(By.XPATH,
                                                                                 '//tr[@class="row-highlight  stageStr-awarded byInvitation-false ember-view"]')
            self.logger.info(
                f"For URL {response.url} , retrieved {len(bidding_invitation_elements)} - bidding invitation elements, {len(closed_invitation_elements)} - closed invitation elements"
                f"{len(canceled_invitation_elements)} - canceled invitation elements and {len(awarded_invitation_elements)} - awarded invitation elements")
            for row in bidding_invitation_elements:
                yield from self.__process_row_data(response, row)

            # for row in closed_invitation_elements:
            #     yield from self.__process_row_data(response, row)
            #
            # for row in canceled_invitation_elements:
            #     yield from self.__process_row_data(response, row)
            #
            # for row in awarded_invitation_elements:
            #     yield from self.__process_row_data(response, row)
        except Exception as e:
            self.logger.error("Error parsing data from planet bids page.", exc_info=True)
        finally:
            self.logger.info("Exiting the driver")
            driver.close()
            driver.quit()

    def __process_row_data(self, response, row):
        child_page_id = row.get_attribute('rowattribute')
        remaining_element = row.find_element(By.XPATH, f'//td[@data-itemid="{child_page_id}"]/span')
        remaining_days = remaining_element.text
        detail_url = response.url[:response.url.rfind('/')] + '/bo-detail'
        self.logger.info(f"Processing child page - {detail_url}/{child_page_id} with days remaining = {remaining_days}")
        yield response.follow(f'{detail_url}/{child_page_id}', callback=self.parse_child_page,
                              cb_kwargs={"days_remaining": remaining_days, "main_url": response.url})

    def parse_child_page(self, response, days_remaining, main_url):
        driver = self.create_web_driver()
        try:
            self.logger.info(f"Processing child page from url {response.url} with input params {days_remaining}")
            driver.get(response.url)
            driver.implicitly_wait(5)
            all_rows = driver.find_elements(By.XPATH,
                                            '//div[@class="bid-detail-wrapper"]/div[@class="ember-view"]/div[@class="ember-view"]')
            loader = ItemLoader(item=PlanetBidItem())
            loader.add_value('main_url', main_url)
            loader.add_value('page_url', response.url)
            for row in all_rows:
                label = row.find_element(By.XPATH,
                                         './/div[@class="col-12 col-sm-3 col-lg-2 bid-detail-item-title"]').text
                value = row.find_element(By.XPATH,
                                         './/div[@class="col-12 col-sm-8 col-lg-9 bid-detail-item-value"]').text
                loader.add_value('page_url', response.url)
                if label is not None and value is not None:
                    label = label.strip()
                    value = value.strip()
                    if label == 'Project Title':
                        loader.add_value('project_title', value)
                    if label == 'Invitation #':
                        loader.add_value('owner_project_no', value)
                    if label == 'Scope of Services':
                        loader.add_value('job_description', value)
                    if label == 'Bid Due Date':
                        loader.add_value('bid_due_date', value)
                    if label == 'Address':
                        loader.add_value('state_code', value)
                    if label == 'owner':
                        loader.add_value('owner', value)
                    if label == 'Contact Info':
                        loader.add_value('contact_first_name', value)
                    if label == 'Contact Info':
                        loader.add_value('contact_last_name', value)
                    if label == 'Contact Info':
                        loader.add_value('contact_ph_no', value)
                    if label == 'Contact Info':
                        loader.add_value('contact_email_id', value)
                    if label == 'County':
                        loader.add_value('county', value)
                    if label == 'estimated_val':
                        loader.add_value('estimated_val', value)
                    if label == 'Bid Posting Date':
                        loader.add_value('bid_posting_date', value)
                    if label == 'owner_project_no':
                        loader.add_value('owner_project_no', value)
                    if label == 'project_stage':
                        loader.add_value('project_stage', value)
                self.logger.info(f"Finishing extracting elements from child page {response.url}, Closing the window")
            driver.close()
            return loader.load_item()
        except Exception as e:
            self.logger.error("Error parsing data from planet bids page.", exc_info=True)
        finally:
            driver.quit()

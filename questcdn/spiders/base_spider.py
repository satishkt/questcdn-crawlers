from datetime import datetime

import scrapy
from scrapy import signals
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session, aliased
from sqlalchemy.orm.sync import update

from questcdn.models import db_connect, DataAggregatorAgent, Tracking


class BaseQuestCDNSpider(scrapy.Spider):
    name = "base_quest_cdn_spider"

    def __init__(self, name, **kwargs):
        super(BaseQuestCDNSpider, self).__init__(name=self.name, **kwargs)
        ## Set up the database core connection/engine here. This engine is shared across all db calls and is passed as a spider attribute.
        self.engine = db_connect()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Use the scrapy signals API to track all these events and perform operations whenever these call back events happen
        :param crawler:
        :param args:
        :param kwargs:
        :return:
        """
        spider = super(BaseQuestCDNSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.engine_started, signal=signals.engine_started)
        crawler.signals.connect(spider.engine_stopped, signal=signals.engine_stopped)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.item_error, signal=signals.item_error)
        crawler.signals.connect(spider.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_error, signal=signals.spider_error)
        return spider

        ####################### Call back methods that will be invoked ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def engine_started(self):
        self.logger.info(f"Starting Engine for spider {self.name}")
        pass

    def engine_stopped(self):
        self.logger.info(f"Stopping Engine for spider {self.name}")
        pass

    def item_scraped(self, item, spider, response):
        self.logger.info(f"Spider {spider.name} has finished scraping item {item}")
        pass

    def item_error(self, item, response, spider, failure):
        pass

    def item_dropped(self, item, response, exception, spider):
        pass

    def spider_opened(self, spider):
        self.scraping_begin(spider)
        pass

    def spider_closed(self, spider, reason):
        self.scraping_end(spider, reason)
        pass

    def spider_error(self, failure, response, spider):
        self.scraping_failed(spider, failure, response)
        pass

    ####################### Call back methods that will be invoked END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def check_if_agent_is_to_be_scraped(self, agent_url) -> bool:
        """
        This method checks if the url provided is enabled for scraping.
        Check the data aggregator agent table to see if this url is active and needs to be scraped.
        :return:
        """
        self.logger.info(f"Checking to see if {agent_url} is enabled for scraping")
        with Session(self.engine) as session:
            agent = aliased(DataAggregatorAgent, name="agent")
            stmt = select(agent).where(agent.site_url == agent_url)
            result = session.execute(stmt)
            row = result.fetchone()
            self.logger.info(row.agent.auto_flag)
            print(row.agent.auto_flag)

            if row.agent.auto_flag is None or row.agent.auto_flag != 'N':
                self.logger.info(f"Agent URL = {agent_url} is enabled for scraping")
                return False
            else:
                self.logger.info(f"Agent URL = {agent_url} is not enabled for scraping")
                return False

    def scraping_begin(self, spider):
        """
                This methods adds an entry into the tracking table to track the start of scraping process.
                :return:
        """
        # TODO - Create an entry in the tracking table, get the tracking ID and store it in a local class variable.

        self.logger.info(f"Starting to scrape with spider {spider.name}")
        tracking = Tracking()
        scraped_urls = ','.join(spider.start_urls)
        tracking.site_url = scraped_urls
        tracking.start_time = datetime.now()
        tracking.created_date_time = datetime.now()
        with Session(self.engine) as session:
            session.add(tracking)
            session.flush()
            self.logger.info(f"Inserted tracking id is {tracking.id}")
            self.tracking_id = tracking.id
            session.commit()

    def scraping_end(self, spider, reason):
        """
        This method adds an entry into the tracking table to record that the spider has finished the scraping process.
        :param spider:
        :param reason:
        :return:
        """
        self.logger.info(f"Ending Spider  Tracking session for spider {spider.name} with tracking id {self.tracking_id}")
        with Session(self.engine) as session:
            tracking_end_time = datetime.now()
            tracking = session.query(Tracking).filter(Tracking.id == self.tracking_id).one()
            tracking.end_time = tracking_end_time
            session.commit()
            self.logger.info(
                f"Ending tracking session for tracking id {self.tracking_id} at {tracking_end_time} with reason as {reason}")

    def scraping_failed(self, spider, reason, response):
        """
        This method adds an entry into the error_info table with error_code as SPIDER_ERROR
        :param spider:
        :param reason:
        :return:
        """
        # TODO - Use the local class variable for tracking id and add an entry in the errors table with error code as SPIDER_ERROR and the error reason as a JSON formatted string,response has the URL where the spider crashed.
        pass

    def item_failure(self, spider, response, exception):
        """
        This method adds an entry into the error_info table with error_code as ITEM_ERROR
        :param spider:
        :param response:
        :param exception:
        :return:
        """
        # TODO - Use the local class variable for tracking id , add an entry into the errors table with error code as ITEM_ERROR and the error reason as generated exception from the JSON.

        pass

    def start_requests(self):
        self.logger.info(f'Starting the spider - {self.name}')
        for url in self.start_urls:
            self.logger.info(f"Checking if the url {url} is enabled for scraping ")
            should_scrape = self.check_if_agent_is_to_be_scraped(url)
            if should_scrape:
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                self.logger.warning(f"URL {url}  is not enabled for scraping, exiting")

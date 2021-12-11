import uuid
from datetime import datetime

import scrapy
from scrapy import signals
from sqlalchemy import select
from sqlalchemy.orm import aliased

from questcdn.models import DataAggregatorAgent, Tracking, Error, db_session, create_table


class BaseQuestCDNSpider(scrapy.Spider):
    name = "base_quest_cdn_spider"

    def __init__(self, name, **kwargs):
        super(BaseQuestCDNSpider, self).__init__(name=self.name, **kwargs)
        create_table()
        self.track_id = str(uuid.uuid1())

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

    def engine_stopped(self):
        self.logger.info(f"Stopping Engine for spider {self.name}")

    def item_scraped(self, item, spider, response):
        self.logger.info(f"Spider {spider.name} has finished scraping item {item}")

    def item_error(self, item, response, spider, failure):
        self.item_failure(spider, item, response, exception=failure)

    def item_dropped(self, item, response, exception, spider):
        self.item_failure(spider, item, response, exception=exception)

    def spider_opened(self, spider):
        self.scraping_begin(spider)

    def spider_closed(self, spider, reason):
        self.scraping_end(spider, reason)

    def spider_error(self, failure, response, spider):
        self.scraping_failed(spider, failure, response)

    ####################### Call back methods that will be invoked END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def find_tracker_row(self, track_id, session) -> Tracking:
        track = aliased(Tracking, name='track')
        stmt = select(track).where(track.track_id == track_id)
        row = session.execute(stmt).fetchone()
        return row.track

    def check_if_agent_is_to_be_scraped(self, agent_url) -> bool:
        """
        This method checks if the url provided is enabled for scraping.
        Check the data aggregator agent table to see if this url is active and needs to be scraped.
        :return:
        """
        self.logger.info(f"Checking to see if {agent_url} is enabled for scraping")
        session = db_session()
        with session, session.begin():
            agent = aliased(DataAggregatorAgent, name="agent")
            stmt = select(agent).where(agent.site_url == agent_url)
            result = session.execute(stmt)
            row = result.fetchone()
            if row is not None:
                self.logger.info(f"Data aggregator agent flag for {agent_url} is {row.agent.auto_flag}")
                if row.agent.auto_flag is 'Y':
                    self.logger.info(f"Agent URL = {agent_url} is enabled for scraping")
                    return True
                else:
                    self.logger.info(f"Agent URL = {agent_url} is not enabled for scraping")
                    return False
            else:
                self.logger.warning(f"No entry found in data aggregator agent for url {agent_url}")

    def scraping_begin(self, spider):
        """
                This methods adds an entry into the tracking table to track the start of scraping process.
                :return:
        """
        self.logger.info(f"Starting to scrape with spider {spider.name}")
        tracking = Tracking()
        tracking.spider_name = spider.name
        tracking.start_time = datetime.now()
        tracking.created_date_time = datetime.now()
        tracking.track_id = self.track_id
        self.logger.info(f"Inserted tracking id is {self.track_id}")
        session = db_session()
        with session, session.begin():
            session.add(tracking)
            session.commit()

    def scraping_end(self, spider, reason):
        """
        This method adds an entry into the tracking table to record that the spider has finished the scraping process.
        :param spider:
        :param reason:
        :return:
        """
        self.logger.info(
            f"Ending Spider  Tracking session for spider {spider.name} with tracking id {self.track_id}")
        session = db_session()
        with session, session.begin():
            tracking = self.find_tracker_row(self.track_id, session)
            tracking_end_time = datetime.now()
            tracking.end_time = tracking_end_time
            tracking.final_status = 'NO_ISSUES'
            self.logger.info(
                f"Ending tracking session for tracking id {self.track_id} at {tracking_end_time} with reason as {reason}")
            session.commit()

    def scraping_failed(self, spider, reason, response):
        """
        This method adds an entry into the error_info table with error_code as SPIDER_ERROR
        :param spider:
        :param reason:
        :return:
        """
        self.logger.info(
            f"Ending Spider  Tracking session for spider {spider.name} with tracking id {self.track_id}")
        session = db_session()
        with session, session.begin():
            tracking = self.find_tracker_row(self.track_id, session)
            tracking_end_time = datetime.now()
            tracking.end_time = tracking_end_time
            tracking.final_status = 'FAILED'
            tracking.extra_info = reason
            self.logger.info(
                f"Ending tracking session for tracking id {self.track_id} at {tracking_end_time} with reason as {reason} and response {response}")
            session.commit()

        pass

    def item_failure(self, item, spider, response, exception):
        """
        This method adds an entry into the error_info table with error_code as ITEM_ERROR
        :param spider:
        :param response:
        :param exception:
        :return:
        """
        session = db_session()
        with session, session.begin():
            self.logger.error(
                f"Logging item failed error from {spider.name} for item {item}, with exception = {str(exception)} and response = {response}")
            item_failure_error = Error()
            tracking = self.find_tracker_row(self.track_id, session)
            item_failure_error.tracking_id = tracking.id
            item_failure_error.error_url = response.url
            item_failure_error.item_info = item
            item_failure_error.error_info = str(exception)
            item_failure_error.error_code = 'ITEM_PARSE_FAILED'
            session.add(item_failure_error)
            session.commit()

    def start_requests(self):
        self.logger.info(f'Starting the spider - {self.name}')
        for url in self.start_urls:
            self.logger.info(f"Checking if the url {url} is enabled for scraping ")
            should_scrape = self.check_if_agent_is_to_be_scraped(url)
            if should_scrape:
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                self.logger.warning(f"URL {url}  is not enabled for scraping, exiting")

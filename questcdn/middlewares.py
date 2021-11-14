# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import datetime
from sqlalchemy.orm import sessionmaker
import mysql.connector
from questcdn import Jobs, db_connect


class QuestcdnSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QuestcdnDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SaveJobInDatabase(object):

    def __init__(self):
        self.create_connection()
        # self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'mpassword',
            database = 'crawling'
        )
        self.curr = self.conn.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_closed(self, spider, reason):
        db_arg = getattr(spider,'addtodatabase','true')
        stats = spider.crawler.stats.get_stats()

        job = {}
        job['job_id'] = self.get_jobid()
        job['start_timestamp'] = stats.get('start_time').strftime('%Y-%m-%d %H:%M:%S')
        job['end_timestamp'] = stats.get('finish_time').strftime('%Y-%m-%d %H:%M:%S')
        job['spider_name'] = spider.name
        job['items_scraped'] = stats.get('item_scraped_count')
        job['items_dropped'] = stats.get('item_dropped_count')
        job['finish_reason'] = stats.get('finish_reason')

        """
        Save jobs in the database.
        This method is called whenever the spider is finished (closed)
        """
        session = self.Session()
        job_add = Jobs(**job)
        session.add(job_add)
        session.commit()

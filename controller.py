"""
Module to hanlde different scripts that the crawler can execute
"""

from common.utils.logging import DEFAULT_LOGGER, LogTypes
from common.mongo.controller import MongoController
from common.celery import queues

from crawler import NewsCrawler
from tasks import app

class Controller():
    """
    Hanldes the different scripts and order of execution
    """
    def __init__(self):
        """
        Initialise the crawler
        """
        self.crawler = NewsCrawler()
        self.mongo_controller = MongoController()

    def __save_news_result(self, news_result):
        """
        Save a news article to the MongoDb

        :param dict news_result: The result received packaged up
        """
        # Remove the trailing Z from timestamp
        news_result['timestamp'] = news_result['timestamp'][:-1]

        crawl = self.mongo_controller.add_crawl_news(
            news_result['keyword_id'],
            news_result['author'],
            news_result['title'],
            news_result['text'],
            news_result['timestamp'],
            return_object=True,
            cast=True
        )

        DEFAULT_LOGGER.log(f'Stored crawl result {crawl.to_json()}', log_type=LogTypes.INFO.value)

        app.send_task('process-crawl', kwargs={ 'crawl_dict': crawl.to_json() }, queue=queues['processor'])

        return crawl

    def __save_news_results(self, news_results):
        """
        Save all news articles

        :param list<dict> news_results: The to be saved news results
        """
        crawls = [self.__save_news_result(result) for result in news_results]
        return crawls

    def run_single_keyword(self, keyword_string, language):
        """
        Crawl a single keyword

        :param str keyword_string: Target keyword string
        :param str language: Target language
        """
        keyword = self.mongo_controller.get_keyword(keyword_string, language, cast=True)
        news_results = self.crawler.search(keyword)
        return self.__save_news_results(news_results)

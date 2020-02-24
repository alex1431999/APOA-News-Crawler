import requests
import os
import sys
import math

class NewsCrawler():
    """
    Interface to the google news API
    Resources: https://newsapi.org/docs/get-started

    The developer plan only allows for truncated results which makes these results
    quite useless for us for now. While we are only running on the dev plan we will just be analyzing
    the titels and not the content.
    """
    def __init__(self):
        """
        Set up credentials and urls
        """
        self.api_key = os.environ["NEWS_API_KEY"]

        # URLS
        self.url_search_headlines = 'https://newsapi.org/v2/top-headlines?'
        self.url_search_keyword = 'https://newsapi.org/v2/everything?'

    def __article_to_news_dict(self, keyword, article):
        """
        Convert an article into a NewsResult object

        :param Keyword keyword: The target keyword used for the request
        :param Object article: The article object holding all information about the article
        """
        title = article['title']
        author = article['author']
        text = article['description']
        timestamp = article['publishedAt']

        news_dict = { 
            'keyword_id': keyword._id,
            'title': title,
            'author': author,
            'text': text,
            'timestamp': timestamp
        }
        return news_dict

    def __send_request(self, keyword_string, language, page_results_amount, page_count_current):
        """
        Send a news request to the API

        :param str keyword: The target keyword used for the request
        :param str language: The target language
        :param int page_results_amount: The amount of results for each page
        :param int page_count_current: The current page we are on
        """
        url = (
            self.url_search_keyword +
            'q="{}"&'.format(keyword_string) +
            'sortyBy=poularity&' +
            'pageSize={}&'.format(page_results_amount) +
            'page={}&'.format(page_count_current) +
            'language={}&'.format(language) +
            'apiKey={}'.format(self.api_key)
        )
        response = requests.get(url).json()
        return response


    def search(self, keyword, limit=sys.maxsize):
        """
        Send a search request for a specific target keyword

        :param Keyword keyword: The target keyword used for the request
        :param int limit: The amount of articles that should be returned 
        """
        # Determine the amount of requests that need to be sent
        page_results_amount = min(100, limit) # 100 is the maximum amount of results per page
        page_amount = math.ceil(limit / page_results_amount) # Amount of pages
        page_count_current = 1 # The current page

        news = self.__send_request(keyword.keyword_string, keyword.language, page_results_amount, page_count_current) # Send an initial request
        news['articles'] = news['articles'][:limit] # Limit the amount of articles
        available_results = news['totalResults']
        page_count_current += 1 # Increase page count to move on to the next one

        while (page_count_current <= page_amount and available_results < len(news['articles'])):
            response = self.__send_request(keyword.keyword_string, keyword.language, page_results_amount, page_count_current)

            if (response['status'] == 'ok'): # Valid response received
                news['articles'] += response['articles'] # Concat all articles
                news['articles'] = news['articles'][:limit] # Make sure you don't exceed the limit
                page_count_current += 1
            else: # The dev version only allows for 100 results
                break

        news = [self.__article_to_news_dict(keyword, article) for article in news['articles']] # Cast articles to news_result objects
        return news

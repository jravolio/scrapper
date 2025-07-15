from scrapy.crawler import CrawlerProcess
import logging
import json
import time
from spiders.ge import GloboSpider


def load_articles():
    pass


def save_articles(articles):
    pass


def detect_new_articles(old, new):
    old_urls = {a["url"] for a in old}
    return [a for a in new if a["url"] not in old_urls]


def post_to_twitter(article):
    print(f"Would post to Twitter: {article['headline']} - {article['url']}")


def run_spider():
    items = []
    
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {__name__ + ".CollectorPipeline": 1},
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(GloboSpider)
    process.start()
    return items


if __name__ == "__main__":
    while True:
        logging.info("Starting scrape...")
        old_articles = load_articles()
        new_articles = run_spider()
        save_articles(new_articles)

        new_posts = detect_new_articles(old_articles, new_articles)
        for article in new_posts:
            post_to_twitter(article)  # Stub

        logging.info(f"Sleeping for 10 minutes...")
        time.sleep(600)

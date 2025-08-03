from scrapy.utils.reactor import install_reactor
install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

import logging
import time

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from spiders.ge import GloboSpider
from utils.twitter import Twitter
from core.settings import settings
from utils.chatgpt import ChatGPT
from core.db import PostActions

DELAY_TIME = 95 * 60  # 95 minutes in seconds


class CustomGloboSpider(GloboSpider):
    scraped_items = []  # Class variable to store items across instances
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clear previous items when creating new instance
        CustomGloboSpider.scraped_items = []

    def parse_article(self, response):
        for article in super().parse_article(response):
            CustomGloboSpider.scraped_items.append(article)
            yield article


@defer.inlineCallbacks
def crawl_and_process():
    """Run the spider and process articles in a loop"""
    db = PostActions(settings.DB_URL)
    db.create_tables()

    twitter = Twitter(
        bearer_token=settings.BEARER_TOKEN_TWITTER,
        consumer_key=settings.CONSUMER_KEY_TWITTER,
        consumer_secret=settings.CONSUMER_SECRET_TWITTER,
        access_token=settings.ACCESS_TOKEN_TWITTER,
        access_token_secret=settings.ACCESS_TOKEN_TWITTER_SECRET,
    )

    chatgpt = ChatGPT(api_key=settings.OPENAI_API_KEY)
    
    runner = CrawlerRunner(settings={"LOG_LEVEL": "INFO"})

    while True:
        logging.info("Starting scrape...")
        
        # Run the spider (pass the class, not an instance)
        yield runner.crawl(CustomGloboSpider)
        
        # Process the scraped articles
        new_articles = CustomGloboSpider.scraped_items
        logging.info(f"Found {len(new_articles)} articles to process")

        for article in new_articles:
            try:
                existing_post = db.get_post_by_url(article['url'])
                if existing_post:
                    logging.info(f"Skipping already processed article: {article['url']}")
                    logging.info(f"Existing post return: {existing_post}")
                    continue # skip if already processed

                catchy_title = chatgpt.generate_catchy_title(
                    news_content=article["first_paragraph"],
                    original_title=article["title"]
                )

                tweet = f"{catchy_title}\n{article['url']}"
                tweet_id = twitter.post_tweet(tweet)
                logging.info(f"Tweeted: {tweet}")

                saved = db.add_post(title=article["title"],
                                    description=article["first_paragraph"],
                                    ai_title=catchy_title,
                                    news_url=article["url"])
                
                logging.info(f"Saved to DB: {saved.id} – {saved.news_url}")

                logging.info(f"Sleeping for {DELAY_TIME} seconds…")
                time.sleep(DELAY_TIME)  # Sleep to avoid hitting rate limits
            except Exception as e:
                db.session.rollback()
                logging.error(
                    f"Failed to process article {article['url']}: {e}")

        logging.info(f"Waiting {DELAY_TIME} seconds before next scrape...")
        d = defer.Deferred()
        reactor.callLater(DELAY_TIME, d.callback, None)


if __name__ == "__main__":
    configure_logging({"LOG_LEVEL": "INFO"})
    
    # Start the crawling and processing loop
    d = crawl_and_process()
    d.addErrback(lambda failure: logging.error(f"Crawling failed: {failure}"))
    
    # Run the reactor
    reactor.run()

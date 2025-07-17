from scrapy.crawler import CrawlerProcess
import logging
import time
from spiders.ge import GloboSpider
from utils.twitter import Twitter
from core.settings import settings
from utils.chatgpt import ChatGPT
from core.db import PostActions


def detect_new_articles(old, new):
    old_urls = {a["url"] for a in old}
    return [a for a in new if a["url"] not in old_urls]


def run_spider():
    items = []

    class CustomGloboSpider(GloboSpider):
        def parse(self, response):
            yield from super().parse(response)

        def parse_article(self, response):
            for article in super().parse_article(response):
                items.append(article)
                yield article

    process = CrawlerProcess(settings={"LOG_LEVEL": "INFO"})
    process.crawl(CustomGloboSpider)
    process.start()
    return items


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

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

    seen_articles = []
    new_articles = run_spider()

    while True:
        logging.info("Starting scrape...")

        new_posts = detect_new_articles(seen_articles, new_articles)

        for article in new_articles:
            try:
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
                                    news_url=article["url"],
                                    tweet_id=tweet_id)
                logging.info(f"Saved to DB: {saved.id} – {saved.news_url}")


            except Exception as e:
                logging.error(
                    f"Failed to process article {article['url']}: {e}")

        seen_articles.extend(new_posts)
        logging.info("Sleeping for 10 minutes…")
        time.sleep(600) # run every 10 minutes

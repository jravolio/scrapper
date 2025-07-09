import scrapy
import logging


class GloboSpider(scrapy.Spider):
    name = "globo"
    start_urls = ["https://ge.globo.com/"]

    # Feed export: save everything the spider yields into articles.json
    custom_settings = {
        "FEEDS": {
            "articles.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4
            }
        }
    }

    def parse(self, response):
        articles = response.xpath(
            "//div[contains(@class,'bastian-page')]/div/div")
        logging.info(f"Found {len(articles)} candidate articles")

        for article in articles:
            title = article.xpath(
                ".//p[contains(@elementtiming,'text-ssr')]/text()").get()
            link = article.xpath(".//a/@href").get()

            if not link:
                continue

            yield response.follow(
                link,
                callback=self.parse_article,
                meta={"headline": title},
            )

    def parse_article(self, response):
        first_para = response.xpath(
            "(//p[contains(@class,'content-text__container')])[1]/text()"
        ).get()

        yield {
            "headline": response.meta["headline"],
            "url": response.url,
            "first_paragraph": first_para,
        }

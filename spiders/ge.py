import scrapy
import logging
import json
import os
import time
from scrapy.crawler import CrawlerProcess


class GloboSpider(scrapy.Spider):
    name = "globo"
    start_urls = ["https://ge.globo.com/"]

    def parse(self, response):
        articles = response.xpath("//div[contains(@class,'bastian-page')]/div/div")
        logging.info(f"Found {len(articles)} candidate articles")

        for article in articles:
            title = article.xpath(".//p[contains(@elementtiming,'text-ssr')]/text()").get()
            link = article.xpath(".//a/@href").get()

            if not link:
                continue

            yield response.follow(
                link,
                callback=self.parse_article,
                meta={"headline": title, "url": link},
            )

    def parse_article(self, response):
        first_paragraph = response.xpath(
            "(//p[contains(@class,'content-text__container')])[1]/text()"
        ).get()

        yield {
            "title": response.meta["headline"],
            "url": response.meta["url"],
            "first_paragraph": first_paragraph,
        }

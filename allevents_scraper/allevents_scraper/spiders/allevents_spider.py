import scrapy
from scrapy_playwright.page import PageMethod


class AllEventsSpider(scrapy.Spider):
    name = "allevents"
    allowed_domains = ["allevents.in"]
    start_urls = ["https://allevents.in/new-york"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
"playwright_page_methods": [
    PageMethod("wait_for_timeout", 3000),
],

                },
            )

    async def parse(self, response):
        events = response.css("div.event-card")

        for event in events:
            yield {
                "title": event.css("h3::text").get(),
                "date": event.css("p.event-date::text").get(),
                "location": event.css("p.event-location::text").get(),
                "link": event.css("a.event-card-link::attr(href)").get(),
            }

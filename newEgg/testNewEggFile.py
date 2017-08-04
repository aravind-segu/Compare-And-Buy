from scrapy import Spider
from scrapy.http import Request
from scrapy.selector import Selector


class newegggpu(Spider):
    name = "newegggpu"
    allowed_domains = ["newegg.com"]
    rank = 1

    def start_requests(self):
        start_urls = [
            "https://www.newegg.ca/Laptops-Notebooks/SubCategory/ID-32/Page-%s?Tid=6741&PageSize=36&order=BESTMATCH"
            % page for page in xrange(1, 67)
        ]
        for url in start_urls:
            yield Request(url = url, callback = self.parse)

    def parse(self, response):
       print response
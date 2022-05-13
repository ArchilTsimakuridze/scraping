import re
import scrapy
from bs4 import BeautifulSoup as bs

from second_project.items import SecondProjectItem
from second_project.settings import SEEDS

WEB_LINKS = "//h2[contains(@class, 'post-title')]//a/@href"
TITLE = "//div[contains(@class, 'container wide')]//h1[contains(@class, 'post-title')]//text()"
CONTENT = "//div[contains(@class, 'post-entry text-justify')]"
NEXT_PAGE_LINK = "//div[contains(@class, 'nav-links')]//a[contains(@class, 'next page-numbers')]/@href"

DOCUMENT_ID_RGX = r"^https?://(?:www\.)?.*?\.org/(.+)"
DOCUMENT_ID_PREFIX = "naa"


class ArisePlus(scrapy.Spider):
    name = 'asean'
    start_urls = SEEDS

    def parse(self, response, **kwargs):
        for link in response.xpath(WEB_LINKS).getall():
            yield scrapy.Request(url=link,
                                 callback=self.parse_html,
                                 meta={'seed_url': response.url})

        next_page = response.xpath(
            "//div[contains(@class, 'nav-links')]//a[contains(@class, 'next "
            "page-numbers')]/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_html(self, response):

        items = SecondProjectItem()

        items['seed_url'] = response.meta.get('seed_url')
        items['url'] = response.url
        items['document_id'] = generate_document_id(response.url)
        items['title'] = prettify_text(" ".join(response.xpath(TITLE).getall()))
        items['fulltext'] = generate_fulltext(response.xpath(CONTENT).getall())
        items['fulltext_content_type'] = 'fulltext/html;utf-8'
        yield items


def prettify_text(text):
    return re.sub(r"\s+", " ", text).strip().replace("\r", "").replace("\n", "").replace("\t", "").strip()


def generate_fulltext(fulltext):
    fulltext = ' '.join(fulltext)
    fulltext = bs(fulltext).prettify().replace("\r", "").replace("\n", "")
    return fulltext


def generate_document_id(url):
    document_id = re.findall(DOCUMENT_ID_RGX, url)[0].strip("/").replace("/", "-").upper()
    document_id = (
        ":".join([DOCUMENT_ID_PREFIX, document_id])
            .upper()
            .rstrip(".PDF")
            .replace("%20", "-")
            .rstrip(".HTM")
            .rstrip(".DOCX")
            .rstrip(".CEB")
    )
    return document_id







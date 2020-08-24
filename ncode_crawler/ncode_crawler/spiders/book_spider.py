# virtualenv python=3.8 scrapy=2.3.0
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class BookSpider(scrapy.Spider):
    name = "book"

    def __init__(self, book=None, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://ncode.syosetu.com/%s/1/" % book]
        self.book = book

    def parse(self, response):
        chp_title = response.css(".novel_subtitle::text").get()
        soup = BeautifulSoup(response.text, 'html.parser')
        main_text = soup.find('div', {'id':'novel_honbun'}).get_text()

        cururl = urlparse(response.url).path.split('/')
        file_name = self.book + '/' + cururl[1] + '_' + cururl[2] + '.txt'

        with open(file_name, 'wt', encoding='utf8') as file:
            file.write(chp_title+'\n')
            file.write(main_text)
            file.close()

        """
        print("\nText:")
        print(main_text)
        print()
        """

        next_page = response.xpath("//a[contains(., '次へ')]/@href").get()
        #print("next page:")
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

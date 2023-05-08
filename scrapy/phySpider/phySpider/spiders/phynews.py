import scrapy


class PhynewsSpider(scrapy.Spider):
    name = "phynews"
    allowed_domains = ["phys.org"]
    start_urls = ["http://phys.org/physics-news/"]

    def parse(self, response):
        links_to_articles = response.xpath('/html/body/main/div/div[1]/div/div[1]/div[4]/div/div/article/div[1]/div/h3/a/@href')
        for link in links_to_articles:
            yield response.follow(link.get(), callback=self.parse_articles)

    def parse_articles(self, response):

        title = response.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[4]/article/h1/text()').get()
        brief = response.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[4]/article/div[2]/p[1]/text()[1]').get()
        body = response.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[4]/article/div[2]/p/text()').getall()
        pdf = response.xpath('/html/body/main/div[1]/div[3]/div[2]/section/div/div[2]/ul/li[2]/a/@href')
        yield {
            'title' : title,
            'brief' : brief,
            'body'  : body,
            'pdf'   : pdf
        }

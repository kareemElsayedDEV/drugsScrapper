import scrapy


class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = [
        'https://dalilaldwaa.com/medicine-list/'
    ]

    def parse(self, response):
        for post in response.css('div.cm-item'):
            details = post.css('.cm-details::attr(href)').get()
            yield from response.follow_all(details, self.parseDrugItem)
            
        next_page = response.css('a.page-link::attr(href)')[-1].get()
        if next_page is not None:
            yield from response.follow_all(next_page, callback=self.parse)
           
    def parseDrugItem(self, response):
        name_retail = response.css('div.even::text')[1].get()
        if name_retail is None:
            name_retail = '';
        yield {
            'img': response.css('img.img-fluid::attr(src)').get(),
            'name': response.css('div.mid-snipp h1::text').get(),
            'name_retail': name_retail,
            'name_scientific': response.css('div.odd::text')[3].get(),
            'price': response.css('p.m-price::text').get(),
            'desc_ar': response.css('div#arabic-desc::text').getall(),
            'desc_en': response.css('div#english-desc::text').getall()
        }
        producers = ""
        for producer in response.css('div.even a::text'):
            producers=producers+ producer
            
        yield {
            'manufacturers': producers
        }
                

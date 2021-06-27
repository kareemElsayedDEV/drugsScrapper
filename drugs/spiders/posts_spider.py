import scrapy


class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = [
        'https://dalilaldwaa.com/medicine-list/'
    ]

    def parse(self, response):
        for post in response.css('div.cm-item'):
            details = post.css('.cm-details::attr(href)').get()
            details = response.urljoin(details)
            yield scrapy.Request(details, self.parseDrugItem)
            
        next_page = response.css('a.page-link::attr(href)')[-1].get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
           
    def parseDrugItem(self, response):
        name_retail_container = response.css('div.even::text')
        name_retail = ""
        if name_retail_container:
            name_retail = name_retail_container[1].get()
            
        name_scientific_container = response.css('div.odd::text')
        name_scientific = ""
        if name_scientific_container:
            name_scientific = name_scientific_container[3].get()

        producers = ""
        for producer in response.css('div.even a::text'):
            producers=producers+ producer.get()
            
            
        yield {
            'img': response.css('img.img-fluid::attr(src)').get(),
            'name': response.css('div.mid-snipp h1::text').get(),
            'name_retail': name_retail,
            'name_scientific': name_scientific,
            'price': response.css('p.m-price::text').get(),
            'desc_ar': response.css('div#arabic-desc::text').getall(),
            'desc_en': response.css('div#english-desc::text').getall(),
            'manufacturers': producers
        }
                

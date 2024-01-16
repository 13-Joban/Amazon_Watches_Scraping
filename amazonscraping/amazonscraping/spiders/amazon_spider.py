import scrapy
from ..items import AmazonscrapingItem

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.in"]
    page_number = 2
    start_urls = ["https://www.amazon.in/s?k=watch+for+men&i=watches&rh=n%3A2563504031%2Cp_72%3A1318476031%2Cp_36%3A3439818031%2Cp_n_feature_fourteen_browse-bin%3A11142592031&s=price-asc-rank&dc&ds=v1%3A0Oavb0YJAzzvorU7LF3RfeOaVmdWS3KPt71nw8Va8aE&crid=25PG7RN3QLXY7&qid=1705343431&rnid=11142591031&sprefix=watch+for+men%2Caps%2C215&ref=sr_nr_p_n_feature_fourteen_browse-bin_1"]

    def parse(self, response):
        items = AmazonscrapingItem()
        # print(items)
        total_products = response.xpath("//div[@class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']")

        for product in total_products:

            product_brand = product.xpath(".//span[@class='a-size-base-plus a-color-base']/text()").extract()[0]
            product_desc = product.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").extract()[0]
            product_price_list = product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").extract()
            product_price = product_price_list[0] if product_price_list else ''

            # product_price = product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").extract()[0]
            product_url = product.xpath(".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href").extract()[0]

            items['product_brand'] = product_brand
            items['product_price'] = product_price
            items['product_desc'] = product_desc
            items['product_url'] = 'https://www.amazon.in' + product_url

            yield items

        next_page = 'https://www.amazon.in/s?k=watch+for+men&i=watches&rh=n%3A2563504031%2Cp_72%3A1318476031%2Cp_36%3A3439818031%2Cp_n_feature_fourteen_browse-bin%3A11142592031&s=price-asc-rank&dc&page=' + str(AmazonSpiderSpider.page_number) + '&crid=25PG7RN3QLXY7&qid=1705343446&rnid=11142591031&sprefix=watch+for+men%2Caps%2C215&ref=sr_pg_2'

        print(next_page)

        if AmazonSpiderSpider.page_number <= 19:
            AmazonSpiderSpider.page_number += 1
            yield scrapy.Request(url=next_page, callback=self.parse)

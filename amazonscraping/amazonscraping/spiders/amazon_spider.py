import scrapy
from ..items import AmazonscrapingItem


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.in"]
    page_number = 2
    start_urls = [
        "https://www.amazon.in/s?k=watch+for+men&i=watches&rh=n%3A2563504031%2Cp_72%3A1318476031%2Cp_36%3A3439818031%2Cp_n_feature_fourteen_browse-bin%3A11142592031&s=price-asc-rank&dc&ds=v1%3A0Oavb0YJAzzvorU7LF3RfeOaVmdWS3KPt71nw8Va8aE&crid=25PG7RN3QLXY7&qid=1705343431&rnid=11142591031&sprefix=watch+for+men%2Caps%2C215&ref=sr_nr_p_n_feature_fourteen_browse-bin_1"]
    i = 1

    def parse(self, response):
        if response.meta.get('first_hit', True):
            no_of_pages = int(
                response.xpath("//span[@class='s-pagination-item s-pagination-disabled']/text()").extract()[0])

            # iterate over pages

            # print('no_of_pages', no_of_pages)

            for page in range(2, no_of_pages + 1):
                next_page = f'https://www.amazon.in/s?k=watch+for+men&i=watches&rh=n%3A2563504031%2Cp_72%3A1318476031%2Cp_36%3A3439818031%2Cp_n_feature_fourteen_browse-bin%3A11142592031&s=price-asc-rank&dc&page={page}&crid=25PG7RN3QLXY7&qid=1705343446&rnid=11142591031&sprefix=watch+for+men%2Caps%2C215&ref=sr_pg_{page}'
                yield response.follow(next_page, callback=self.parse, meta={'first_hit': False})

            # for page in no_of_pages:
            #     next_page = 'https://www.amazon.in/s?k=watch+for+men&i=watches&rh=n%3A2563504031%2Cp_72%3A1318476031%2Cp_36%3A3439818031%2Cp_n_feature_fourteen_browse-bin%3A11142592031&s=price-asc-rank&dc&page=' + str(
            #         AmazonSpiderSpider.page_number) + '&crid=25PG7RN3QLXY7&qid=1705343446&rnid=11142591031&sprefix=watch+for+men%2Caps%2C215&ref=sr_pg_' + str(
            #         AmazonSpiderSpider.page_number)
            #
            #     # print(next_page)
            #
            #     if self.page_number <= no_of_pages:
            #         print("AmazonSpiderSpider.page_number", AmazonSpiderSpider.page_number)
            #         AmazonSpiderSpider.page_number += 1
            #         yield response.follow(next_page, callback=self.parse, meta={'first_hit': False})

        items = AmazonscrapingItem()
        # no_of_pages = int(response.xpath("//span[@class='s-pagination-item s-pagination-disabled']/text()").extract()[0])
        # print(no_of_pages)

        # print(items)
        total_products = response.xpath(
            "//div[@class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']")
        # print("total_products",total_products)
        # total_products =

        for product in total_products:
            product_brand_list = product.xpath(".//span[@class='a-size-base-plus a-color-base']/text()").extract()
            product_brand = product_brand_list[0] if product_brand_list else ''
            product_desc_list = product.xpath(
                ".//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").extract()
            product_desc = product_desc_list[0] if product_desc_list else ''
            product_price_list = product.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").extract()
            product_price = product_price_list[0] if product_price_list else ''
            product_url_list = product.xpath(
                ".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href").extract()
            product_url = product_url_list[0] if product_url_list else ''

            items['product_rank'] = int(self.i)
            items['product_brand'] = product_brand
            items['product_url'] = 'https://www.amazon.in' + product_url

            self.i = self.i + 1
            # yield items
            yield response.follow(product_url, callback=self.parse_product, meta={'items': items.copy()})

    def parse_product(self, response):
        items = response.meta['items']

        product_description = response.xpath("//span[@id='productTitle']/text()").extract_first() if response.xpath(
            "//span[@id='productTitle']/text()").extract_first() else ''

        product_price = response.xpath('//*[(@id = "corePriceDisplay_desktop_feature_div")]//*[contains(concat( " ", @class, " " ), concat( " ", "a-price-whole", " " ))]/text()').extract_first()
        product_case_diameter = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()
        product_band_color = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()
        product_band_material_type = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 4) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()
        product_watch_movement_type = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 5) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()
        product_warranty_type = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 6) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()
        product_item_weight = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 7) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()
        product_country_of_origin = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-facts-detail", " " )) and (((count(preceding-sibling::*) + 1) = 8) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "a-col-right", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "a-color-base", " " ))]/text()').extract_first()

        items['product_description'] = product_description
        items['product_price'] = product_price
        items['product_case_diameter'] = product_case_diameter
        items['product_band_color'] = product_band_color
        items['product_band_material_type'] = product_band_material_type
        items['product_watch_movement_type'] = product_watch_movement_type
        items['product_warranty_type'] = product_warranty_type
        # items['product_case_thickness'] = product_case_thickness
        items['product_item_weight'] = product_item_weight
        items['product_country_of_origin'] = product_country_of_origin

        yield items

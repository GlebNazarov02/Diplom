import scrapy

class AutoSpider(scrapy.Spider):
    name = 'auto'
    start_urls = ['https://auto.ru']

    def parse(self, response):
        # Ищем ссылки на список объявлений автомобилей на главной странице
        for link in response.css('.ListingItemTitle-module__link'):
            yield response.follow(link, self.parse_car)
        
        # Переходим на следующую страницу
        next_page = response.css('.ListingPager-module__next-text').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_car(self, response):
        # Извлекаем информацию об автомобиле
        car_name = response.css('h1::text').get()
        car_price = response.css('.OfferPriceCaption-module__price::text').get()
        car_specs = response.css('.OffersSpecifications-module__item:nth-child(2) .OffersSpecifications-module__value::text').get()

        # Можно сохранить полученные данные в файл или БД
        yield {
            'name': car_name,
            'price': car_price,
            'specs': car_specs
        }

    
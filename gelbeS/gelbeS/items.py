# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    firmenname = scrapy.Field()
    gelbe_seiten_link = scrapy.Field()
    branche = scrapy.Field()
    bundesland = scrapy.Field()
    anschrift = scrapy.Field()
    plz = scrapy.Field()
    telefonnummer = scrapy.Field()
    email_adresse = scrapy.Field()
    anmerkung = scrapy.Field()
from gelbeS.items import CompanyItem
from logging import basicConfig
from re import search
from scrapy import Request
import json
import scrapy


class GsSpider(scrapy.Spider):
    name = 'gs'
    allowed_domains = ['gelbeseiten.de']
    start_urls = ['https://gelbeseiten.de/']
    
    # 'https://www.gelbeseiten.de/Suche/Suchbegriff/Region'
    # basic_pattern = f'{start_urls}/Suche/{search_term}/{region}'

    def start_requests(self):
        url = 'https://gelbeseiten.de/'
        search_term = getattr(self, 'search_term', None)
        region = getattr(self, 'region', None)
        if search_term is not None:
            url = f'{url}Suche/{search_term}/'
        elif search_term is None:
            print('###\n###\n####\nDid you forget to add a search term option?\nMaybe check https://docs.scrapy.org/en/latest/intro/tutorial.html#using-spider-arguments')

        if region is not None:
            url += f'{region}'
        else:
            url += 'Bundesweit'

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # company = CompanyItem()

        for article in response.css('article'):
            # example for visible: article = articles.get()
            # example for lazyload: article = articles.getall()[3]


            # if data-lazyloaddata attribute in article element
                # ...
                # comp_str = article.css('::attr(data-lazyloaddata)').get()
                # turn it into a json dict:
                    # comp_dict = json.loads(comp_str)
                # get adresseKompakt dict from it
                    # comp_dict['adresseKompakt']
                # get telefonnummer, plzOrt & strasseHausnummer, detailseitenUrl from it
                    # comp_dict['adresseKompakt']['telefonnummer']
                    # comp_dict['adresseKompakt']['plzOrt']
                    # comp_dict['adresseKompakt']['strasseHausnummer']
                    # comp_dict['detailseitenUrl']
            # elif data-lazyloaddata attribute not in article element
                # get Anschrift that way: f"{article.css('[data-wipe-name=Adresse] *::text').getall()[0].strip()} {article.css('[data-wipe-name=Adresse] *::text').getall()[1]}"
                # finde restliche Daten
                # ...
                # gsbiz site: article.css('a::attr(href)').get()
                # 
            # else
                # add Anmerkung: "Keine Daten gefunden (weder data-lazyloaddata attribute, noch direkt aus article element extrahierbar)"

            # --- APPROACH to extract gsbiz urls for all 50 initial businesses
            if article.css('a::attr(href)').get() is not None:
                href_detail_page_url = article.css('a::attr(href)').get()
                # company['gelbe_seiten_link'] = href_detail_page_url
                
                yield response.follow(href_detail_page_url, callback=self.detailPage)

            elif article.css('::attr(data-lazyloaddata)').get() is not None:
                comp_str = article.css('::attr(data-lazyloaddata)').get()
                comp_dict = json.loads(comp_str)
                lazy_detail_page_url = comp_dict['detailseitenUrl']

                # company['gelbe_seiten_link'] = lazy_detail_page_url


                # yield {
                #     'Firmenname': article.css('h2::text').get(),
                #     'Gelbe Seiten Link': lazy_detail_page_url,
                #     'Branche(n)': None,
                #     'Bundesland': None,
                #     'Anschrift': None,
                #     'PLZ': None,
                #     'Telefonnummer': None,
                #     'E-Mail Adresse': None,
                #     'Anmerkung': None,
                #     }

                # wenn das meta hier nicht klappt, notfalls ein paar zeilen drüber schon einmal yielden - siehe: https://stackoverflow.com/a/55530050
                    # oder vergiss meta einfach, yielde oben, follow dem link und ergänzen die restlichen Daten in der follow-up funktion - wenn möglich
                        # wahrscheinlich wird in dem stackoverflow nur meta genutzt um nochmal die Daten aus der vorherigen Funktion in der folgenden zu nutzen (was in meinem Fall nicht unbedingt benötogt wird)
                yield response.follow(lazy_detail_page_url, callback=self.detailPage)

            else:
                yield {
                    'Anmerkung': 'Keine Daten gefunden (weder data-lazyloaddata attribute, noch direkt aus article element extrahierbar)',
                    }


            # --- APPROACH first time creating necessary data dict
            # yield {
            #     'Firmenname': article.css('h2::text').get(),
            #     'Branche(n)': None,
            #     'Bundesland': None,
            #     'Anschrift': f"{article.css('[data-wipe-name=Adresse] *::text').getall()[0].strip()} {article.css('[data-wipe-name=Adresse] *::text').getall()[1]}",
            #         # street + number (uncleaned): article.css('address p::text').get()
            #         # region + plz: article.css('address p span::text').get()
            #         # list with complete address (uncleaned): article.css('[data-wipe-name=Adresse] *::text').getall()
            #             # street + number (cleaned - only trailing comma): article.css('[data-wipe-name=Adresse] *::text').getall()[0].strip()
            #             # region + plz (cleaned): article.css('[data-wipe-name=Adresse] *::text').getall()[1]
            #     'PLZ': None,
            #     'Telefonnummer': None,
            #     'E-Mail Adresse': None,
            #     'Gelbe Seiten Link': None,
            #     'Anmerkung': None,
            # }


            # --- APPROACH cURL request: https://docs.scrapy.org/en/latest/topics/developer-tools.html#requests-from-curl
            #   probably not possible because of cookies/tokens or so
                # eventually use "Pre-rendering JS": https://docs.scrapy.org/en/latest/topics/dynamic-content.html#topics-javascript-rendering

                # next_button_undisplayed = response.css('#mod-LoadMore--button').css('[style="display: none;"]').get()
                # if not next_button_undisplayed:
                #     next_request = Request.from_curl('CURL WOULD GO HERE')

    def detailPage(self, response):
        company = CompanyItem()
        company['gelbe_seiten_link'] = response.url
        company['firmenname'] = response.css('h1::text').get()
        company['branche'] = response.css('[data-selenium="teilnehmerkopf__branche"]::text').getall()
        company['bundesland'] = response.css('address *::text').getall()[5]
        company['anschrift'] = response.css('address *::text').getall()[1]
        company['plz'] = response.css('address *::text').getall()[3]
        company['telefonnummer'] = response.css('.mod-TeilnehmerKopf__telefonnummer *::text').getall()[1]
        company['email_adresse'] = response.css('.contains-icon-email a::text').get().strip()



        # yield {
        # 'Firmenname': company_name,
        # 'Gelbe Seiten Link': href_detail_page,
        # 'Branche(n)': None,
        # 'Bundesland': None,
        # 'Anschrift': None,
        # 'PLZ': None,
        # 'Telefonnummer': None,
        # 'E-Mail Adresse': None,
        # 'Anmerkung': None,
        # }

        yield company






# Todo: (If an entry already exists don't make a new one)
# you might want to use this to create clean items from sources of multiple pages: https://stackoverflow.com/questions/34209014/scrapy-scrape-item-fields-from-different-pages

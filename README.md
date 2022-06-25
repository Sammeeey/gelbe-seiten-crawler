# gelbe-seiten-crawler
Scrapy Project to crawl https://www.gelbeseiten.de/

## Usage
- use command line and navigate to crawler directory (which includes the `scrapy.cfg` file)
- use `scrapy crawl` command in the following way

`scrapy crawl gs -O 22-05-26_Beton.csv -a search_term=Beton`

*human understandable translation* of command:
- `scrapy crawl` = run crawler
- `gs` = (name of the crawler respective spider (find it in `.gelbeS/spiders/gs.py`)
- `-O ` = [save the output as file](https://docs.scrapy.org/en/latest/intro/tutorial.html#storing-the-scraped-data) in current directory
- `22-05-26_Beton.csv` = name of the file which should be saved (can be amended depending on crawled terms, date etc.)
- `-a` = seemingly initializer to [pass a search term to the spider](https://stackoverflow.com/a/20938801)
- `search_term=Beton` = search_term is a variable which gets passed to the spider (find it in `.gelbeS/spiders/gs.py`)
    - the passed term (here `Beton`) is the one that gets searched by requesting the respective gelbeseiten.de-URL
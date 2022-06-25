# gelbe-seiten-crawler
Scrapy Project to crawl https://www.gelbeseiten.de/
- collects results which are visible to scrapy spider without further manipulation of website (no JS rendering etc.)
  - spider doesn not obey the robots.txt of the target page, because of `ROBOTSTXT_OBEY = False` in [`settings.py`](https://github.com/Sammeeey/gelbe-seiten-crawler/blob/822e999e876df09bf61163045a5bc17affd8b0e5/gelbeS/gelbeS/settings.py)
- avoids duplicates in output file by default

## Installation (on windows 10; tested - should work)
1. clone repo
2. enter repo folder: `cd gelbe-seiten-crawler`
3. create virtual environment: `py -m venv venv`
4. activate virtual environment: `venv\Scripts\activate.bat`
5. update pip: `py -m pip install --upgrade pip`
6. install requirements: `pip install -r requirements.txt`
7. enter folder which contains the `scrapy.cfg` file: `cd gelbeS`
8. run/crawl spider as described below (*Usage*)

## Usage
1. use command line and navigate to crawler directory (which includes the `scrapy.cfg` file)
2. run/crawl spider (`scrapy crawl` command) in the below descibed way
3. find file with scraped data, choosen name and choosen format in `scrapy.cfg` directory

`scrapy crawl gs -O 22-05-26_Beton.csv -a search_term=Beton`

*human understandable translation* of command:
- `scrapy crawl` = run crawler
- `gs` = (name of the crawler respective spider (find it in `.gelbeS/spiders/gs.py`)
- `-O ` = [save the output as file](https://docs.scrapy.org/en/latest/intro/tutorial.html#storing-the-scraped-data) in current directory
- `22-05-26_Beton.csv` = name of the file which should be saved
  - name can be amended depending on crawled terms, date etc.
  - choose your preferred [output file format](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-exports) (here `.csv`)
- `-a` = seemingly initializer to [pass a search term to the spider](https://stackoverflow.com/a/20938801)
- `search_term=Beton` = search_term is a variable which gets passed to the spider (find it in `.gelbeS/spiders/gs.py`)
    - the passed term (here `Beton`) is the one that gets searched by requesting the respective gelbeseiten.de-URL

![example command line crawl](https://github.com/Sammeeey/gelbe-seiten-crawler/blob/9747afae549858f941acaffd799dc96693d3b4cb/web-scraping-process.gif)

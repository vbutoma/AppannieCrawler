# Appannie Crawler

## Setup

Python version: 3.5

```bash
pip3 install -r requirements.txt
```

Fill in your credentials in the user's section. File: Appanie/Appanie/spiders/configs/company_crawler.json
## Running examples

Cd into project's dir

```bash
cd Appanie
```

* ```bash
    scrapy crawl CompanyScraper
    ```
* ```bash
    scrapy crawl CompanyScraper -a company_id=abacaba
    ```
* ```bash
    scrapy crawl CompanyScraper -a company_id=1000200000020105 -a start_date=2017-07-11 -a end_date=2018-08-01
    ```
    
* ```bash
    scrapy crawl CompanyScraper -a company_id=abacaba -a start_date=2017-07-11 -a end_date=2018-08-01
    ```

Also you can customize runner.py and run it :)

```bash
python3 runner.py
```
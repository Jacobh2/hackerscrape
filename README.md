# Hackerscrape

The only scraper you need when you really just want to scrape the hackernews website :sunglasses:

## Run locally

`docker-compose up`

Will start up a docker container on port 8080

## Test covarage
```
Name                         Stmts   Miss  Cover
------------------------------------------------
logger_config.py                11     11     0%
main.py                         43     43     0%
objects/__init__.py              0      0   100%
objects/article.py               2      0   100%
ranker/__init__.py              17      1    94%
repository/__init__.py          41     19    54%
scrape/__init__.py              16      0   100%
service.py                      22      1    95%
tests/test_hackerscrape.py      32      0   100%
tests/test_ranker.py            24      0   100%
tests/test_repository.py        15      0   100%
tests/test_scrape.py            12      0   100%
webserver/__init__.py            0      0   100%
webserver/app.py                46     46     0%
webserver/articles.py           18     18     0%
------------------------------------------------
TOTAL                          299    139    54%
```
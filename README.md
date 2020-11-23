# Amazon Purchase Script 

Example: script to buy the things on Amazon 

forked from yosh1/amazon-automation & druyang/amazon-PS5-automation

Use at your own risk

Requirements: 
--- 

* Python 3 
* Selenium 
* [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads) in same directory 
* dotenv

Recommended to be run on Linux or Max. Would be a good script to run on a raspberry pi or server

Notes of caution: 
--- 

Things to check for on Amazon/potential edge cases: 

 * Amazon 2FA 
 * Default address / payment method - fixed with 1-click buy - to do:  need to verify logged in and authenticated
 * Captchas for hitting Amazon's server a lot

---

## Copy `.env`

```
$ cp .env.sample .env
```

## Run

```
$ python3 main.py
```

Alternatively use Docker: 

```
$ docker-compose build
$ docker-compose up -d
```


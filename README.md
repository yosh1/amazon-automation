# Amazon Purchase Script 

Example: script to buy the PS5 on Amazon 

forked from yosh1/amazon-automation. 

Use at your own risk

Requirements: 
--- 

* Python 3 
* Selenium 
* dotenv

Recommended to be run on Linux or Max. Would be a good script to run on a raspberry pi 

Notes of caution: 
--- 

Things to check for on Amazon/potential edge cases: 

 * Amazon 2FA 
 * Default address / payment method 
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

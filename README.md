# Amazon Automation

Script to make an automatic purchase on Amazon.com

---

## Requirements

- Python3 (but not supported v3.9 higher)
  - Selenium
  - dotenv
- Linux or Mac (Would be a good script to run on a raspberry pi or server)

## How to run

※ Make sure you have 2FA (two factor authentication) turned off on your Amazon account!

### Copy and edit `.env` file

```
$ cp .env.sample .env
```

### Run

```
$ python3 main.py
```

Alternatively use Docker:

```
$ docker-compose build
$ docker-compose up -d
```

## License

Under MIT License.

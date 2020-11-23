#coding: utf-8

import time
import os
from os.path import join, dirname
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LOGIN_MAIL = os.environ.get("MAIL_ADDRESS")
LOGIN_PASSWORD = os.environ.get("PASSWORD")
ITEM_URL = os.environ.get("ITEM_URL")
ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 500    # Maximum USD for the purchase


def l(str):
    print("%s : %s" % (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))


if __name__ == '__main__':

    # Launch selenium
    try:
        b = webdriver.Chrome('./chromedriver')
        b.get(ITEM_URL)
    except:
        l('Failed to open browser.')
        exit()

    while True:
        # Check for inventory
        while True:
            try:
                shop = b.find_element_by_id('merchant-info').text
                print(shop)
                # shop = shop.split('が販売')[0].split('この商品は、')[1]

                if ACCEPT_SHOP not in shop:
                    raise Exception("not Amazon.")

                b.find_element_by_id('add-to-cart-button').click()
                break
            except:
                time.sleep(60)
                b.refresh()

        # Purchase
        b.get('https://www.amazon.co.jp/gp/cart/view.html/ref=nav_cart')
        b.find_element_by_name('proceedToCheckout').click()

        # Login
        try:
            b.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
            b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            b.find_element_by_id('signInSubmit').click()
        except:
            l('LOGIN PASS.')
            pass

        # Verify Price
        p = b.find_element_by_css_selector('td.grand-total-price').text
        if int(p.split(' ')[1].replace(',', '')) > LIMIT_VALUE:
            l('PLICE IS TOO LARGE.')
            continue

        # Place the order
        b.find_element_by_name('placeYourOrder1').click()
        break

    l('ALL DONE.')

# coding: utf-8

import time
import os
from os.path import join, dirname
from datetime import datetime
from selenium import webdriver
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException

# 環境変数のロード
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数の取得
LOGIN_MAIL = os.getenv("MAIL_ADDRESS")
LOGIN_PASSWORD = os.getenv("PASSWORD")
ITEM_URL = os.getenv("ITEM_URL")
ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 33500 # 最低金額

def log_message(message):
    """ ログメッセージを出力する関数 """
    print(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} : {message}")

def check_environment_variables():
    """ 環境変数のチェックを行う関数 """
    if None in (LOGIN_MAIL, LOGIN_PASSWORD, ITEM_URL):
        log_message('環境変数が正しく設定されていません')
        exit()

def initialize_browser():
    """ ブラウザを起動する関数 """
    try:
        browser = webdriver.Chrome('./chromedriver')
        browser.get(ITEM_URL)
        return browser
    except Exception as e:
        log_message(f'Failed to open browser: {e}')
        exit()

def main():
    check_environment_variables()
    browser = initialize_browser()

    while True:
        while True:
            try:
                shop_info = browser.find_element_by_id('merchant-info').text
                shop_name = shop_info.split('が販売')[0].split('この商品は、')[1]

                if ACCEPT_SHOP not in shop_name:
                    raise Exception("not Amazon.")

                browser.find_element_by_id('add-to-cart-button').click()
                break
            except NoSuchElementException:
                time.sleep(60)
                browser.refresh()

        # 購入手続き
        browser.get('https://www.amazon.co.jp/gp/cart/view.html/ref=nav_cart')
        browser.find_element_by_name('proceedToCheckout').click()

        # ログイン
        try:
            browser.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
            browser.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            browser.find_element_by_id('signInSubmit').click()
        except NoSuchElementException:
            log_message('ログインに失敗しました')
            continue

        # 値段の確認
        try:
            price_text = browser.find_element_by_css_selector('td.grand-total-price').text
            price = int(price_text.split(' ')[1].replace(',', ''))
            if price > LIMIT_VALUE:
                log_message('価格が制限を超えています')
                continue
        except NoSuchElementException:
            log_message('価格の取得に失敗しました')
            continue

        # 注文の確定
        browser.find_element_by_name('placeYourOrder1').click()
        break

    log_message('ALL DONE.')

if __name__ == '__main__':
    main()

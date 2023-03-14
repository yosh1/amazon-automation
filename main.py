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
LIMIT_VALUE = 33500    # 最低金額


def l(str):
    print("%s : %s" % (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))


if __name__ == '__main__':

    # 環境変数のチェック
    if LOGIN_MAIL is None or LOGIN_PASSWORD is None or ITEM_URL is None:
        l('環境変数が正しく設定されていません')
        exit()

    # ブラウザの起動
    try:
        b = webdriver.Chrome('./chromedriver')
        b.get(ITEM_URL)
    except:
        l('Failed to open browser.')
        exit()

    while True:
        # 在庫確認
        while True:
            try:
                shop = b.find_element_by_id('merchant-info').text
                shop = shop.split('が販売')[0].split('この商品は、')[1]

                if ACCEPT_SHOP not in shop:
                    raise Exception("not Amazon.")

                b.find_element_by_id('add-to-cart-button').click()
                break
            except:
                time.sleep(60)
                b.refresh()

        # 購入手続き
        b.get('https://www.amazon.co.jp/gp/cart/view.html/ref=nav_cart')
        b.find_element_by_name('proceedToCheckout').click()

        # ログイン
        try:
            b.find_element_by_id('ap_email').send_keys(LOGIN_MAIL)
            b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            b.find_element_by_id('signInSubmit').click()
        except:
            l('ログインに失敗しました')
            pass

        # 値段の確認
        p = b.find_element_by_css_selector('td.grand-total-price').text
        if int(p.split(' ')[1].replace(',', '')) > LIMIT_VALUE:
            l('価格が制限を超えています')
            continue

        # 注文の確定
        b.find_element_by_name('placeYourOrder1').click()
        break

    l('ALL DONE.')

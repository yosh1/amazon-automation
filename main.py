#coding: utf-8

import time
from datetime import datetime
from selenium import webdriver

LOGIN_ID = '[メールアドレス]'
LOGIN_PASSWORD = '[パスワード]'

ITEM_URL = 'https://www.amazon.co.jp/dp/??????????????????'    # 商品URL

ACCEPT_SHOP = 'Amazon'
LIMIT_VALUE = 33500    # 最低金額

def l(str):
    print("%s : %s"%(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),str))

if __name__ == '__main__':

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
                # 販売元確認
                shop = b.find_element_by_id('merchant-info').text
                shop = shop.split('が販売')[0].split('この商品は、')[1]

                if ACCEPT_SHOP not in shop:
                    raise Exception("not Amazon.")

                # カードに入れる
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
            b.find_element_by_id('ap_email').send_keys(LOGIN_ID)
            b.find_element_by_id('ap_password').send_keys(LOGIN_PASSWORD)
            b.find_element_by_id('signInSubmit').click()
        except:
            l('LOGIN PASS.')
            pass

        # 値段の確認
        p = b.find_element_by_css_selector('td.grand-total-price').text
        if int(p.split(' ')[1].replace(',', '')) > LIMIT_VALUE:
            l('PLICE IS TOO LARGE.')
            continue

        # 注文の確定
        b.find_element_by_name('placeYourOrder1').click()
        break

    l('ALL DONE.')
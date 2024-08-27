#coding: utf-8

import time
import os
from os.path import join, dirname
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return {
        "LOGIN_MAIL": os.environ.get("MAIL_ADDRESS"),
        "LOGIN_PASSWORD": os.environ.get("PASSWORD"),
        "ITEM_URL": os.environ.get("ITEM_URL"),
        "ACCEPT_SHOP": "Amazon",
        "LIMIT_VALUE": 33500  # 最低金額
    }

def log_message(message):
    print(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} : {message}")

def validate_env_variables(env_vars):
    if not all(env_vars.values()):
        log_message("環境変数が正しく設定されていません")
        exit()

def initialize_browser():
    try:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service)
        return browser
    except Exception as e:
        log_message(f"Failed to open browser: {e}")
        exit()

def check_stock_and_add_to_cart(browser, item_url, accept_shop):
    while True:
        try:
            browser.get(item_url)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, 'merchant-info'))
            )
            shop_info = browser.find_element(By.ID, 'merchant-info').text
            shop = shop_info.split('が販売')[0].split('この商品は、')[1]

            if accept_shop not in shop:
                raise ValueError("Not the desired shop.")

            browser.find_element(By.ID, 'add-to-cart-button').click()
            break
        except Exception as e:
            log_message(f"Stock checking error: {e}")
            time.sleep(60)
            browser.refresh()

def login(browser, login_mail, login_password):
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'ap_email'))
        )
        browser.find_element(By.ID, 'ap_email').send_keys(login_mail)
        browser.find_element(By.ID, 'ap_password').send_keys(login_password)
        browser.find_element(By.ID, 'signInSubmit').click()
    except Exception as e:
        log_message(f"ログインに失敗しました: {e}")
        raise

def check_price_and_place_order(browser, limit_value):
    try:
        price_text = browser.find_element(By.CSS_SELECTOR, 'td.grand-total-price').text
        price = int(price_text.split(' ')[1].replace(',', ''))
        if price > limit_value:
            log_message("価格が制限を超えています")
            return False
        browser.find_element(By.NAME, 'placeYourOrder1').click()
        return True
    except Exception as e:
        log_message(f"Order placing error: {e}")
        return False

def main():
    env_vars = load_env_variables()
    validate_env_variables(env_vars)

    browser = initialize_browser()

    try:
        check_stock_and_add_to_cart(browser, env_vars["ITEM_URL"], env_vars["ACCEPT_SHOP"])
        
        browser.get('https://www.amazon.co.jp/gp/cart/view.html/ref=nav_cart')
        browser.find_element(By.NAME, 'proceedToCheckout').click()
        
        login(browser, env_vars["LOGIN_MAIL"], env_vars["LOGIN_PASSWORD"])
        
        if check_price_and_place_order(browser, env_vars["LIMIT_VALUE"]):
            log_message("ALL DONE.")
        else:
            log_message("購入手続きに失敗しました。再試行します。")
            main()
    finally:
        browser.quit()

if __name__ == '__main__':
    main()

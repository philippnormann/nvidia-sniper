import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TIMEOUT = 10


def add_to_basket(driver, gpu_url, locale):
    driver.get('https://www.nvidia.com/' + locale + gpu_url)
    try:
        add_to_basket_btn_path = '//div[contains(@class,"singleSlideBanner")]' + \
            '//div[contains(@class, "js-add-button")]'
        add_to_basket_clickable = EC.element_to_be_clickable(
            (By.XPATH, add_to_basket_btn_path))
        WebDriverWait(driver, TIMEOUT).until(add_to_basket_clickable)
        logging.info(f'Found available GPU: {gpu_url}')
        logging.info(f'Adding to basket...')
        driver.find_element(By.XPATH, add_to_basket_btn_path).click()
        return True
    except TimeoutException:
        return False


def to_checkout(driver, locale):
    checkout_reached = False
    logging.info('Going to checkout page...')
    while not checkout_reached:
        try:
            driver.find_element(By.CLASS_NAME, 'cart__checkout-button').click()
            WebDriverWait(driver, TIMEOUT).until(EC.url_contains(
                'store.nvidia.com/store?Action=DisplayPage'))
            checkout_reached = True
        except TimeoutException:
            logging.info(
                "Timed out waiting for checkout page to load, trying again...")
            driver.get(f"https://www.nvidia.com/{locale}/shop")
            WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'nav-cart-link')))
            driver.find_element(By.CLASS_NAME, 'nav-cart-link').click()


def checkout_guest(driver, customer):
    logging.info('Checking out as guest...')
    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, 'btnCheckoutAsGuest')))
    driver.find_element(By.ID, 'btnCheckoutAsGuest').click()

    driver.find_element(By.ID, 'billingName1').send_keys(
        customer['name']['first'])
    driver.find_element(By.ID, 'billingName2').send_keys(
        customer['name']['last'])

    driver.find_element(By.ID, 'billingAddress1').send_keys(
        customer['address']['street'])
    driver.find_element(By.ID, 'billingCity').send_keys(
        customer['address']['city'])
    driver.find_element(By.ID, 'billingPostalCode').send_keys(

        customer['address']['zip'])
    driver.find_element(By.ID, 'billingPhoneNumber').send_keys(
        customer['phone'])
    driver.find_element(By.ID, 'email').send_keys(
        customer['email'])
    driver.find_element(By.ID, 'verEmail').send_keys(
        customer['email'])

    driver.find_element(By.ID, 'ccNum').send_keys(
        customer['credit']['card'])
    driver.find_element(By.ID, 'ccNum').send_keys(
        customer['credit']['card'])

    month_select = Select(driver.find_element_by_id('expirationDateMonth'))
    month_select.select_by_value(customer['credit']['expiration']['month'])

    year_select = Select(driver.find_element_by_id('expirationDateYear'))
    year_select.select_by_value(customer['credit']['expiration']['year'])

    driver.find_element(By.ID, 'cardSecurityCode').send_keys(
        customer['credit']['code'])

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    driver.find_element(
        By.CSS_SELECTOR, '#dr_siteButtons > .dr_button').click()


def checkout_paypal(driver):
    logging.info('Checking out using PayPal Express...')
    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, 'lnkPayPalExpressCheckout')))
        driver.find_element(By.ID, 'lnkPayPalExpressCheckout').click()
    except TimeoutException:
        logging.info("Timed out waiting for PayPal button to load")

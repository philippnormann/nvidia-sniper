import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def add_to_basket(driver, timeout, locale, gpu_url, anticache):
    driver.get('https://www.nvidia.com/' + locale + gpu_url + anticache)
    try:
        add_to_basket_selector = '.singleSlideBanner .js-add-button'
        add_to_basket_clickable = EC.element_to_be_clickable(
            (By.CSS_SELECTOR, add_to_basket_selector))
        WebDriverWait(driver, timeout).until(add_to_basket_clickable)
        logging.info(f'Found available GPU: {gpu_url}')
        logging.info(f'Trying to add to basket...')
        try:
            driver.find_element(By.CSS_SELECTOR, add_to_basket_selector).click()
        except ElementClickInterceptedException:
            logging.info(f'Couldn\'t click the add to basket button, checking if theres a cookie prompt obscuring...')
            # Maybe should be global? 
            cookie_prompt_accept_id = 'cookiePolicy-btn-close'
            try:
                driver.find_element(By.ID, cookie_prompt_accept_id).click()
            except NoSuchElementException:
                logging.error(f'Couldn\'t find a prompt to close.')
                return False
            logging.info(f'Trying to add to basket again...')
            driver.find_element(By.CSS_SELECTOR, add_to_basket_selector).click()
        return True
    except TimeoutException:
        return False


def to_checkout(driver, timeout, locale):
    checkout_reached = False
    logging.info('Going to checkout page...')
    while not checkout_reached:
        try:
            driver.find_element(By.CLASS_NAME, 'cart__checkout-button').click()
            WebDriverWait(driver, timeout).until(
                EC.url_contains('store.nvidia.com'))
            checkout_reached = True
        except TimeoutException:
            logging.info(
                'Timed out waiting for checkout page to load, trying again...')
            try:
                driver.find_element(By.CLASS_NAME, 'cart__checkout-button')
            except NoSuchElementException:
                driver.get(f'https://www.nvidia.com/{locale}/shop')
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'nav-cart-link')))
                driver.find_element(By.CLASS_NAME, 'nav-cart-link').click()


def fill_out_form(driver, customer):
    driver.find_element(By.ID, 'billingName1').send_keys(
        customer['billing']['first-name'])
    driver.find_element(By.ID, 'billingName2').send_keys(
        customer['billing']['last-name'])

    driver.find_element(By.ID, 'billingAddress1').send_keys(
        customer['billing']['street'])
    driver.find_element(By.ID, 'billingCity').send_keys(
        customer['billing']['city'])
    driver.find_element(By.ID, 'billingPostalCode').send_keys(
        customer['billing']['zip'])

    driver.find_element(By.ID, 'billingPhoneNumber').send_keys(
        customer['billing']['phone'])
    driver.find_element(By.ID, 'email').send_keys(
        customer['billing']['email'])
    driver.find_element(By.ID, 'verEmail').send_keys(
        customer['billing']['email'])

    driver.find_element(By.ID, 'shippingDifferentThanBilling').click()

    driver.find_element(By.ID, 'shippingName1').send_keys(
        customer['shipping']['first-name'])
    driver.find_element(By.ID, 'shippingName2').send_keys(
        customer['shipping']['last-name'])

    driver.find_element(By.ID, 'shippingAddress1').send_keys(
        customer['shipping']['street'])
    driver.find_element(By.ID, 'shippingCity').send_keys(
        customer['shipping']['city'])
    driver.find_element(By.ID, 'shippingPostalCode').send_keys(
        customer['shipping']['zip'])

    driver.find_element(By.ID, 'shippingPhoneNumber').send_keys(
        customer['shipping']['phone'])

    driver.find_element(By.ID, 'ccNum').send_keys(
        customer['credit']['card'])

    month_select = Select(driver.find_element_by_id('expirationDateMonth'))
    month_select.select_by_value(customer['credit']['expiration']['month'])

    year_select = Select(driver.find_element_by_id('expirationDateYear'))
    year_select.select_by_value(customer['credit']['expiration']['year'])

    driver.find_element(By.ID, 'cardSecurityCode').send_keys(
        customer['credit']['code'])


def checkout_guest(driver, timeout, customer, auto_submit=False):
    proceeded_to_form = False
    logging.info('Checking out as guest...')
    while not proceeded_to_form:
        try:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.ID, 'btnCheckoutAsGuest')))
            driver.find_element(By.ID, 'btnCheckoutAsGuest').click()
            proceeded_to_form = True
        except TimeoutException:
            logging.info(
                'Timed out waiting for checkout button to load, trying again...')
            driver.get('https://store.nvidia.com/store/nvidia/cart')

    fill_out_form(driver, customer)

    submit_btn_selector = '#dr_siteButtons > .dr_button'
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    driver.find_element(
        By.CSS_SELECTOR, submit_btn_selector).click()
    if auto_submit:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_btn_selector)))
        driver.find_element(By.CSS_SELECTOR, submit_btn_selector).click()


def checkout_paypal(driver, timeout):
    proceeded_to_paypal = False
    logging.info('Checking out using PayPal Express...')
    while not proceeded_to_paypal:
        try:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.ID, 'lnkPayPalExpressCheckout')))
            driver.find_element(By.ID, 'lnkPayPalExpressCheckout').click()
            proceeded_to_paypal = True
        except TimeoutException:
            logging.info(
                'Timed out waiting for PayPal button to load, trying again...')
            driver.get('https://store.nvidia.com/store/nvidia/cart')

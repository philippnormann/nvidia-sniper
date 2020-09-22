import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def scroll_to(driver, element):
    driver.execute_script(
        'arguments[0].scrollIntoView({block: "center"})', element)


def add_to_basket(driver, timeout, locale, gpu_url, anticache):
    logging.info(f'Checking {locale} availability for {gpu_url}...')
    driver.get('https://www.nvidia.com/' + locale + gpu_url + anticache)
    try:
        add_to_basket_selector = '.singleSlideBanner .js-add-button'
        add_to_basket_clickable = EC.element_to_be_clickable(
            (By.CSS_SELECTOR, add_to_basket_selector))
        WebDriverWait(driver, timeout).until(add_to_basket_clickable)
        logging.info(f'Found available GPU: {gpu_url}')
        logging.info(f'Trying to add to basket...')
        add_to_basket_btn = driver.find_element(
            By.CSS_SELECTOR, add_to_basket_selector)
        scroll_to(driver, add_to_basket_btn)
        add_to_basket_btn.click()
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
        customer['billing']['address-line-1'])
    driver.find_element(By.ID, 'billingAddress2').send_keys(
        customer['billing']['address-line-2'])

    try:
        driver.find_element(By.ID, 'billingState')
        state_select = Select(driver.find_element_by_id('billingState'))
        state_select.select_by_value(customer['billing']['state'])
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.ID, 'billingCountry')
        country_select = Select(driver.find_element_by_id('billingCountry'))
        country_select.select_by_value(customer['billing']['country'])
    except NoSuchElementException:
        pass

    driver.find_element(By.ID, 'billingCity').send_keys(
        customer['billing']['city'])
    driver.find_element(By.ID, 'billingPostalCode').send_keys(
        customer['billing']['post-code'])

    driver.find_element(By.ID, 'billingPhoneNumber').send_keys(
        customer['billing']['phone'])
    driver.find_element(By.ID, 'email').send_keys(
        customer['billing']['email'])
    driver.find_element(By.ID, 'verEmail').send_keys(
        customer['billing']['email'])

    if 'shipping' in customer:
        driver.find_element(By.ID, customer['shipping']['speed']).click()

        driver.find_element(By.ID, 'shippingDifferentThanBilling').click()

        driver.find_element(By.ID, 'shippingName1').send_keys(
            customer['shipping']['first-name'])
        driver.find_element(By.ID, 'shippingName2').send_keys(
            customer['shipping']['last-name'])

        driver.find_element(By.ID, 'shippingAddress1').send_keys(
            customer['shipping']['address-line-1'])
        driver.find_element(By.ID, 'shippingAddress2').send_keys(
            customer['shipping']['address-line-2'])

        try:
            driver.find_element(By.ID, 'shippingState')
            state_select = Select(driver.find_element_by_id('shippingState'))
            state_select.select_by_value(customer['shipping']['state'])
        except NoSuchElementException:
            pass

        try:
            driver.find_element(By.ID, 'shippingCountry')
            country_select = Select(
                driver.find_element_by_id('shippingCountry'))
            country_select.select_by_value(customer['shipping']['country'])
        except NoSuchElementException:
            pass

        driver.find_element(By.ID, 'shippingCity').send_keys(
            customer['shipping']['city'])
        driver.find_element(By.ID, 'shippingPostalCode').send_keys(
            customer['shipping']['post-code'])

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


def skip_address_check(driver):
    driver.find_element(By.ID, 'billingAddressOptionRow2').click()
    driver.find_element(By.ID, 'shippingAddressOptionRow2').click()
    driver.find_element(By.ID, 'selectionButton').click()

def checkout_guest(driver, timeout, customer, auto_submit=False):
    proceeded_to_form = False
    logging.info('Checking out as guest...')
    while not proceeded_to_form:
        try:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.ID, 'btnCheckoutAsGuest')))
            guest_checkout_btn = driver.find_element(By.ID, 'btnCheckoutAsGuest')
            scroll_to(driver, guest_checkout_btn)
            guest_checkout_btn.click()
            proceeded_to_form = True
        except TimeoutException:
            logging.info(
                'Timed out waiting for checkout button to load, trying again...')
            driver.get('https://store.nvidia.com/store/nvidia/cart')

    fill_out_form(driver, customer)
    submit_btn_selector = '#dr_siteButtons > .dr_button'
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    driver.find_element(By.CSS_SELECTOR, submit_btn_selector).click()

    try:
        driver.find_element(By.CLASS_NAME, 'dr_error')
        skip_address_check(driver)
    except NoSuchElementException:
        pass

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

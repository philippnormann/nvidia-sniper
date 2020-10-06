import os
import sys
import json
import logging
import queue
import asyncio
try:
    import aiohttp
    import colorama
    
    from pick import pick
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
except Exception:
    logging.error(
        'Could not import all required modules. '\
        'Please run the following command again:\n\n'\
        '\tpipenv install\n')
    exit()

from pathlib import Path
from time import sleep

import sniper.api as api
import sniper.nvidia as nvidia
import sniper.constants as const
import sniper.webdriver as webdriver
import sniper.notifications as notify

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'
config_path = src_path.parent / 'config'


def read_json(filename):
    with open(filename, encoding='utf-8') as json_file:
        return json.load(json_file)


async def checkout_api(driver, user_agent, timeout, locale, dr_locale, api_currency, target_gpu, notifications, notification_queue):
    logging.info(
        f"Checking {locale} availability for {target_gpu['name']} using API...")
    product_loaded = nvidia.get_product_page(
        driver, locale, target_gpu, anticache=True)
    if product_loaded:
        try:
            item = driver.find_element(
                By.CSS_SELECTOR, const.PRODUCT_ITEM_SELECTOR)
            dr_id = item.get_attribute('data-digital-river-id')
        except NoSuchElementException:
            logging.info('Failed to locate Digital River ID on product page')
            return False
        async with aiohttp.ClientSession(headers={'User-Agent': user_agent}, cookie_jar=aiohttp.CookieJar()) as session:
            try:
                inventory = await api.get_inventory_status(session, dr_locale, api_currency, dr_id)
            except Exception:
                logging.info(
                    f'Failed to get inventory status for {dr_id}, the API is most likely down for everyone')
                return False
            logging.info(f'Inventory status for {dr_id}: {inventory}')
            if inventory != 'PRODUCT_INVENTORY_OUT_OF_STOCK':
                logging.info(f"Found available GPU: {target_gpu['name']}")
                if notifications['availability']['enabled']:
                    driver.save_screenshot(const.SCREENSHOT_FILE)
                    notification_queue.put('availability')
                try:
                    logging.info('Fetching API token...')
                    store_token = await api.fetch_token(session, dr_locale)
                    logging.info('API Token: ' + store_token)
                    logging.info('Overiding store cookies for driver...')
                    driver.get(const.STORE_URL)
                    for key, morsel in session.cookie_jar.filter_cookies(const.STORE_URL).items():
                        driver.add_cookie(
                            {'name': key, 'value': morsel.value, 'domain': const.STORE_HOST})
                except Exception:
                    logging.exception(f'Failed to fetch API token')
                    return False
                try:
                    logging.info('Calling add to cart API...')
                    add_to_cart_response = await api.add_to_cart(session, store_token, dr_locale, dr_id)
                    response = add_to_cart_response['message']
                    logging.info(f'Add to basket response: {response}')
                except Exception:
                    logging.exception(f'Failed to add item to basket')
                    return False
                try:
                    logging.info('Going to checkout page...')
                    driver.get(const.CHECKOUT_URL)
                    if notifications['add-to-basket']['enabled']:
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        notification_queue.put('add-to-basket')
                    return True
                except (TimeoutException, WebDriverException):
                    logging.error(
                        'Lost basket and failed to checkout, trying again...')
                    return False
            else:
                return False
    else:
        return False


def checkout_selenium(driver, timeout, locale, target_gpu, notifications, notification_queue):
    logging.info(
        f"Checking {locale} availability for {target_gpu['name']} using selenium...")
    product_loaded = nvidia.get_product_page(driver, locale, target_gpu)
    if product_loaded:
        gpu_available = nvidia.check_availability(driver, timeout)
        if gpu_available:
            logging.info(f"Found available GPU: {target_gpu['name']}")
            if notifications['availability']['enabled']:
                driver.save_screenshot(const.SCREENSHOT_FILE)
                notification_queue.put('availability')
            added_to_basket = False
            while not added_to_basket:
                logging.info(f'Trying to add to basket...')
                added_to_basket = nvidia.add_to_basket(driver, timeout)
                if not added_to_basket:
                    logging.info(
                        f'Add to basket click failed, trying again!')
            logging.info(f'Add to basket click suceeded!')
            if notifications['add-to-basket']['enabled']:
                driver.save_screenshot(const.SCREENSHOT_FILE)
                notification_queue.put('add-to-basket')
            logging.info('Going to checkout page...')
            checkout_reached = nvidia.to_checkout(
                driver, timeout, locale, notification_queue)
            if checkout_reached:
                return True
            else:
                logging.error(
                    'Lost basket and failed to checkout, trying again...')
                return False
        else:
            logging.info('GPU currently not available')
        return False
    else:
        return False


def read_config():
    try:
        notification_config = read_json(config_path / 'notifications.json')
    except FileNotFoundError:
        logging.error(
            'Missing notification configuration file, copy the template to config/notifications.json and customize as described in the README to continue.')
        sys.exit()
    except json.decoder.JSONDecodeError:
        logging.error(
            'Error while parsing the notification configuration file, check config/notifications.json for syntax errors and fix them to continue.')
        sys.exit()

    try:
        customer = read_json(config_path / 'customer.json')
    except FileNotFoundError:
        logging.error(
            'Missing customer configuration file, copy the template to config/customers.json and customize as described in the README to continue.')
        sys.exit()
    except json.decoder.JSONDecodeError:
        logging.error(
            'Error while parsing the customer configuration file, check config/customer.json for syntax errors and fix them to continue.')
        sys.exit()
    return notification_config, customer


async def main():
    colorama.init()
    print(const.HEADER)

    notification_config, customer = read_config()

    driver = webdriver.create()
    user_agent = driver.execute_script('return navigator.userAgent;')

    log_format = '%(asctime)s nvidia-sniper: %(message)s'
    fh = logging.FileHandler('sniper.log', encoding='utf-8')
    sh = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO,
                        format=log_format, handlers=[fh, sh])

    logging.info('|---------------------------|')
    logging.info('| Starting Nvidia Sniper 🎯 |')
    logging.info('|---------------------------|')

    gpu_data = read_json(data_path / 'gpus.json')
    target_gpu, _ = pick(list(gpu_data.keys()),
                         'Which GPU are you targeting?',
                         indicator='=>')

    payment_method, _ = pick(['credit-card', 'paypal'],
                             'Which payment method do you want to use?',
                             indicator='=>')

    auto_submit, _ = pick(['Yes', 'No'],
                          'Do you want to automatically submit the order? (only works with credit card)',
                          indicator='=>',  default_index=1)
    auto_submit = auto_submit == 'Yes'

    timeout, _ = pick([' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds', '64 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=1)
    timeout = int(timeout.replace('seconds', '').strip())

    target_gpu = gpu_data[target_gpu]

    notifications = notification_config['notifications']
    notification_queue = queue.Queue()
    notifier = notify.Notifier(
        notification_config, notification_queue, target_gpu)
    notifier.start_worker()

    locale = customer['locale']
    locales = read_json(data_path / 'locales.json')
    dr_locale = locales[locale]['DRlocale']
    api_currency = locales[locale]['apiCurrency']

    if notifications['started']['enabled']:
        nvidia.get_product_page(driver, locale, target_gpu)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
            (By.CLASS_NAME, const.BANNER_CLASS)))
        driver.save_screenshot(const.SCREENSHOT_FILE)
        notification_queue.put('started')

    if os.path.isfile('./recaptcha_solver-5.7-fx.xpi') : # Check if user is using recaptcha extension
        logging.info('ReCaptcha solver detected, enabled')
        extension_path = os.path.abspath("recaptcha_solver-5.7-fx.xpi") # Must be the full path to an XPI file!
        driver.install_addon(extension_path, temporary=True)
    else:
        logging.info('ReCaptcha solver not found')

    while True:
        checkout_reached = await checkout_api(
            driver, user_agent, timeout, locale, dr_locale, api_currency, target_gpu, notifications, notification_queue)

        if not checkout_reached:
            sleep(timeout)
            checkout_reached = checkout_selenium(
                driver, timeout, locale, target_gpu, notifications, notification_queue)

        if checkout_reached:
            if payment_method == 'credit-card':
                nvidia.checkout_guest(
                    driver, timeout, customer, auto_submit)
            else:
                nvidia.checkout_paypal(driver, timeout),

            logging.info('Checkout successful!')
            if notifications['checkout']['enabled']:
                driver.save_screenshot(const.SCREENSHOT_FILE)
                notification_queue.put('checkout')

            if auto_submit:
                nvidia.click_recaptcha(driver, timeout)
                order_submitted = nvidia.submit_order(driver, timeout)
                if order_submitted:
                    logging.info('Auto buy successfully submitted!')
                    if notifications['submit']['enabled']:
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        notification_queue.put('submit')
                else:
                    logging.error(
                        'Failed to auto buy! Please solve the reCAPTCHA and submit manually...')
                    if notifications['captcha-fail']['enabled']:
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        while not order_submitted:
                            notification_queue.put('captcha-fail')
                            order_submitted = nvidia.submit_order(
                                driver, timeout)
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        notification_queue.put('submit')
            break
    notification_queue.join()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

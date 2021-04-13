import os
import sys
import json
import logging
import queue
import asyncio
try:
    import coloredlogs
    import colorama

    from pick import pick
    from verboselogs import VerboseLogger
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
except Exception:
    logging.error(
        'Could not import all required modules. '
        'Please run the following command again:\n\n'
        '\tpipenv install\n')
    exit()

from pathlib import Path
from time import sleep

import sniper.api as api
import sniper.checkout as checkout
import sniper.constants as const
import sniper.webdriver as webdriver
import sniper.notifications as notify

logger = VerboseLogger('root')

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'
config_path = src_path.parent / 'config'


def read_json(filename):
    with open(filename, encoding='utf-8') as json_file:
        return json.load(json_file)


def update_sku_file(skus):
    with open(data_path / 'skus.json', 'w+') as f:
        f.write(json.dumps(skus, indent=4))


def read_config():
    try:
        notification_config = read_json(config_path / 'notifications.json')
    except FileNotFoundError:
        logger.critical(
            'Missing notification configuration file, copy the template to config/notifications.json and customize as described in the README to continue.')
        sys.exit()
    except json.decoder.JSONDecodeError:
        logger.critical(
            'Error while parsing the notification configuration file, check config/notifications.json for syntax errors and fix them to continue.')
        sys.exit()

    try:
        customer = read_json(config_path / 'customer.json')
    except FileNotFoundError:
        logger.critical(
            'Missing customer configuration file, copy the template to config/customer.json and customize as described in the README to continue.')
        sys.exit()
    except json.decoder.JSONDecodeError:
        logger.critical(
            'Error while parsing the customer configuration file, check config/customer.json for syntax errors and fix them to continue.')
        sys.exit()
    return notification_config, customer


def setup_logger():
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    coloredlogs.install(level='DEBUG', fmt=log_format)

    file_handler = logging.FileHandler('sniper.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

    logging.getLogger('WDM').disabled = True
    logging.getLogger('apprise').disabled = True
    logging.getLogger('asyncio').disabled = True
    logging.getLogger('apprise.URLBase').disabled = True
    logging.getLogger('urllib3.connectionpool').disabled = True
    logging.getLogger(
        'selenium.webdriver.remote.remote_connection').disabled = True


async def main():
    colorama.init()
    print(const.HEADER)
    setup_logger()

    notification_config, customer = read_config()

    driver = webdriver.create()
    user_agent = driver.execute_script('return navigator.userAgent;')

    gpu_data = read_json(data_path / 'gpus.json')
    target_gpu_name, _ = pick(list(gpu_data.keys()),
                              'Which GPU are you targeting?',
                              indicator='=>')

    payment_method, _ = pick(['credit-card', 'paypal'],
                             'Which payment method do you want to use?',
                             indicator='=>')

    auto_submit = None
    if payment_method == 'credit-card':
        auto_submit, _ = pick(['Yes', 'No'],
                              'Do you want to automatically submit the order?',
                              indicator='=>',  default_index=1)
        auto_submit = auto_submit == 'Yes'

    timeout, _ = pick([' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds', '64 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=1)
    timeout = int(timeout.replace('seconds', '').strip())

    target_gpu = gpu_data[target_gpu_name]

    notifications = notification_config['notifications']
    notification_queue = queue.Queue()
    notifier = notify.Notifier(
        notification_config, notification_queue, target_gpu)
    notifier.start_worker()

    locale = customer['locale']
    locales = read_json(data_path / 'locales.json')
    api_currency = locales[locale]['apiCurrency']
    dr_locale = locales[locale]['DRlocale']
    promo_locale = locales[locale]['PromoLocale'].replace('_', '-').lower()
    api_client = api.Client(user_agent, promo_locale,
                            dr_locale, api_currency, target_gpu)
    api_up = True

    product_ids = read_json(data_path / 'skus.json')
    target_id = product_ids[promo_locale][target_gpu_name]

    logger.info('|---------------------------|')
    logger.info('| Starting Nvidia Sniper 🎯 |')
    logger.info(f'|  Customer locale: {locale}   |')
    logger.info(f'|    Nvidia locale: {promo_locale}   |')
    logger.info(f'|        DR locale: {dr_locale}   |')
    logger.info(f'|         Currency: {api_currency}     |')
    logger.info('|---------------------------|')

    if notifications['started']['enabled']:
        checkout.get_product_page(driver, promo_locale, target_gpu)
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, f'.{const.BANNER_CLASS} .lazyloaded')))
        sleep(1)
        driver.save_screenshot(const.SCREENSHOT_FILE)
        notification_queue.put('started')

    while True:
        in_stock = False
        try:
            logger.info(
                f"Checking {promo_locale} availability for {target_gpu['name']} using API...")
            status = await api_client.check_availability(target_id)
            if not api_up:
                api_up = True
                if notifications['api-up']['enabled']:
                    notification_queue.put('api-up')
            logger.info(f'Inventory status for {target_id}: {status}')
            in_stock = status != 'PRODUCT_INVENTORY_OUT_OF_STOCK'
        except PermissionError:
            logger.error(
                f'Access to inventory API was denied, clearing cookies and trying again...')
            api_client.session.cookie_jar.clear()
            sleep(timeout)
        except LookupError:
            logger.error(
                f'Failed to get inventory status for {target_id}, updating product ID...')
            target_id = None
            while target_id is None:
                target_id = await api_client.get_product_id()
                if target_id is None:
                    logger.warning(
                        f"Product ID for {target_gpu['name']} is not available yet, refreshing product page...")
                    sleep(timeout)
                else:
                    logger.success(
                        f"Found product ID for {target_gpu['name']}: {target_id}")
                    product_ids[promo_locale][target_gpu_name] = target_id
                    logger.info('Updating product ID file...')
                    update_sku_file(product_ids)
        except SystemError as ex:
            error_name = type(ex).__name__
            error_message = '\n'.join(map(str, ex.args)).rstrip()
            logger.error(
                f'Internal API error - {error_name}: {error_message}')
            if api_up:
                api_up = False
                if notifications['api-down']['enabled']:
                    notification_queue.put('api-down')

        if in_stock:
            logger.success(
                f"Found available GPU: {target_gpu['name']}")
            if notifications['availability']['enabled']:
                notification_queue.put('availability')
            store_token = None
            while store_token is None:
                try:
                    logger.info('Fetching API token...')
                    store_token = await api_client.get_token()
                    logger.success('API Token: ' + store_token)
                    logger.info('Overiding store cookies for driver...')
                    store_cookies = api_client.get_cookies(const.STORE_URL)
                    driver.get(const.CART_URL)
                    for key, value in store_cookies.items():
                        driver.add_cookie({'name': key, 'value': value})
                except SystemError:
                    logger.error('Failed to fetch API token, trying again...')

            addded_to_cart = False
            while not addded_to_cart:
                try:
                    logger.info(f'Calling add to cart API for {target_id}...')
                    add_to_cart_response = await api_client.add_to_cart(store_token, target_id)
                    addded_to_cart = True
                    response = add_to_cart_response['message']
                    logger.success(f'Add to cart response: {response}')
                except Exception as ex:
                    error_name = type(ex).__name__
                    error_message = '\n'.join(map(str, ex.args)).rstrip()
                    logger.error(
                        f'Failed to add item to cart - {error_name}: {error_message}')

            checkout_reached = False
            while not checkout_reached:
                try:
                    logger.info('Going to checkout page...')
                    driver.get(const.CHECKOUT_URL)
                    checkout_reached = True
                    if notifications['add-to-cart']['enabled']:
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        notification_queue.put('add-to-cart')
                except (TimeoutException, WebDriverException):
                    logger.error(
                        'Failed to load checkout page, trying again...')

            if payment_method == 'credit-card':
                checkout.checkout_guest(driver, timeout, customer, auto_submit)
            else:
                checkout.checkout_paypal(driver, timeout)

            logger.success('Checkout successfully completed!')
            if notifications['checkout']['enabled']:
                driver.save_screenshot(const.SCREENSHOT_FILE)
                notification_queue.put('checkout')

            if auto_submit:
                checkout.click_recaptcha(driver, timeout)
                order_submitted = checkout.submit_order(driver, timeout)
                if order_submitted:
                    logger.success('Auto buy successfully submitted!')
                    if notifications['submit']['enabled']:
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        notification_queue.put('submit')
                else:
                    logger.error(
                        'Failed to auto buy! Please solve the reCAPTCHA and submit manually...')
                    if notifications['captcha-fail']['enabled']:
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        while not order_submitted:
                            notification_queue.put('captcha-fail')
                            order_submitted = checkout.submit_order(
                                driver, timeout)
                        driver.save_screenshot(const.SCREENSHOT_FILE)
                        notification_queue.put('submit')
            break
        else:
            sleep(timeout)

    await api_client.session.close()
    notification_queue.join()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

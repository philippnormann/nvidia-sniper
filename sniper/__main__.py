import json
import logging
import colorama

from pathlib import Path

from pick import pick
from colorama import Fore, Style
import sniper.nvidia as nvidia
import sniper.webdriver as webdriver
import sniper.notifications as notify

HEADER = f'''
{Fore.GREEN}
███╗   ██╗██╗   ██╗██╗██████╗ ██╗ █████╗     
████╗  ██║██║   ██║██║██╔══██╗██║██╔══██╗    
██╔██╗ ██║██║   ██║██║██║  ██║██║███████║    
██║╚██╗██║╚██╗ ██╔╝██║██║  ██║██║██╔══██║    
██║ ╚████║ ╚████╔╝ ██║██████╔╝██║██║  ██║    
╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝    
{Fore.RED}
███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}
'''
SCREENSHOT_FILE = 'screenshot.png'

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'


def read_json(filename):
    with open(data_path / filename, encoding='utf-8') as json_file:
        return json.load(json_file)


if __name__ == '__main__':
    colorama.init()
    print(HEADER)

    log_format = '%(asctime)s nvidia-sniper: %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    customer = read_json('customer.json')
    locale = customer['locale']
    notifications = customer['notifications']

    gpu_data = read_json('gpus.json')
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

    timeout, _ = pick([' 2 seconds', ' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=2)
    timeout = int(timeout.replace('seconds', '').strip())

    driver = webdriver.create()
    target_gpu = gpu_data[target_gpu]
    
    if notifications['started']['enabled']:
        notify.send_notifications(
            target_gpu, 'started', notifications)

    while True:
        logging.info(
            f"Checking {locale} availability for {target_gpu['name']}...")
        nvidia.get_product_page(driver, locale, target_gpu)
        gpu_available = nvidia.check_availability(driver, timeout)
        if gpu_available:
            logging.info(f"Found available GPU: {target_gpu['name']}")
            if notifications['availability']['enabled']:
                driver.save_screenshot(SCREENSHOT_FILE)
                notify.send_notifications(target_gpu, 'availability', notifications)
            added_to_basket = False
            while not added_to_basket:
                logging.info(f'Trying to add to basket...')
                added_to_basket = nvidia.add_to_basket(driver, timeout)
                if not added_to_basket:
                    logging.info(f'Add to basket click failed, trying again!')

            logging.info(f'Add to basket click suceeded!')
            if notifications['add-to-basket']['enabled']:
                driver.save_screenshot(SCREENSHOT_FILE)
                notify.send_notifications(target_gpu, 'add-to-basket', notifications)
            logging.info('Going to checkout page...')
            checkout_reached = nvidia.to_checkout(driver, timeout, locale)
            if checkout_reached:
                if payment_method == 'credit-card':
                    nvidia.checkout_guest(driver, timeout, customer, auto_submit)
                else:
                    nvidia.checkout_paypal(driver, timeout),

                logging.info('Checkout successful!')
                if notifications['checkout']['enabled']:
                    driver.save_screenshot(SCREENSHOT_FILE)
                    notify.send_notifications(target_gpu, 'checkout', notifications)

                if auto_submit:
                    nvidia.click_recaptcha(driver, timeout)
                    order_submitted = nvidia.submit_order(driver, timeout)
                    if order_submitted:
                        logging.info('Auto buy successfully submitted!')
                        if notifications['submit']['enabled']:
                            driver.save_screenshot(SCREENSHOT_FILE)
                            notify.send_notifications(target_gpu, 'submit', notifications)
                    else:
                        logging.error(
                            'Failed to auto buy! Please solve the reCAPTCHA and submit manually...')
                        if notifications['captcha-fail']['enabled']:
                            driver.save_screenshot(SCREENSHOT_FILE)
                            notify.send_notifications(
                                target_gpu, 'captcha-fail', notifications)
                break
            else:
                logging.error('Lost basket and failed to checkout, trying again...')

        else:
            logging.info('GPU currently not available')

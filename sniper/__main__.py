import json
import logging
import colorama

from pathlib import Path
from time import sleep

from pick import pick
from selenium import webdriver
from colorama import Fore, Style
from selenium.webdriver.firefox.options import Options, FirefoxProfile

from selenium.webdriver.common.by import By
import sniper.checkout as checkout

header = f'''
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

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'


def read_json(filename):
    with open(data_path / filename, encoding='utf-8') as json_file:
        return json.load(json_file)


if __name__ == '__main__':
    colorama.init()
    print(header)

    log_format = '%(asctime)s nvidia-sniper: %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    customer = read_json('customer.json')
    gpu_data = read_json('gpus.json')

    gpus = list(gpu_data.keys())

    target_gpu, _ = pick(gpus, 'Please choose a GPU target', indicator='=>')
    target_url = gpu_data[target_gpu]['url']

    payment_method, _ = pick(['credit-card', 'paypal'],
                             'Please choose a payment method', indicator='=>')

    image_loading, _ = pick(['enabled', 'disabled'],
                            'Please choose if images should be loaded', indicator='=>')

    timeout, _ = pick([' 2 seconds', ' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=2)
    timeout = int(timeout.replace('seconds', '').strip())

    profile = FirefoxProfile()
    if image_loading == 'disabled':
        profile.set_preference('permissions.default.image', 2)

    driver = webdriver.Firefox(firefox_profile=profile)

    while True:
        success = checkout.add_to_basket(
            driver, timeout, customer['locale'], target_url)
        if success:
            checkout.to_checkout(driver, timeout, customer['locale'])
            if payment_method == 'credit-card':
                checkout.checkout_guest(driver, timeout, customer)
            else:
                checkout.checkout_paypal(driver, timeout),
            logging.info('Checkout successful!')
            break
        else:
            logging.info('GPU currently not available')

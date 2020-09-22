import json
import logging
import colorama
import random
import string
import apprise

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

    no_image_loading, _ = pick(['Yes', 'No'],
                               'Do you want to disable image loading?', indicator='=>')
    no_image_loading = no_image_loading == 'Yes'

    timeout, _ = pick([' 2 seconds', ' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=2)
    timeout = int(timeout.replace('seconds', '').strip())

    randomstring = ''.join(random.choice(string.ascii_lowercase)
                           for i in range(10))
    startnumber = 0

    profile = FirefoxProfile()
    if no_image_loading:
        profile.set_preference('permissions.default.image', 2)

    driver = webdriver.Firefox(firefox_profile=profile)
    target_url = gpu_data[target_gpu]['url']

    while True:
        anticache = "?" + str(randomstring) + "=" + str(startnumber)
        success = checkout.add_to_basket(
            driver, timeout, customer['locale'], target_url, anticache)
        if success:
            checkout.to_checkout(driver, timeout, customer['locale'])
            if payment_method == 'credit-card':
                checkout.checkout_guest(driver, timeout, customer, auto_submit)
            else:
                checkout.checkout_paypal(driver, timeout),

            logging.info('Checkout successful!')
            driver.save_screenshot('screenshot.png')

            for name, service in customer['notification'].items():
                logging.info(f'Sending notifications to {name}')
                apobj = apprise.Apprise()
                apobj.add(service['url'])
                if service['screenshot']:
                    apobj.notify(
                        title=service['title'],
                        body=service['message'],
                        attach='screenshot.png'
                    )
                else:
                    apobj.notify(
                        title=service['title'],
                        body=service['message'],
                    )
            break
        else:
            logging.info('GPU currently not available')
        startnumber += 1

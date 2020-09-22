import os
import json
import logging
import colorama
import apprise
import configparser

from pathlib import Path
from time import sleep
from sys import platform

from pick import pick
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options, FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
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


def get_default_profile():
    if platform == 'linux' or platform == 'linux2':
        mozilla_profile = Path(os.getenv('HOME')) / '.mozilla' / 'firefox'
    elif platform == 'darwin':
        mozilla_profile = Path(os.getenv('HOME')) / \
            'Library' / 'Application Support' / 'Firefox'
    elif platform == 'win32':
        mozilla_profile = Path(os.getenv('APPDATA')) / 'Mozilla' / 'Firefox'

    mozilla_profile_ini = mozilla_profile / 'profiles.ini'
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    return mozilla_profile / profile.get('Profile0', 'Path')


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

    timeout, _ = pick([' 2 seconds', ' 4 seconds', ' 8 seconds', '16 seconds', '32 seconds'],
                      'Please choose a timout / refresh interval', indicator='=>', default_index=2)
    timeout = int(timeout.replace('seconds', '').strip())

    default_profile = get_default_profile().resolve()
    profile = FirefoxProfile(default_profile)
    profile.set_preference('dom.webdriver.enabled', False)
    profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()

    driver = webdriver.Firefox(
        firefox_profile=profile, executable_path=GeckoDriverManager().install())

    target_url = gpu_data[target_gpu]['url']

    while True:
        success = checkout.add_to_basket(
            driver, timeout, customer['locale'], target_url)
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

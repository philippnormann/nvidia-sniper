import json
import logging

from pathlib import Path
from time import sleep

from pick import pick
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
import sniper.checkout as checkout

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

header = f"""
{bcolors.OKGREEN}
███╗   ██╗██╗   ██╗██╗██████╗ ██╗ █████╗     
████╗  ██║██║   ██║██║██╔══██╗██║██╔══██╗    
██╔██╗ ██║██║   ██║██║██║  ██║██║███████║    
██║╚██╗██║╚██╗ ██╔╝██║██║  ██║██║██╔══██║    
██║ ╚████║ ╚████╔╝ ██║██████╔╝██║██║  ██║    
╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝    
{bcolors.FAIL}
███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
{bcolors.ENDC}
"""

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'


def read_json(filename):
    with open(data_path / filename, encoding='utf-8') as json_file:
        return json.load(json_file)


if __name__ == "__main__":
    print(header)

    log_format = '%(asctime)s nvidia-sniper: %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    customer = read_json('customer.json')
    gpu_data = read_json('gpus.json')

    gpus = list(gpu_data.keys())

    target_gpu, _ = pick(gpus, 'Please choose a GPU target', indicator='=>')
    target_url = gpu_data[target_gpu]['url']

    payment_method, _ = pick(["credit-card", "paypal"],
                             'Please choose a payment method', indicator='=>')
    
    driver = webdriver.Firefox()

    while True:
        success = checkout.add_to_basket(
            driver, target_url, customer['locale'])
        if success:
            checkout.to_checkout(driver, customer['locale'])
            if payment_method == 'credit-card':
                checkout.checkout_guest(driver, customer)
            else:
                checkout.checkout_paypal(driver)
            logging.info('Checkout successful!')
            break
        else:
            logging.info('GPU currently not available')

import logging
try:
    from colorama import Fore, Style
except Exception:
    logging.error(
        'Could not import all required modules. '\
        'Please run the following command again:\n\n'\
        '\tpipenv install\n')
    exit()

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

BANNER_CLASS = 'singleSlideBanner'
ADD_TO_BASKET_SELECTOR = f'.{BANNER_CLASS} .js-add-button'
PRODUCT_ITEM_SELECTOR = f'.{BANNER_CLASS} .js-product-item'
PRODUCT_ID_ATTR = 'data-digital-river-id'
CHECKOUT_BUTTON_SELECTOR = '.cart .js-checkout'
CART_ICON_CLASS = 'nav-cart-link'
CHECKOUT_AS_GUEST_ID = 'btnCheckoutAsGuest'
SUBMIT_BUTTON_SELECTOR = '#dr_siteButtons > .dr_button'
PAYPAL_BUTTON_ID = 'lnkPayPalExpressCheckout'

RECAPTCHA_FRAME_SELECTOR = "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']"
RECAPTCHA_BOX_XPATH = "//span[@id='recaptcha-anchor']"

STORE_HOST = 'store.nvidia.com'
STORE_URL = f'https://{STORE_HOST}/store'

CART_URL = f'{STORE_URL}/nvidia/cart'
TOKEN_URL = f'{STORE_URL}/nvidia/SessionToken'
CHECKOUT_URL = f'{STORE_URL}?Action=DisplayHGOP2LandingPage&SiteID=nvidia'

API_HOST = 'api-prod.nvidia.com'
INVENTORY_URL = f'https://{API_HOST}/direct-sales-shop/DR/products'
ADD_TO_CART_URL = f'https://{API_HOST}/direct-sales-shop/DR/add-to-cart'

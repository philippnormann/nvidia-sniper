from colorama import Fore, Style

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

ADD_TO_BASKET_SELECTOR = '.singleSlideBanner .js-add-button'
PRODUCT_ITEM_SELECTOR = '.singleSlideBanner .js-product-item'
CHECKOUT_BUTTON_CLASS = 'cart__checkout-button'
CART_ICON_CLASS = 'nav-cart-link'
CHECKOUT_AS_GUEST_ID = 'btnCheckoutAsGuest'
SUBMIT_BUTTON_SELECTOR = '#dr_siteButtons > .dr_button'
PAYPAL_BUTTON_ID = 'lnkPayPalExpressCheckout'

RECAPTCHA_FRAME_SELECTOR = "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']"
RECAPTCHA_BOX_XPATH = "//span[@id='recaptcha-anchor']"

TOKEN_URL = 'https://store.nvidia.com/store/nvidia/SessionToken'
ADD_TO_CART_URL = 'https://api-prod.nvidia.com/direct-sales-shop/DR/add-to-cart'
INVENTORY_URL = 'https://api-prod.nvidia.com/direct-sales-shop/DR/products/'

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
CHECKOUT_BUTTON_CLASS = 'cart__checkout-button'
CART_ICON_CLASS = 'nav-cart-link'
CHECKOUT_AS_GUEST_ID = 'btnCheckoutAsGuest'
SUBMIT_BUTTON_SELECTOR = '#dr_siteButtons > .dr_button'
PAYPAL_BUTTON_ID = 'lnkPayPalExpressCheckout'

RECAPTCHA_FRAME_SELECTOR = "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']"
RECAPTCHA_BOX_XPATH = "//span[@id='recaptcha-anchor']"

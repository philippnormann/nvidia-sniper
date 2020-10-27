import aiohttp

from bs4 import BeautifulSoup

import sniper.constants as const


class Client():
    def __init__(self, user_agent, promo_locale, dr_locale, api_currency, target_gpu):
        self.promo_locale = promo_locale
        self.dr_locale = dr_locale
        self.api_currency = api_currency
        self.target_gpu = target_gpu
        self.online = False
        self.dr_id = None
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': user_agent}, cookie_jar=aiohttp.CookieJar())

    def get_cookies(self, host):
        cookies = self.session.cookie_jar.filter_cookies(host)
        return {key: morsel.value for key, morsel in cookies.items()}

    async def check_availability(self, dr_id):
        async with self.session.get(f'{const.INVENTORY_URL}/{self.dr_locale}/{self.api_currency}/{dr_id}') as response:
            if response.status == 200:
                json_resp = await response.json()
                return json_resp['products']['product'][0]['inventoryStatus']['status']
            elif response.status == 403:
                raise(PermissionError(response.status, await response.text()))
            elif 400 <= response.status < 500:
                raise(LookupError(response.status, await response.text()))
            elif 500 <= response.status < 600:
                raise(SystemError(response.status, await response.text()))

    async def get_product_id(self):
        full_url = f"https://www.nvidia.com/{self.promo_locale}{self.target_gpu['url']}"
        async with self.session.get(full_url) as resp:
            soup = BeautifulSoup(await resp.text(), features="html.parser")
            product = soup.select_one(const.PRODUCT_ITEM_SELECTOR,
                                      attrs={const.PRODUCT_ID_ATTR: True})
            return product[const.PRODUCT_ID_ATTR] if product is not None else None

    async def get_token(self):
        async with self.session.get(f'{const.TOKEN_URL}?locale={self.dr_locale}') as response:
            if response.status == 200:
                json_resp = await response.json()
                return json_resp['session_token']
            else:
                raise(SystemError(await response.text()))

    async def add_to_cart(self, store_token, dr_id):
        async with self.session.post(const.ADD_TO_CART_URL,
                                     headers={'nvidia_shop_id': store_token},
                                     json={"products": [{"productId": dr_id, "quantity": 1}]}) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise(SystemError(await response.text()))

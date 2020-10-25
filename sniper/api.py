import aiohttp

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

    async def fetch_token(self):
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

    async def get_inventory_status(self, dr_id):
        async with self.session.get(f'{const.INVENTORY_URL}/{self.dr_locale}/{self.api_currency}/{dr_id}') as response:
            if response.status == 200:
                json_resp = await response.json()
                return json_resp['products']['product'][0]['inventoryStatus']['status']
            else:
                raise(SystemError(await response.text()))

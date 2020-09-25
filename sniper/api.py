import sniper.constants as const


async def fetch_token(session, dr_locale):
    async with session.get(f'{const.TOKEN_URL}?locale={dr_locale}') as response:
        json_resp = await response.json()
        return json_resp['session_token']


async def add_to_cart(session, store_token, dr_locale, dr_id):
    async with session.post(const.ADD_TO_CART_URL,
                            headers={'nvidia_shop_id': store_token},
                            json={"products": [{"productId": dr_id, "quantity": 1}]}) as response:
        if response.status == 203:
            return await response.json()
        else:
            raise(SystemError(await response.text()))


async def get_inventory_status(session, dr_locale, api_currency, dr_id):
    async with session.get(f'{const.INVENTORY_URL}/{dr_locale}/{api_currency}/{dr_id}') as response:
        json_resp = await response.json()
        return json_resp['products']['product'][0]['inventoryStatus']['status']

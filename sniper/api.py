import asyncio
import logging
import sniper.constants as const

# TODO: Review if json is correct to be set as None, should not matter but just in case
async def http_post(session, url, timeout=60, headers=None, json=None, attempt=0, retries=3, retry=True):
    try:
        async with session.post(url, timeout=timeout, headers=headers, json=json) as response:
            if response.status == 200:
                return response
            else:
                raise(SystemError(await response.text()))
    except asyncio.TimeoutError as error:
        if (attempt < retries and retry) or (retries == 0 and retry):
            next_attempt = attempt + 1

            logging.info(f'Request to {url} failed, trying again')

            return await http_post(
                session=session, 
                url=url, 
                timeout=timeout, 
                headers=headers,
                json=json,
                attempt=next_attempt, 
                retries=retries, 
                retry=True
            )
        else:
            raise(error)

async def http_get(session, url, timeout=60, headers=None, attempt=0, retries=3, retry=True):
    try:
        async with session.get(url, timeout=timeout, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise(SystemError(await response.text()))
    except asyncio.TimeoutError as error:
        if (attempt < retries and retry) or (retries == 0 and retry):
            next_attempt = attempt + 1

            logging.info(f'Request to {url} failed, trying again')

            return await http_get(
                session=session, 
                url=url, 
                timeout=timeout, 
                headers=headers, 
                attempt=next_attempt, 
                retries=retries, 
                retry=True
            )
        else:
            raise(error)

async def fetch_token(session, dr_locale):
    response = await http_get(f'{const.TOKEN_URL}?locale={dr_locale}')
    
    return response['session_token']


async def add_to_cart(session, store_token, dr_locale, dr_id):
    response = await http_post(
        session=session, 
        url=const.ADD_TO_CART_URL,
        timeout=5,
        headers={'nvidia_shop_id': store_token},
        json={"products": [{"productId": dr_id, "quantity": 1}]}
    )

    return response


async def get_inventory_status(session, dr_locale, api_currency, dr_id):
    response = await http_get(session=session, url=f'{const.INVENTORY_URL}/{dr_locale}/{api_currency}/{dr_id}', timeout=10)
    
    return response['products']['product'][0]['inventoryStatus']['status']

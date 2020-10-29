import sys
import json
import string
import itertools
import asyncio
from pathlib import Path

import aiohttp
from tqdm import tqdm
from bs4 import BeautifulSoup
from asyncio_throttle import Throttler
from pick import pick

src_path = Path(__file__).parent
data_path = src_path.parent / 'data'


def read_json(filename):
    with open(filename, encoding='utf-8') as json_file:
        return json.load(json_file)


def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


async def retrieve_sku(client, promo_locale, gpu_name, gpu_data,  throttler, pbar):
    url_locale = promo_locale.replace('_', '-').lower()
    full_url = f"https://www.nvidia.com/{url_locale}{gpu_data['url']}"
    async with throttler:
        async with client.get(full_url) as resp:
            pbar.update(1)
            soup = BeautifulSoup(await resp.text(), features="html.parser")
            product = soup.select_one('.singleSlideBanner .js-product-item',
                                      attrs={'data-digital-river-id': True})
            sku = product['data-digital-river-id'] if product is not None else None
            if sku is not None:
                pbar.write(
                    f'Found SKU in {promo_locale} for {gpu_name}: {sku}')
            return promo_locale, gpu_name, sku


async def crawl_skus():
    skus = read_json(data_path / 'skus.json')
    gpus = read_json(data_path / 'gpus.json')

    tasks = []
    throttler = Throttler(rate_limit=10)
    pbar = tqdm(total=len(skus) * len(gpus), desc="Crawling SKUs", unit="SKU")

    async with aiohttp.ClientSession() as client:
        for promo_locale in skus.keys():
            for gpu_name, gpu_data in gpus.items():
                tasks.append(retrieve_sku(
                    client,  promo_locale,
                    gpu_name, gpu_data,
                    throttler, pbar))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for locale, model, new_sku in results:
            current_sku = skus[locale][model]
            if new_sku is not None and current_sku != new_sku:
                pbar.write(
                    f'Updating SKU for {model} in {locale}: {current_sku} -> {new_sku}')
                skus[locale][model] = new_sku
            elif new_sku is not None and current_sku == new_sku:
                pbar.write(
                    f'SKU confirmed for {model} in {locale}: {new_sku}')

    with open(data_path / 'skus.json', 'w+') as f:
        f.write(json.dumps(skus, indent=4))


async def check_availability(client, dr_id, dr_locale, currency, throttler, pbar):
    full_url = f"https://api-prod.nvidia.com/direct-sales-shop/DR/products/{dr_locale}/{currency}/{dr_id}"
    async with throttler:
        async with client.get(full_url) as resp:
            pbar.update(1)
            json_resp = await resp.json()
            if 'products' in json_resp and len(json_resp['products']['product']) > 0:
                product_name = json_resp['products']['product'][0]['name']
                pbar.write(
                    f'Found valid SKU in {dr_locale} for {product_name}: {dr_id}')
                return dr_locale, dr_id, product_name
            else:
                return None


async def enumerate_skus(locale, prefix):
    locales = read_json(data_path / 'locales.json')
    trailing_zeroes = 2
    variable_digits = 10 - len(prefix) - trailing_zeroes
    throttler = Throttler(rate_limit=10)
    candidates = set(itertools.product(string.digits, repeat=variable_digits))
    pbar = tqdm(total=len(candidates), desc="Enumerating SKUs", unit="SKU")

    async with aiohttp.ClientSession() as client:
        for var_digit_chunk in grouper(1000, candidates):
            tasks = []
            for var_digits in var_digit_chunk:
                full_sku = prefix + ''.join(var_digits) + "0" * trailing_zeroes
                tasks.append(check_availability(
                    client, full_sku,
                    locales[locale]['DRlocale'],
                    locales[locale]['apiCurrency'],
                    throttler, pbar))
            await asyncio.gather(*tasks)


async def check_product_status(client, dr_locale, throttler, pbar):
    params = {'page': '1',
              'limit': '10',
              'locale': dr_locale,
              'category': 'GPU',
              'manufacturer': 'NVIDIA'}
    async with throttler:
        pbar.write(f'Checking {dr_locale} product status...')
        async with client.get('https://api.nvidia.partners/edge/product/search', params=params) as resp:
            pbar.update(1)
            if resp.status == 200:
                json_resp = await resp.json()
                if json_resp is not None:
                    results = json_resp["searchedProducts"]
                    products = [results['featuredProduct']] + \
                        results['productDetails']
                    locale_status = {}
                    for product in products:
                        if '30' in product['gpu']:
                            pbar.write(f"Status for {product['gpu']} in {dr_locale}: {product['prdStatus']}")
                            locale_status[product["gpu"]] = product['prdStatus']
                    return dr_locale, locale_status
                else:
                    pbar.write(
                        f'Product status check failed for {dr_locale} - no result')
            else:
                pbar.write(
                    f'Product status check failed for {dr_locale} - status code: {resp.status}')


async def check_worldwide_status():
    locales = read_json(data_path / 'locales.json')
    dr_locales = set(locale['DRlocale'].replace('_', '-')
                     for locale in locales.values())
    pbar = tqdm(total=len(dr_locales),
                desc="Checking worldwide product status", unit="locale")
    throttler = Throttler(rate_limit=5)

    async with aiohttp.ClientSession() as client:
        tasks = []
        for dr_locale in dr_locales:
            tasks.append(check_product_status(
                client, dr_locale, throttler, pbar))
        status_results = {res[0]: res[1] for res in await asyncio.gather(*tasks, return_exceptions=True) if res is not None}

    with open(data_path / 'status.json', 'w+') as f:
        pbar.write(f'Writing status results to data/status.json')
        f.write(json.dumps(status_results, indent=4, sort_keys=True))


async def main():
    mode, _ = pick(['check-worldwide-status', 'crawl-skus', 'enumerate-skus'],
                   'How do you want to scout?', indicator='=>')

    if mode == 'check-worldwide-status':
        await check_worldwide_status()
    elif mode == 'enumerate-skus':
        locale = input('Locale (default: de-de): ') or 'de-de'
        prefix = input('Prefix (default: 54387): ') or '54387'
        await enumerate_skus(locale, prefix)
    elif mode == 'crawl-skus':
        await crawl_skus()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

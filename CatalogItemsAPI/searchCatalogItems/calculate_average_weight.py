from dotenv import load_dotenv
import os
from sp_api.api import CatalogItems
from sp_api.base import Marketplaces
from common.rate_limiter import RateLimiter


def weight_to_grams(weight_info):
    unit = weight_info['unit']
    weight = weight_info['value']
    if unit == 'grams':
        return weight
    elif unit == 'kilograms':
        return weight * 1000
    elif unit == 'ounces':
        return weight * 28.3495
    elif unit == 'pounds':
        return weight * 453.592
    elif unit == 'milligrams':
        return weight / 1000
    else:
        return None


rate_limiter = RateLimiter(tokens_per_second=5, capacity=5)

load_dotenv()

refresh_token = os.getenv('refresh_token')
lwa_app_id = os.getenv('lwa_app_id')
lwa_client_secret = os.getenv('lwa_client_secret')

credentials = dict(
    refresh_token=refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret
)

next_token = None

keywords_to_find = 'ancient magnesium glycinate oil spray'
product_weight_with_units = []

try:
    catalog_api = CatalogItems(credentials=credentials,
                               marketplace=Marketplaces.DE, version="2022-04-01")
    response = catalog_api.search_catalog_items(marketplaceIds=Marketplaces.DE.marketplace_id, keywords=[
        keywords_to_find], pageSize=20, includedData=['attributes'])

    try:
        next_token = response.pagination['nextToken']
    except:
        next_token = None

    for item in response.payload['items']:
        try:
            weight = item['attributes']['item_weight']
        except:
            try:
                weight = item['attributes']['item_package_weight']
            except:
                weight = None
        product_weight_with_units.append(weight)

    while next_token:
        response = rate_limiter.send_request(catalog_api.search_catalog_items,
                                             marketplaceIds=Marketplaces.DE.marketplace_id, keywords=[
                keywords_to_find], pageSize=20, pageToken=next_token, includedData=['attributes'])
        for item in response.payload['items']:
            try:
                weight = item['attributes']['item_weight']
            except:
                try:
                    weight = item['attributes']['package_weight']
                except:
                    weight = None
            product_weight_with_units.append(weight)
        try:
            next_token = response.pagination['nextToken']
        except:
            next_token = None

except Exception as e:
    print(e)

product_weight_with_units = [
    weight for weight in product_weight_with_units if weight is not None]
product_weights_in_grams = []

for weight in product_weight_with_units:
    weight_in_grams = weight_to_grams(weight[0])
    if weight_in_grams:
        product_weights_in_grams.append(weight_in_grams)

average_weight = sum(product_weights_in_grams) / len(product_weights_in_grams)

print(average_weight)

from dotenv import load_dotenv
import os
from sp_api.api import CatalogItems
from sp_api.base import Marketplaces
from common.rate_limiter import RateLimiter

load_dotenv()

refresh_token = os.getenv('refresh_token')
lwa_app_id = os.getenv('lwa_app_id')
lwa_client_secret = os.getenv('lwa_client_secret')

credentials = dict(
    refresh_token=refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret
)
rate_limiter = RateLimiter(tokens_per_second=5, capacity=5)
next_token = None

keywords_to_find = 'Competing in the Age of AI'
pages_needed = 0
page_size = 5
items_info = []

try:
    catalog_api = CatalogItems(credentials=credentials,
                              marketplace=Marketplaces.DE, version="2022-04-01")
    response = catalog_api.search_catalog_items(marketplaceIds="A1PA6795UKMFR9", keywords=[
                                               keywords_to_find], pageSize=page_size, includedData=['attributes'])
    items_info.extend(response.payload['items'])
    pages_needed += 1
    try:
        next_token = response.pagination['nextToken']
    except:
        next_token = None
    while next_token:
        response = rate_limiter.send_request(catalog_api.search_catalog_items, marketplaceIds="A1PA6795UKMFR9", keywords=[
                                             keywords_to_find], pageSize=page_size, pageToken=next_token, includedData=['attributes'])
        items_info.extend(response.payload['items'])
        pages_needed += 1
        try:
            next_token = response.pagination['nextToken']
        except:
            next_token = None

except Exception as e:
    print(e)

print("Results per page: ")
print(page_size)
print("Number of pages needed: ")
print(pages_needed)
print("Books having the chosen title: ")
print(len(items_info))

print("Authors of the books: ")
authors_counter = 1
for book in items_info:
    print(authors_counter, " - ", book['attributes']['author'][0]['value'])
    authors_counter += 1

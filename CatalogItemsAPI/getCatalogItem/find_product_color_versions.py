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

# product url: https://www.amazon.com/dp/B0D14H2YBZ
# product: Kids Water Bottle

asin = 'B0D14H2YBZ'
page_size = 5
items_colors = []

try:
    catalog_api = CatalogItems(credentials=credentials,
                              marketplace=Marketplaces.US, version="2022-04-01")
    response = rate_limiter.send_request(catalog_api.get_catalog_item, marketplaceIds="ATVPDKIKX0DER",
                                         asin=asin, pageSize=page_size, includedData=['relationships,summaries'])

    # get parent asin
    parent_asin = response.payload['relationships'][0]['relationships'][0]['parentAsins'][0]

    # get all child asins of the parent asin
    response = rate_limiter.send_request(catalog_api.get_catalog_item, marketplaceIds="ATVPDKIKX0DER",
                                         asin=parent_asin, pageSize=page_size, includedData=['relationships,summaries'])
    child_asins = response.payload['relationships'][0]['relationships'][0]['childAsins']

    # for each child asin get its color and save it to itemsColors list
    for child_asin in child_asins:
        response = rate_limiter.send_request(
            catalog_api.get_catalog_item, marketplaceIds="ATVPDKIKX0DER", asin=child_asin, pageSize=page_size, includedData=['summaries'])
        items_colors.append(response.payload['summaries'][0]['color'])

except Exception as e:
    print(e)

print("\nColors of the product: ")
for color in items_colors:
    print(color)

print("\nNumber of colors: ")
print(len(items_colors))

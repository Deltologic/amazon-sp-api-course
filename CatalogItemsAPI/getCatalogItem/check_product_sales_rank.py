from dotenv import load_dotenv
import os
from sp_api.api import CatalogItems
from sp_api.base import Marketplaces
from common.rate_limiter import RateLimiter


class SalesRank:
    def __init__(self, rank, category):
        self.rank = rank
        self.category = category

    def __str__(self):
        return f"Rank: {self.rank}, Category: {self.category}"


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

# product url: https://www.amazon.com/dp/B07RFSSYBH
# product: "Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones" book
asin = 'B07RFSSYBH'
page_size = 5
sales_ranks = []

try:
    catalog_api = CatalogItems(credentials=credentials,
                               marketplace=Marketplaces.US, version="2022-04-01")
    response = rate_limiter.send_request(catalog_api.get_catalog_item, marketplaceIds="ATVPDKIKX0DER",
                                         asin=asin, pageSize=page_size, includedData=['summaries,salesRanks'])
    ranks = response.payload['salesRanks'][0]['classificationRanks']
    for rank in ranks:
        rank_with_category = SalesRank(rank['rank'], rank['title'])
        sales_ranks.append(rank_with_category)

except Exception as e:
    print(e)

print("\nSales ranks of the book: ")
for rank in sales_ranks:
    print(rank)

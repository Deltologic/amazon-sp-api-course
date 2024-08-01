from dotenv import load_dotenv
import os
from sp_api.api import Orders
from sp_api.base import Marketplaces
from common.rate_limiter import RateLimiter
from collections import Counter


load_dotenv()

refresh_token = os.getenv('refresh_token')
lwa_app_id = os.getenv('lwa_app_id')
lwa_client_secret = os.getenv('lwa_client_secret')

credentials = dict(
    refresh_token=refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret
)
rate_limiter = RateLimiter(tokens_per_second=0.0167, capacity=20)

orders = []

try:
    orders_api = Orders(marketplace=Marketplaces.US, credentials=credentials)
    response = rate_limiter.send_request(orders_api.get_orders, OrderStatuses=[
                                         'Shipped'], CreatedAfter='2024-05-31T23:59:59', CreatedBefore='2024-06-05T00:00:00', MarketplaceIds=['ATVPDKIKX0DER'])
    orders.extend(response.payload['Orders'])
    try:
        next_token = response.payload['NextToken']
    except:
        next_token = None
    while next_token:
        response = rate_limiter.send_request(orders_api.get_orders, OrderStatuses=[
                                             'Shipped'], CreatedAfter='2024-05-31T23:59:59', CreatedBefore='2024-06-05T00:00:00', MarketplaceIds=['ATVPDKIKX0DER'], NextToken=next_token)
        orders.extend(response.payload['Orders'])
        try:
            next_token = response.payload['NextToken']
        except:
            next_token = None

except Exception as e:
    print(e)

print("Number of orders per postal code: ")
postal_codes_count = Counter(
    order['ShippingAddress']['PostalCode']
    for order in orders
    if 'ShippingAddress' in order and 'PostalCode' in order['ShippingAddress']
)
top_5_postalCodes = postal_codes_count.most_common(5)
print(top_5_postalCodes)

print("Number of orders per state: ")
states_count = Counter(order['ShippingAddress']['StateOrRegion'] for order in orders
                      if 'ShippingAddress' in order and 'StateOrRegion' in order['ShippingAddress'])
top_5_states = states_count.most_common(5)
print(top_5_states)

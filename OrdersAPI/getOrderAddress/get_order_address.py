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
rate_limiter = RateLimiter(tokens_per_second=0.5, capacity=30)

order_id = os.getenv('order_id')

try:
    orders_api = Orders(marketplace=Marketplaces.DE, credentials=credentials)
    response = rate_limiter.send_request(
        orders_api.get_order_address, order_id=order_id)

except Exception as e:
    print(e)

print('\nShipping address:')
print('Client name: ', response.payload['ShippingAddress']['Name'])
print('Phone: ', response.payload['ShippingAddress']['Phone'])
print('City: ', response.payload['ShippingAddress']['City'])

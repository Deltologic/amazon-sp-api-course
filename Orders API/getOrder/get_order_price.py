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
price_info = {
    'amount': 0.0,
    'currencyCode': ''
}

try:
    orders_api = Orders(marketplace=Marketplaces.US, credentials=credentials)
    response = rate_limiter.send_request(orders_api.get_order, order_id=order_id)
    price_info['amount'] = response.payload['OrderTotal']['Amount']
    price_info['currencyCode'] = response.payload['OrderTotal']['CurrencyCode']

    print(response)

except Exception as e:
    print(e)

print(price_info)

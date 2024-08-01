from dotenv import load_dotenv
import os
from sp_api.api import Orders
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
rate_limiter = RateLimiter(tokens_per_second=0.5, capacity=30)

order_id = os.getenv('order_id')

try:
    orders_api = Orders(marketplace=Marketplaces.DE, credentials=credentials)
    response = rate_limiter.send_request(
        orders_api.get_order_items, order_id=order_id)

except Exception as e:
    print(e)

summary_shipping_price = 0
summary_tax = 0
summary_shipping_tax = 0

order_items = response.payload['OrderItems']
for order_item in order_items:
    summary_shipping_price_str = order_item.get(
        'ShippingPrice', {}).get('Amount', '0')
    summary_tax_str = order_item.get('ItemTax', {}).get('Amount', '0')
    summary_shipping_tax_str = order_item.get('ShippingTax', {}).get('Amount', '0')

    summary_shipping_price += float(summary_shipping_price_str)
    summary_tax += float(summary_tax_str)
    summary_shipping_tax += float(summary_shipping_tax_str)

print('\n\nSummary shipping price: ', summary_shipping_price)
print('Summary items tax: ', summary_tax)
print('Summary shipping tax: ', summary_shipping_tax)

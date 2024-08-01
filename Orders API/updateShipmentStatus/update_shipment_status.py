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
rate_limiter = RateLimiter(tokens_per_second=5, capacity=15)

order_id = os.getenv('order_id')

try:
    orders_api = Orders(marketplace=Marketplaces.DE, credentials=credentials)
    response = rate_limiter.send_request(
        orders_api.update_shipment_status, order_id=order_id, marketplaceId='A1PA6795UKMFR9', shipmentStatus='ReadyForPickup')

except Exception as e:
    print(e)

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
rate_limiter = RateLimiter(tokens_per_second=2, capacity=10)

order_id = os.getenv('order_id')

try:
    orders_api = Orders(marketplace=Marketplaces.DE, credentials=credentials)
    response = rate_limiter.send_request(
        orders_api.confirm_shipment, order_id=order_id, marketplaceId='A1PA6795UKMFR9', packageDetail={
            'packageReferenceId': '0001',
            'carrierCode': 'DHL',
            "shippingMethod": 'Paket',
            'trackingNumber': '1234567890',
            'shipDate': '2024-07-19T12:00:00Z',
                        'orderItems': [
                            {
                                'orderItemId': '123456789',
                                'quantity': 1
                            },
                            {
                                'orderItemId': '2345678901',
                                'quantity': 2
                            },
                        ]
        })

except Exception as e:
    print(e)

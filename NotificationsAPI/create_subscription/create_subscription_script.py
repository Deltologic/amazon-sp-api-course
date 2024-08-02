import os
from dotenv import load_dotenv
from sp_api.base import Marketplaces
from sp_api.api import Notifications
from create_subscription import create_subscription, NotificationType

# <input part> ==========================================================================================================
# choose the notification type
notification_type=NotificationType.ORDER_CHANGE

destination_id = "4b6776fe-44c8-45f0-acf2-ecc68284e1d8"

# </input part> ==========================================================================================================

load_dotenv()
refresh_token = os.getenv('refresh_token')
lwa_app_id = os.getenv('lwa_app_id')
lwa_client_secret = os.getenv('lwa_client_secret')

credentials = dict(
    refresh_token=refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret
)

notifications_client = Notifications(
    credentials=credentials, marketplace=Marketplaces.PL
)

subscription_id = create_subscription(notifications_client, notification_type, destination_id)
print('Subscription ID:', subscription_id)


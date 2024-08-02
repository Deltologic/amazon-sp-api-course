import os
from dotenv import load_dotenv
from sp_api.base import Marketplaces
from sp_api.api import Notifications

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

destination_name = os.getenv("AWS_EVENTBRIDGE_DESTINATION_NAME")
account_id = os.getenv("ACCOUNT_ID")


destination_id_response = notifications_client.create_destination(
    name=destination_name,
    account_id=account_id,
)
destination_id = destination_id_response.payload.get("destinationId")

print('Destination ID:', destination_id)

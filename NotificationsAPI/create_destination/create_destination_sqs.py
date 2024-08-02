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

sqs_name = os.getenv("AWS_SQS_NAME")
sqs_arn = os.getenv("AWS_SQS_ARN")

notifications_client = Notifications(
    credentials=credentials, marketplace=Marketplaces.PL
)

destination_id_response = notifications_client.create_destination(
    name=sqs_name, arn=sqs_arn)
destination_id = destination_id_response.payload.get("destinationId")

print('Destination ID:', destination_id)

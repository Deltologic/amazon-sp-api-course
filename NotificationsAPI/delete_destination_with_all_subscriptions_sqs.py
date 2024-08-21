import os
from dotenv import load_dotenv
from sp_api.base import Marketplaces
from sp_api.api import Notifications
from sp_api.base import SellingApiNotFoundException
from common.rate_limiter import RateLimiter

# <input part> ==========================================================================================================
# specify the destination name you want to delete
destination_name = "sqs-test"

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

destinations = notifications_client.get_destinations()

destination_id = [destination['destinationId']
                  for destination in destinations.payload if destination['name'] == destination_name][0]

sqs_notification_types = [
    "ACCOUNT_STATUS_CHANGED",
    "ANY_OFFER_CHANGED",
    "B2B_ANY_OFFER_CHANGED",
    "DETAIL_PAGE_TRAFFIC_EVENT",
    "FBA_INVENTORY_AVAILABILITY_CHANGES",
    "FBA_OUTBOUND_SHIPMENT_STATUS",
    "FEE_PROMOTION",
    "FEED_PROCESSING_FINISHED",
    "FULFILLMENT_ORDER_STATUS",
    "ITEM_INVENTORY_EVENT_CHANGE",
    "ITEM_SALES_EVENT_CHANGE",
    "ORDER_CHANGE",
    "PRICING_HEALTH",
    "REPORT_PROCESSING_FINISHED",
]

eventbridge_notification_types = [
    "BRANDED_ITEM_CONTENT_CHANGE",
    "ITEM_PRODUCT_TYPE_CHANGE",
    "LISTINGS_ITEM_STATUS_CHANGE",
    "LISTINGS_ITEM_ISSUES_CHANGE",
    "LISTINGS_ITEM_MFN_QUANTITY_CHANGE",
    "PRODUCT_TYPE_DEFINITIONS_CHANGE"
]

all_notification_types = sqs_notification_types + eventbridge_notification_types

subscriptions_to_delete = []
rate_limiter = RateLimiter(tokens_per_second=1, capacity=5)

for sqs_notification_type in all_notification_types:
    try:
        subscription = rate_limiter.send_request(notifications_client.get_subscription,
                                                 notification_type=sqs_notification_type)
        if subscription.payload:
            subscription_id = subscription.payload['subscriptionId']
            if subscription.payload['destinationId'] == destination_id:
                subscriptions_to_delete.append(
                    (sqs_notification_type, subscription_id))
    except SellingApiNotFoundException:
        pass

for sqs_notification_type, subscription_id in subscriptions_to_delete:
    print(f"Deleting subscription {subscription_id} of type {sqs_notification_type}")
    rate_limiter.send_request(notifications_client.delete_notification_subscription,
                              notification_type=sqs_notification_type, subscription_id=subscription_id)

print("Deleting destination:", destination_id)
notifications_client.delete_destination(destination_id)

print("Destination with its subsciptions deleted")

import os
from dotenv import load_dotenv
from sp_api.base import Marketplaces
from sp_api.api import Notifications
from common.rate_limiter import RateLimiter
from create_subscription.create_subscription import create_subscription, NotificationType

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

sqs_notification_types = [NotificationType.ORDER_CHANGE,
                          NotificationType.FEED_PROCESSING_FINISHED, NotificationType.REPORT_PROCESSING_FINISHED]

eventbridge_notification_types = [NotificationType.LISTINGS_ITEM_STATUS_CHANGE]

# <input part> ==========================================================================================================
# set sqs_handled to True if you want to create sqs-handled notification type
sqs_handled = True

# uncomment this part if you set sqs_handled to True and you want to create new destination
destination_name = os.getenv("AWS_SQS_NAME")
sqs_arn = os.getenv("AWS_SQS_ARN")
destination_id_response = notifications_client.create_destination(name=destination_name, arn=sqs_arn)
destination_id = destination_id_response.payload.get("destinationId")

# uncomment this part if you set sqs_handled to False and you want to create new destination
# destination_name = os.getenv("AWS_EVENTBRIDGE_DESTINATION_NAME")
# account_id=os.getenv("ACCOUNT_ID")
# destination_id_response = notifications_client.create_destination(
#     name=destination_name,
#     account_id=account_id,
# )
# destination_id=destination_id_response.payload.get("destinationId")

# uncomment this part if you don't want to create new destination, but use existing one
# destination_id = "10f0f5ee-59f5-4152-94cd-bcf6c3f99485"

# </input part> ==========================================================================================================

print('Destination ID:', destination_id)


rate_limiter = RateLimiter(tokens_per_second=1, capacity=5)
rate_limiter_to_delete_subscriptions = RateLimiter(
    tokens_per_second=1, capacity=5)

if sqs_handled:
    notification_types = sqs_notification_types
else:
    notification_types = eventbridge_notification_types

for notification_type in notification_types:
    try:
            subscription = rate_limiter.send_request(notifications_client.get_subscription,
                                                    notification_type=notification_type.value)
            print('existing subscription: ', subscription)
            if subscription:
                subscription_response = rate_limiter_to_delete_subscriptions.send_request(
                    notifications_client.delete_notification_subscription,
                        notification_type=notification_type, subscription_id=subscription.payload["subscriptionId"]
                    )
                
                print('deleted subscription:', subscription_response)

    except Exception as e:
        pass
    
    print("Creating subscription for " + notification_type.value)
    subscription_response = create_subscription(
        notifications_client, notification_type=notification_type, destination_id=destination_id)
    print('\n\nnew subscription id:',
            subscription_response, '\n\n')
    
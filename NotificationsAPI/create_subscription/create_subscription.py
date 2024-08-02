from enum import Enum
from sp_api.api import Notifications
from common.rate_limiter import RateLimiter


class NotificationType(Enum):
    REPORT_PROCESSING_FINISHED = "REPORT_PROCESSING_FINISHED"
    ORDER_CHANGE = "ORDER_CHANGE"
    FEED_PROCESSING_FINISHED = "FEED_PROCESSING_FINISHED"
    LISTINGS_ITEM_STATUS_CHANGE = "LISTINGS_ITEM_STATUS_CHANGE"


def create_subscription(notifications_client: Notifications, notification_type: NotificationType, destination_id: str) -> dict:
    rate_limiter = RateLimiter(tokens_per_second=1, capacity=5)
    if notification_type == NotificationType.ORDER_CHANGE:
        response = rate_limiter.send_request(notifications_client.create_subscription,
                                             destination_id=destination_id,
                                             notification_type=notification_type.value,
                                             processingDirective={
                                                 "eventFilter": {
                                                     "orderChangeTypes": ["OrderStatusChange"],
                                                     "eventFilterType": "ORDER_CHANGE"
                                                 }
                                             }
                                             )
    else:
        response = rate_limiter.send_request(notifications_client.create_subscription,
                                             destination_id=destination_id,
                                             notification_type=notification_type.value
                                             )

    return response.payload.get('subscriptionId')

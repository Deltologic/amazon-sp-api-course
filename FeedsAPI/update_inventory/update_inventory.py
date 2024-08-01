from io import BytesIO
from dotenv import load_dotenv
import os
from sp_api.base import Marketplaces
from sp_api.api import Feeds
from create_xml import ProductInventoryChange, create_xml
from feeds_common.feed_types import FeedType

load_dotenv()

refresh_token = os.getenv('refresh_token')
lwa_app_id = os.getenv('lwa_app_id')
lwa_client_secret = os.getenv('lwa_client_secret')

credentials = dict(
    refresh_token=refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret
)

feeds_api_client = Feeds(credentials=credentials, marketplace=Marketplaces.PL)
seller_id = os.getenv('seller_id')
feed_type = FeedType.POST_INVENTORY_AVAILABILITY_DATA.value


# <input part> ==========================================================================================================
products_to_reprice = [ProductInventoryChange(
    'SKU1', 0), ProductInventoryChange('SKU2', 0)]

"""
-> In order to create feed, set feed_id to empty string.
-> In order to get feed creation result, set feed_id to the id of the created feed.

"""
feed_id = ""

# </input part> ==========================================================================================================


if feed_id == "":
    products_to_reprice_xml = create_xml(seller_id, products_to_reprice)

    feed = BytesIO()
    feed.write(products_to_reprice_xml.encode('utf-8'))
    feed.seek(0)

    feed_document_info = feeds_api_client.submit_feed(
        file=feed, content_type="text/xml", feed_type=feed_type)

    feed_document_response = feed_document_info[0].payload
    create_feed_response = feed_document_info[1].payload

    feed_id = create_feed_response['feedId']
    print(feed_id)

else:
    info = feeds_api_client.get_feed(feedId=feed_id)

    processing_status = info.payload.get('processingStatus')

    if processing_status != None:
        result_feed_document_id = info.payload.get('resultFeedDocumentId')

        if result_feed_document_id == None:
            print('Feed result document is not ready yet')
        else:
            feed_document = feeds_api_client.get_feed_document(
                feedDocumentId=result_feed_document_id)

            current_dir = os.getcwd()
            result_file_path = os.path.join(
                current_dir, 'Feeds API', 'update_price', f'feed-result-{feed_id}.xml')
            with open(result_file_path, 'w', encoding='utf-8') as file:
                file.write(feed_document)

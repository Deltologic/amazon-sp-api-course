import ijson
from dotenv import load_dotenv
import os
from sp_api.api import Reports, CatalogItems
from sp_api.base import Marketplaces

from common.report_types import ReportType
from common.processing_statuses import ProcessingStatus
from reports_common.report_model import GetReportByIdModel


# <input part> ==========================================================================================================
"""
    If you want to use report_period = WEEK:
        -> you need to set data_start_time to week start (Sunday) and data_end_time to week end (Saturday)
"""
data_start_time = "2023-01-01T00:00:00Z"
data_end_time = "2023-12-31T23:59:59Z"

"""
    report_period options:
        -> DAY
        -> WEEK
        -> MONTH
        -> YEAR
"""
report_period = "YEAR"

"""
    distributor_view options:
        -> MANUFACTURING
        -> SOURCING
"""

distributor_view = "MANUFACTURING"

"""
    selling_program options:
        -> RETAIL
        -> BUSINESS
        -> FRESH
"""

selling_program= "RETAIL"

# in this example, we are using the DE marketplace
marketplace_id = "A1PA6795UKMFR9"

# set the report_id to None if you want to create a new report
# if you want to download created report, then set the report_id to the id of the report
report_id = None

# </input part> ==========================================================================================================

report_type = ReportType.GET_VENDOR_SALES_REPORT.value

load_dotenv()

refresh_token = os.getenv('refresh_token')
lwa_app_id = os.getenv('lwa_app_id')
lwa_client_secret = os.getenv('lwa_client_secret')

credentials = dict(
    refresh_token=refresh_token,
    lwa_app_id=lwa_app_id,
    lwa_client_secret=lwa_client_secret
)
reports_api_client = Reports(credentials=credentials,
                             marketplace=Marketplaces.FR)

if report_id == None:
    try:
        response = reports_api_client.create_report(
            reportType=report_type,
            dataStartTime=data_start_time,
            dataEndTime=data_end_time,
            reportOptions={
                "reportPeriod": report_period,
                "distributorView": distributor_view,
                "sellingProgram": selling_program
            },
            marketplaceIds=[
                marketplace_id
            ],
        )

        report_id = response.payload['reportId']
    except Exception as e:
        print("An error occurred while creating the report")
        print(e)

    print('report id:', report_id)

else:
    # the request below should be taken after a while (5-10 minutes) to be sure that the report is ready
    report_file_path = f'./reports-downloaded/start-{data_start_time}-end-{data_end_time}-id-{
        report_id}-period-{report_period}-dist-{distributor_view}-program-{selling_program}.json'

    os.makedirs(os.path.dirname(report_file_path), exist_ok=True)

    try:
        response = reports_api_client.get_report(reportId=report_id)
        report_by_id_response = GetReportByIdModel(response.payload)

        if report_by_id_response.processing_status == ProcessingStatus.DONE.value and report_by_id_response.report_document_id != None:
            with open(report_file_path, 'w') as file:
                report_url_response = reports_api_client.get_report_document(
                    reportDocumentId=report_by_id_response.report_document_id, download=True, file=file)
                print(f"Report downloaded successfully at {report_file_path}")
        elif report_by_id_response.processing_status == ProcessingStatus.IN_PROGRESS.value or report_by_id_response.processing_status == ProcessingStatus.IN_QUEUE.value:
            print("The report is not ready yet")
        else:
            print("An error occurred while getting the report")
            print(report_by_id_response.processing_status)
    except Exception as e:
        print("An error occurred while getting the report")
        print(e)


    def find_most_common_ordered_product(file_path, array_key):
            biggest_sales_quantity=0
            biggest_sales_asin=""
            
            with open(file_path, 'rb') as file:
                items = ijson.items(file, f'{array_key}.item')
                for item in items:
                    if item['orderedUnits']>biggest_sales_quantity:
                        biggest_sales_quantity=item['orderedUnits']
                        biggest_sales_asin=item['asin']
            return (biggest_sales_asin, biggest_sales_quantity)
        
    sales_by_asin_key = 'salesByAsin'
    
    most_common_ordered_product = find_most_common_ordered_product(report_file_path, sales_by_asin_key)
    try:
        catalog_api = CatalogItems(credentials=credentials,
                                marketplace=Marketplaces.DE, version="2022-04-01")
        response = catalog_api.get_catalog_item(
            marketplaceIds=marketplace_id, asin=most_common_ordered_product[0], pageSize=10, includedData=['summaries'])
        item_name = response.payload['summaries'][0]['itemName']
    except Exception as e:
        print(e)
    
    print('\n================================================================================================')
    print(f'Most common ordered product in the period: {data_start_time} - {data_end_time}')
    print(most_common_ordered_product[0])
    print(f'Item name: {item_name}')
    print(f'Quantity ordered: {most_common_ordered_product[1]}')

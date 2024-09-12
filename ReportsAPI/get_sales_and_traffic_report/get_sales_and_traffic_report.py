from dotenv import load_dotenv
import os
from sp_api.api import Reports
from sp_api.base import Marketplaces

from common.report_types import ReportType
from common.processing_statuses import ProcessingStatus
from ReportsAPI.reports_common.report_model import GetReportByIdModel

# <input part> ==========================================================================================================
"""
    If you want to use date_granularity = WEEK:
        -> it is a good practice to use set data_start_time to week start (Sunday) and data_end_time to week end (Saturday)
    If you you want to use date_granularity = MONTH:
        -> it is a good practice to use set data_start_time to month start and data_end_time to month end
"""
data_start_time = "2024-06-25T00:00:00Z"
data_end_time = "2024-07-01T00:00:00Z"

"""
    date_granularity options:
        -> DAY
        -> WEEK
        -> MONTH
"""
date_granularity = "DAY"

"""
    asin_granularity options:
        -> CHILD
        -> PARENT
"""
asin_granularity = "CHILD"

marketplace_id = Marketplaces.US.marketplace_id

# set the report_id to None if you want to create a new report
# if you want to download created report, then set the report_id to the id of the report
report_id = ''

# </input part> ==========================================================================================================

report_type = ReportType.GET_SALES_AND_TRAFFIC_REPORT.value

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
                             marketplace=Marketplaces.US)

if report_id == None:
    try:
        response = reports_api_client.create_report(
            reportType=report_type,
            dataStartTime=data_start_time,
            dataEndTime=data_end_time,
            reportOptions={
                "dateGranularity": date_granularity,
                "asinGranularity": asin_granularity
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
    report_file_path = f'./reports-downloaded/start-{data_start_time}-end-{data_end_time}-id-{report_id}-asin_gran-{asin_granularity}-date_gran-{date_granularity}.json'

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

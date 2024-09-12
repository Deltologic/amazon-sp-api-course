import ijson
from datetime import date
from dotenv import load_dotenv
import os
from sp_api.api import Reports
from sp_api.base import Marketplaces

from common.report_types import ReportType
from common.processing_statuses import ProcessingStatus
from ReportsAPI.reports_common.report_model import GetReportByIdModel


# <input part> ==========================================================================================================
"""
    selling_program options:
        -> RETAIL
        -> FRESH
"""

selling_program = "RETAIL"

# in this example, we are using the DE marketplace
marketplace_id = "A1PA6795UKMFR9"

# set the report_id to None if you want to create a new report
# if you want to download created report, then set the report_id to the id of the report
report_id = None

# </input part> ==========================================================================================================

report_type = ReportType.GET_VENDOR_FORECASTING_REPORT.value
report_request_time=date.today().strftime('%Y-%m-%d')

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
            reportOptions={
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
    report_file_path = f'./reports-downloaded/report-request-time-{report_request_time}-id-{report_id}.json'

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
    
    def stream_json_array(file_path, array_key):
        with open(file_path, 'rb') as file:
            items = ijson.items(file, f'{array_key}.item')
            for item in items:
                yield item

    data_by_department_and_search_term_key = 'forecastByAsin'
    count = 0
    for element in stream_json_array(report_file_path, data_by_department_and_search_term_key):
        count += 1
    print(count)

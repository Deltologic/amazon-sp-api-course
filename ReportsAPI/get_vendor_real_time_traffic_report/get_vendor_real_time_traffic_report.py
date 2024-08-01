from dotenv import load_dotenv
import time
import os
from sp_api.api import Reports
from sp_api.base import Marketplaces

from common.report_types import ReportType
from common.processing_statuses import ProcessingStatus
from reports_common.report_model import GetReportByIdModel
from reports_common.prepare_dates import parse_time_period, prepare_dates
from analyze_reports import get_list_of_time_periods_with_most_glanced_asins, get_list_of_hours_with_most_glanced_asins


# <input part> ==========================================================================================================
date_periods = prepare_dates(report_period=14)

# in this example, we are using the DE marketplace
marketplace_id = "A1PA6795UKMFR9"

# set the report_ids to empty if you want to create new reports
# if you want to download created reports, then fill the array with the report ids
report_ids = []

# </input part> ==========================================================================================================

report_type = ReportType.GET_VENDOR_REAL_TIME_TRAFFIC_REPORT.value

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
                             marketplace=Marketplaces.DE)

if len(report_ids) == 0:
    try:
        for date in date_periods:
            response = reports_api_client.create_report(
                reportType=report_type,
                dataStartTime=date.start_time,
                dataEndTime=date.end_time,
                marketplaceIds=[
                    marketplace_id
                ],
            )

            report_id = response.payload['reportId']
            print('report id:', report_id)
    except Exception as e:
        print("An error occurred while creating the report")
        print(e)

else:
    # the request below should be taken after a while (5-10 minutes) to be sure that the reports are ready
    downloaded_reports_paths = []
    for report_id in report_ids:
        try:
            response = reports_api_client.get_report(reportId=report_id)
            report_by_id_response = GetReportByIdModel(response.payload)

            if report_by_id_response.processing_status == ProcessingStatus.DONE.value and report_by_id_response.report_document_id != None:
                report_file_path = f'./reports-downloaded/start-{report_by_id_response.data_start_time}-end-{report_by_id_response.data_end_time}-id-{
                    report_id}.json'

                os.makedirs(os.path.dirname(report_file_path), exist_ok=True)

                with open(report_file_path, 'w') as file:
                    report_url_response = reports_api_client.get_report_document(
                        reportDocumentId=report_by_id_response.report_document_id, download=True, file=file)
                    print(f"Report downloaded successfully at {report_file_path}")
                    downloaded_reports_paths.append(report_file_path)
                    time.sleep(3)
            elif report_by_id_response.processing_status == ProcessingStatus.IN_PROGRESS.value or report_by_id_response.processing_status == ProcessingStatus.IN_QUEUE.value:
                print("The report is not ready yet")
            else:
                print("An error occurred while getting the report")
                print(report_by_id_response.processing_status)
        except Exception as e:
            print("An error occurred while getting the report")
            print(e)

    # processing the report (can be huge)

    data_by_department_and_search_term_key = 'reportData'
    count = 0
    arrays_to_compare = []
    if len(downloaded_reports_paths) == 2:
        for report_path in downloaded_reports_paths:
            list_of_time_periods = get_list_of_time_periods_with_most_glanced_asins(
                report_path, data_by_department_and_search_term_key)
            arrays_to_compare.append(list_of_time_periods)

        list_of_hours_with_most_glanced_asins = get_list_of_hours_with_most_glanced_asins(
            arrays_to_compare)

        sorted_time_periods = sorted(
            list_of_hours_with_most_glanced_asins, key=lambda x: parse_time_period(x.time_period)[0])
        print('List of hours with most glanced asins:')
        for period in sorted_time_periods:
            print(f'Time period: {period.time_period}, Asin: {period.asin}, Glance views: {period.glance_views}')

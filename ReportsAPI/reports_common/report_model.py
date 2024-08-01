from typing import Optional
from common.report_types import ReportType
from common.processing_statuses import ProcessingStatus

class GetReportByIdModel():
    report_id: str
    report_type: ReportType
    processing_status: ProcessingStatus
    marketplace_ids: list[str]
    processing_start_time: str
    processing_end_time: Optional[str] = None
    data_start_time: str
    data_end_time: str
    created_time: str
    report_document_id: Optional[str] = None
    
    def __init__(self, payload: dict):
        self.report_id = payload.get('reportId')
        self.report_type = payload.get('reportType')
        self.processing_status = payload.get('processingStatus')
        self.marketplace_ids = payload.get('marketplaceIds')
        self.processing_start_time = payload.get('processingStartTime')
        self.processing_end_time = payload.get('processingEndTime')
        self.data_start_time = payload.get('dataStartTime')
        self.data_end_time = payload.get('dataEndTime')
        self.created_time = payload.get('createdTime')
        self.report_document_id = payload.get('reportDocumentId')
    
import math
from datetime import datetime, timedelta
from typing import List


class DatePeriod:
    start_time: str
    end_time: str

    def __init__(self, start_time: datetime, delta: int):
        self.start_time = self._format_date(start_time)
        self.end_time = self._format_date(start_time+timedelta(days=delta))

    def _format_date(self, date: datetime) -> str:
        date_at_midnight = date.replace(
            hour=0, minute=0, second=0, microsecond=0)
        return date_at_midnight.strftime('%Y-%m-%dT%H:%M:%SZ')


def prepare_dates(report_period) -> List[DatePeriod]:
    number_of_reports=math.ceil(28/report_period)
    date_periods=[]
    first_period_start_time = datetime.today() - timedelta(days=29)
    date_periods.append(DatePeriod(first_period_start_time, report_period-1))
    period_to_compare_to = first_period_start_time
    for i in range(0, number_of_reports-1):
        period_start_time = period_to_compare_to + timedelta(days=report_period)
        date_periods.append(DatePeriod(period_start_time, report_period-1))
        period_to_compare_to = period_start_time

    return date_periods

def parse_time_period(time_period):
    start_str, end_str = time_period.split('-')
    start_time = datetime.strptime(start_str, "%H:%M:%SZ")
    end_time = datetime.strptime(end_str, "%H:%M:%SZ")
    return (start_time, end_time)

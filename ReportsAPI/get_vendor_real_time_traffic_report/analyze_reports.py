from datetime import datetime
import json
import ijson
from typing import List


class TimePeriodWithAsin:
    def __init__(self, asin: str, glance_views: int, start_time: str, end_time: str):
        self.asin = asin
        self.glance_views = glance_views
        self.time_period = f"{start_time.split('T')[1]}-{end_time.split('T')[1]}"

    def time_period_is_equal(self, start_time: str, end_time: str):
        other_time_period = f"{start_time.split('T')[1]}-{end_time.split('T')[1]}"
        return self.time_period == other_time_period


def get_list_of_time_periods_with_most_glanced_asins(file_path, array_key):
    time_periods_with_most_glanced_asins: List[TimePeriodWithAsin] = []

    with open(file_path, 'rb') as file:
        items = ijson.items(file, f'{array_key}.item')
        for item in items:
            the_same_time_period = [
                time_per for time_per in time_periods_with_most_glanced_asins if time_per.time_period_is_equal(item['startTime'], item['endTime'])]
            if len(the_same_time_period) == 0:
                time_periods_with_most_glanced_asins.append(TimePeriodWithAsin(
                    asin=item['asin'], glance_views=item['glanceViews'], start_time=item['startTime'], end_time=item['endTime']))
                continue

            if item['glanceViews'] > the_same_time_period[0].glance_views:
                the_same_time_period[0].glance_views = item['glanceViews']
                the_same_time_period[0].asin = item['asin']

    return time_periods_with_most_glanced_asins


def get_list_of_hours_with_most_glanced_asins(arrays: List[List[TimePeriodWithAsin]]) -> List[TimePeriodWithAsin]:
    merged_dict: dict[str, TimePeriodWithAsin] = {}

    for array in arrays:
        for obj in array:
            time_period = obj.time_period
            glances = obj.glance_views
            if time_period not in merged_dict or glances > merged_dict[time_period].glance_views:
                merged_dict[time_period] = obj

    merged_array = list(merged_dict.values())
    return merged_array

from datetime import datetime
import json
import ijson
from typing import List


class TimePeriodWithQuantityAndRevenue:
    def __init__(self, ordered_units: int, ordered_revenue: float, start_time: str, end_time: str):
        self.ordered_products_units = ordered_units
        self.ordered_revenue = ordered_revenue
        
        self.time_period = f'{start_time.split(
            'T')[1]}-{end_time.split('T')[1]}'

    def set_avg_sales(self):
        if(self.ordered_products_units == 0):
            self.average_sales = 0
        else:
            self.average_sales = self.ordered_revenue / self.ordered_products_units
    
    def time_period_is_equal(self, start_time: str, end_time: str):
        other_time_period = f'{start_time.split(
            'T')[1]}-{end_time.split('T')[1]}'
        return self.time_period == other_time_period


def get_time_periods_with_quantities_and_revenues(file_path, array_key):
    time_periods_with_quantities: List[TimePeriodWithQuantityAndRevenue] = []

    with open(file_path, 'rb') as file:
        items = ijson.items(file, f'{array_key}.item')
        for item in items:
            the_same_time_period = [
                time_per for time_per in time_periods_with_quantities if time_per.time_period_is_equal(item['startTime'], item['endTime'])]
            if len(the_same_time_period) == 0:
                time_periods_with_quantities.append(TimePeriodWithQuantityAndRevenue(ordered_units=item['orderedUnits'], ordered_revenue=item['orderedRevenue'], start_time=item['startTime'], end_time=item['endTime']))
                continue
            
            the_same_time_period[0].ordered_products_units += item['orderedUnits']
            the_same_time_period[0].ordered_revenue += item['orderedRevenue']

    return time_periods_with_quantities


def merge_same_time_periods_data(arrays: List[List[TimePeriodWithQuantityAndRevenue]]) -> List[TimePeriodWithQuantityAndRevenue]:
    merged_dict: dict[str, TimePeriodWithQuantityAndRevenue] = {}

    for array in arrays:
        for obj in array:
            time_period = obj.time_period
            glances = obj.ordered_products_units
            if time_period not in merged_dict:
                merged_dict[time_period] = obj
            else:
                merged_dict[time_period].ordered_products_units += obj.ordered_products_units
                merged_dict[time_period].ordered_revenue += obj.ordered_revenue

    merged_array = list(merged_dict.values())
    return merged_array

import json
import ijson
from typing import List


class AsinWithAvailability:
    def __init__(self, asin: str, availability: int, start_time: str, end_time: str):
        self.asin = asin
        self.availability = availability
        self.start_time = start_time
        self.end_time = end_time


def get_list_of_lowest_availabilites(file_path, array_key):
    asins_with_availability: List[AsinWithAvailability] = []

    with open(file_path, 'rb') as file:
        items = ijson.items(file, f'{array_key}.item')
        for item in items:
            asin_with_availability = [
                asin_with_avail for asin_with_avail in asins_with_availability if asin_with_avail.asin == item['asin']]
            if len(asin_with_availability) == 0:
                asins_with_availability.append(AsinWithAvailability(
                    asin=item['asin'], availability=item['highlyAvailableInventory'], start_time=item['startTime'], end_time=item['endTime']))
                continue

            if item['highlyAvailableInventory'] < asin_with_availability[0].availability:
                asin_with_availability[0].availability = item['highlyAvailableInventory']
                asin_with_availability[0].start_time = item['startTime']
                asin_with_availability[0].end_time = item['endTime']

    return asins_with_availability


def get_list_of_lowest_availabilities_from_arrays(arrays: List[List[AsinWithAvailability]]) -> List[AsinWithAvailability]:
    merged_dict: dict[str, AsinWithAvailability] = {}

    for array in arrays:
        for obj in array:
            asin = obj.asin
            stock = obj.availability
            if asin not in merged_dict or stock < merged_dict[asin].availability:
                merged_dict[asin] = obj

    merged_array = list(merged_dict.values())
    return merged_array


def get_most_frequent_time_period_when_stock_is_low(lowest_stock_asins: List[AsinWithAvailability]):
    time_periods = {}
    for asin in lowest_stock_asins:
        time_period = f"{asin.start_time.split('T')[1]}-{asin.end_time.split('T')[1]}"
        if time_period in time_periods:
            time_periods[time_period] += 1
        else:
            time_periods[time_period] = 1

    with open('time_periods.json', 'w') as file:
        json.dump(time_periods, file, indent=4)

    min_availabilty_time_period = max(time_periods, key=time_periods.get)
    return min_availabilty_time_period

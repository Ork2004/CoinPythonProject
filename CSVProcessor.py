import os
import csv
import numpy as np
import re
import time


def mergesort(list1):
    if len(list1) > 1:
        mid = len(list1) // 2
        left_list = list1[:mid]
        right_list = list1[mid:]

        mergesort(left_list)
        mergesort(right_list)

        i = 0
        j = 0
        k = 0

        while i < len(left_list) and j < len(right_list):
            if left_list[i][2] > right_list[j][2]:
                list1[k] = left_list[i]
                i += 1
            else:
                list1[k] = right_list[j]
                j += 1
            k += 1

        while i < len(left_list):
            list1[k] = left_list[i]
            i += 1
            k += 1

        while j < len(right_list):
            list1[k] = right_list[j]
            j += 1
            k += 1

class CSVProcessor:
    def __init__(self, csv_folder="csv"):
        self.csv_folder = csv_folder
        self.files_data = {}

    def process_csv_files(self):
        for csv_filename in os.listdir(self.csv_folder):
            if csv_filename.endswith(".csv"):
                csv_filepath = os.path.join(self.csv_folder, csv_filename)
                self.process_csv_file(csv_filename, csv_filepath)

    def process_csv_file(self, csv_filename, csv_filepath):
        with open(csv_filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]

            dates = [self.extract_date_or_time(row['Date'], 'date') for row in rows]
            times = [self.extract_date_or_time(row['Date'], 'time') for row in rows]
            highs = np.array([float(row['High']) for row in rows])
            lows = np.array([float(row['Low']) for row in rows])
            opens = np.array([float(row['Open']) for row in rows])
            closes = np.array([float(row['Close']) for row in rows])
            volumes = np.array([float(row['Volume']) for row in rows])

            self.files_data[csv_filename] = {
                'dates': dates, 'times': times, 'highs': highs, 'lows': lows, 'opens': opens,
                'closes': closes, 'volumes': volumes
            }

    def extract_date_or_time(self, date_str, extract="both"):
        match = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})", date_str)
        if match:
            date = match.group(1)
            time = match.group(2)
            if extract == "date":
                return date
            elif extract == "time":
                return time
            elif extract == "both":
                return date, time
        return None if extract == "time" else date_str if extract == "date" else (date_str, None)

    def get_top_10_high_low(self):
        top_10_high = {}
        top_10_low = {}

        timings = {}

        for filename, data in self.files_data.items():
            start_time = time.time()
            high_pairs = [
                (data['dates'][i], data['times'][i], data['highs'][i])
                for i in range(len(data['dates']))
            ]
            mergesort(high_pairs)
            top_10_high[filename] = high_pairs[:10]

            low_pairs = [
                (data['dates'][i], data['times'][i], data['lows'][i])
                for i in range(len(data['dates']))
            ]
            mergesort(low_pairs)
            low_pairs.reverse()
            top_10_low[filename] = low_pairs[-10:]

            end_time = time.time()
            timings[filename] = end_time - start_time

        return top_10_high, top_10_low, timings

    def get_statistics(self):
        stats = {}
        for filename, data in self.files_data.items():
            stats[filename] = {
                'avg_high': np.mean(data['highs']),
                'std_high': np.std(data['highs']),
                'avg_low': np.mean(data['lows']),
                'std_low': np.std(data['lows']),
                'avg_open': np.mean(data['opens']),
                'std_open': np.std(data['opens']),
                'avg_close': np.mean(data['closes']),
                'std_close': np.std(data['closes']),
            }
        return stats

    def calculate_moving_average(self, data, window_size=5):
        moving_averages = []
        for i in range(len(data)):
            if i < window_size - 1:
                moving_averages.append(None)
            else:
                moving_averages.append(np.mean(data[i - window_size + 1:i + 1]))
        return moving_averages

    def analyze_trends_and_seasonality(self):
        trends_seasonality = {}

        for filename, data in self.files_data.items():
            closes = data['closes']
            moving_avg = self.calculate_moving_average(closes, window_size=7)

            seasonality = [closes[i] - moving_avg[i] if moving_avg[i] is not None else None for i in range(len(closes))]

            trends_seasonality[filename] = {
                'trend': moving_avg,
                'seasonality': seasonality
            }

        return trends_seasonality
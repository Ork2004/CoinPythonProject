import os
import csv
import numpy as np
import re


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

            dates = [self.extract_date(row['Date']) for row in rows]
            times = [self.extract_time(row['Date']) for row in rows]
            highs = np.array([float(row['High']) for row in rows])
            lows = np.array([float(row['Low']) for row in rows])
            opens = np.array([float(row['Open']) for row in rows])
            closes = np.array([float(row['Close']) for row in rows])
            volumes = np.array([float(row['Volume']) for row in rows])

            self.files_data[csv_filename] = {
                'dates': dates, 'times': times, 'highs': highs, 'lows': lows, 'opens': opens,
                'closes': closes, 'volumes': volumes
            }

    def extract_date(self, date_str):
        match = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})", date_str)
        if match:
            return match.group(1)
        return date_str

    def extract_time(self, date_str):
        match = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})", date_str)
        if match:
            return match.group(2)
        return None

    def get_top_10_high_low(self):
        top_10_high = {}
        top_10_low = {}

        for filename, data in self.files_data.items():
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

        return top_10_high, top_10_low

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
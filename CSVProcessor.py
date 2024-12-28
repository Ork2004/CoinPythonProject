import os
import csv
import numpy as np

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

            dates = [row['Date'] for row in rows]
            highs = np.array([float(row['High']) for row in rows])
            lows = np.array([float(row['Low']) for row in rows])
            opens = np.array([float(row['Open']) for row in rows])
            closes = np.array([float(row['Close']) for row in rows])
            volumes = np.array([float(row['Volume']) for row in rows])

            self.files_data[csv_filename] = {
                'dates': dates, 'highs': highs, 'lows': lows, 'opens': opens,
                'closes': closes, 'volumes': volumes
            }

    def get_top_10_high_low(self):
        top_10_high = {}
        top_10_low = {}
        for filename, data in self.files_data.items():
            high_pairs = []
            for i in range(len(data['dates'])):
                high_pairs.append((data['dates'][i], data['highs'][i]))
            high_pairs.sort(key=lambda x: x[1], reverse=True)
            top_10_high[filename] = high_pairs[:10]

            low_pairs = []
            for i in range(len(data['dates'])):
                low_pairs.append((data['dates'][i], data['lows'][i]))
            low_pairs.sort(key=lambda x: x[1])
            top_10_low[filename] = low_pairs[:10]

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
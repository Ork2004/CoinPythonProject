import csv
from datetime import datetime
import numpy as np
import os
import webbrowser

csv_folder = "csv"  
html_folder = "html" 
if not os.path.exists(html_folder):
    os.makedirs(html_folder)

def process_csv_file(file_path):
    data = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            headers = next(reader)  
            for row in reader:
                try:
                    date = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
                    data.append({
                        "date": date.date(),
                        "open": float(row[4]),
                        "high": float(row[5]),
                        "low": float(row[6]),
                        "close": float(row[7]),
                        "volume": float(row[8]) if row[8] else 0.0
                    })
                except (ValueError, IndexError):
                    print(f"Error processing row: {row}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return data

def analyze_data(data):
    if not data:
        print("No data to analyze.")
        return None, None, None, {}, {}

    close_prices = [entry["close"] for entry in data if "close" in entry and entry["close"] is not None]

    if not close_prices:
        print("No closing price data.")
        return None, None, None, {}, {}

    close_prices_np = np.array(close_prices)

    average_price = np.mean(close_prices_np)
    max_price = np.max(close_prices_np)
    min_price = np.min(close_prices_np)

    monthly_avg = {}
    yearly_avg = {}
    
    for entry in data:
        if entry.get("close") is None:
            continue
        
        month = entry["date"].strftime("%Y-%m")
        if month not in monthly_avg:
            monthly_avg[month] = []
        monthly_avg[month].append(entry["close"])
        
        year = entry["date"].strftime("%Y")
        if year not in yearly_avg:
            yearly_avg[year] = []
        yearly_avg[year].append(entry["close"])

    monthly_avg_np = {month: np.mean(np.array(prices)) for month, prices in monthly_avg.items()}
    yearly_avg_np = {year: np.mean(np.array(prices)) for year, prices in yearly_avg.items()}
    return average_price, max_price, min_price, monthly_avg_np, yearly_avg_np

main_html_content = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Data Analysis</title>
</head>
<body>
    <h1>List of Files with Analysis</h1>
    <ul>
"""

for csv_filename in os.listdir(csv_folder):
    if csv_filename.endswith(".csv"):
        csv_filepath = os.path.join(csv_folder, csv_filename)
        filename = csv_filename.replace(".csv", "")

        print(f"Processing file: {csv_filename}")
        data = process_csv_file(csv_filepath)
        if not data:
            print(f"Skipping {filename}: No data.")
            continue

        average_price, max_price, min_price, monthly_avg, yearly_avg = analyze_data(data)

        if average_price is None:
            print(f"Skipping {filename}: Insufficient data for analysis.")
            continue

        monthly_avg_html = "".join([f"<li>{month}: {avg:.4f}</li>" for month, avg in monthly_avg.items()])
        yearly_avg_html = "".join([f"<li>{year}: {avg:.4f}</li>" for year, avg in yearly_avg.items()])

        html_content = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{filename} Data Analysis</title>
</head>
<body>
    <h1>Data Analysis: {filename}</h1>
    <p><strong>Average Price:</strong> {average_price:.4f}</p>
    <p><strong>Maximum Price:</strong> {max_price:.4f}</p>
    <p><strong>Minimum Price:</strong> {min_price:.4f}</p>
    <h2>Average Prices by Month:</h2>
    <ul>
        {monthly_avg_html}
    </ul>
    <h2>Average Prices by Year:</h2>
    <ul>
        {yearly_avg_html}
    </ul>
</body>
</html>
        """
        html_filename = filename + ".html"
        html_filepath = os.path.join(html_folder, html_filename)
        with open(html_filepath, "w", encoding="utf-8") as file:
            file.write(html_content)

        main_html_content += f'<li><a href="{html_filename}">{filename}</a></li>\n'

main_html_content += """
    </ul>
</body>
</html>
"""

main_html_filepath = os.path.join(html_folder, "index.html")
with open(main_html_filepath, "w", encoding="utf-8") as main_html_file:
    main_html_file.write(main_html_content)

print("Done! Main page created.")
webbrowser.open_new_tab(main_html_filepath)

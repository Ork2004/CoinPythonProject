import os
import webbrowser
import csv
import numpy as np

csv_folder = "csv"
html_folder = "html"

main_html_filepath = os.path.join(html_folder, "index.html")
links = []

for csv_filename in os.listdir(csv_folder):
    if csv_filename.endswith(".csv"):
        csv_filepath = os.path.join(csv_folder, csv_filename)
        filename = csv_filename.replace(".csv", "")

        with open(csv_filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]

            dates = [row['Date'] for row in rows]
            highs = np.array([float(row['High']) for row in rows])
            lows = np.array([float(row['Low']) for row in rows])
            opens = np.array([float(row['Open']) for row in rows])
            closes = np.array([float(row['Close']) for row in rows])
            volumes = np.array([float(row['Volume']) for row in rows])

            # Top 10 Highest/Lowest Valuses
            top_10_high = sorted(zip(dates, highs), key=lambda x: x[1], reverse=True)[:10]
            top_10_low = sorted(zip(dates, lows), key=lambda x: x[1])[:10]

            #Average and Standard Deviation
            avg_high = np.mean(highs)
            std_high = np.std(highs)

            avg_low = np.mean(lows)
            std_low = np.std(lows)

            avg_open = np.mean(opens)
            std_open = np.std(opens)

            avg_close = np.mean(closes)
            std_close = np.std(closes)

        html_content = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{filename}</title>
</head>
<body>
    <h1>{filename}</h1>
    <h2>Top 10 Highest Highs</h2>
    <ul>
        {''.join([f"<li>Date: {high[0]}, Value: {high[1]}</li>" for high in top_10_high])}
    </ul>
    <h2>Top 10 Lowest Lows</h2>
    <ul>
        {''.join([f"<li>Date: {low[0]}, Value: {low[1]}</li>" for low in top_10_low])}
    </ul>
    
    <h2>Statistical Summary</h2>
    <ul>
        <li>Average High: {avg_high:.2f}</li>
        <li>Standard Deviation of Highs: {std_high:.2f}</li>
        <li>Average Low: {avg_low:.2f}</li>
        <li>Standard Deviation of Lows: {std_low:.2f}</li>
        <li>Average Open: {avg_open:.2f}</li>
        <li>Standard Deviation of Opens: {std_open:.2f}</li>
        <li>Average Close: {avg_close:.2f}</li>
        <li>Standard Deviation of Closes: {std_close:.2f}</li>
    </ul>
</body>
</html>
        """

        html_filename = filename + ".html"
        html_filepath = os.path.join(html_folder, html_filename)
        try:
            with open(html_filepath, "w", encoding="utf-8") as file:
                file.write(html_content)
            print(filename + " HTML File Created")
            links.append(f'<li><a href="{html_filename}">{filename}</a></li>')
        except: print("HTML File Creation Failed")

#Index
main_html_content = """<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Index</title>
</head>
<body>
    <h1>List of CSV files</h1>
    <ul>
"""
main_html_content += "\n".join(links)
main_html_content += """
    </ul>
</body>
</html>
"""

try:
    with open(main_html_filepath, "w", encoding="utf-8") as main_html_file:
        main_html_file.write(main_html_content)
    print("Main HTML File Created")
    webbrowser.open(main_html_filepath)
except:
    print("Main HTML File Creation Failed")
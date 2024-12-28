import os
import webbrowser
import csv

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

            high_values = [(row['Date'], float(row['High'])) for row in rows]
            low_values = [(row['Date'], float(row['Low'])) for row in rows]

            top_10_high = sorted(high_values, key=lambda x: x[1], reverse=True)[:10]
            top_10_low = sorted(low_values, key=lambda x: x[1])[:10]

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
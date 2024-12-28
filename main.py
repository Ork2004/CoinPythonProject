import os
import webbrowser

from CSVProcessor import CSVProcessor

csv_folder = "csv"
html_folder = "html"

main_html_filepath = os.path.join(html_folder, "index.html")
links = []

csv_processor = CSVProcessor(csv_folder)
csv_processor.process_csv_files()

top_10_high, top_10_low = csv_processor.get_top_10_high_low()
stats = csv_processor.get_statistics()

for csv_filename, data in csv_processor.files_data.items():
    filename = csv_filename.replace(".csv", "")

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
            {''.join([f"<li>Date: {high[0]}, Time: {high[1]}, Value: {high[2]}</li>" for high in top_10_high[csv_filename]])}
        </ul>
        <h2>Top 10 Lowest Lows</h2>
        <ul>
            {''.join([f"<li>Date: {low[0]}, Time: {low[1]}, Value: {low[2]}</li>" for low in top_10_low[csv_filename]])}
        </ul>

        <h2>Statistical Summary</h2>
        <ul>
            <li>Average High: {stats[csv_filename]['avg_high']:.2f}</li>
            <li>Standard Deviation of Highs: {stats[csv_filename]['std_high']:.2f}</li>
            <li>Average Low: {stats[csv_filename]['avg_low']:.2f}</li>
            <li>Standard Deviation of Lows: {stats[csv_filename]['std_low']:.2f}</li>
            <li>Average Open: {stats[csv_filename]['avg_open']:.2f}</li>
            <li>Standard Deviation of Opens: {stats[csv_filename]['std_open']:.2f}</li>
            <li>Average Close: {stats[csv_filename]['avg_close']:.2f}</li>
            <li>Standard Deviation of Closes: {stats[csv_filename]['std_close']:.2f}</li>
        </ul>
    </body>
    </html>
    """

    html_filename = filename + ".html"
    html_filepath = os.path.join(html_folder, html_filename)
    try:
        with open(html_filepath, "w", encoding="utf-8") as file:
            file.write(html_content)
        links.append(f'<li><a href="{html_filename}">{filename}</a></li>')
    except:
        print("HTML File Creation Failed")

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

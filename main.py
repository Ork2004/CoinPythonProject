import os
import webbrowser
import matplotlib.pyplot as plt

from CSVProcessor import CSVProcessor

csv_folder = "csv"
html_folder = "html"

main_html_filepath = os.path.join(html_folder, "index.html")
links = []

csv_processor = CSVProcessor(csv_folder)
csv_processor.process_csv_files()

top_10_high, top_10_low, timings = csv_processor.get_top_10_high_low()
stats = csv_processor.get_statistics()
trends_seasonality = csv_processor.analyze_trends_and_seasonality()
volume_to_marketcap_ratios = csv_processor.calculate_volume_to_marketcap_ratio()

for filename, timing in timings.items():
    print(f"{filename}: {timing:.4f} seconds")
fastest_file = min(timings, key=timings.get)
slowest_file = max(timings, key=timings.get)

print(f"Fastest file: {fastest_file}: {timings[fastest_file]:.4f} seconds")
print(f"Slowest file: {slowest_file}: {timings[slowest_file]:.4f} seconds")


def save_graph(data, trend, seasonality, filename, label, output_folder="graphs"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(data)), data, label=f"{label} Price", alpha=0.5)
    if trend:
        plt.plot(range(len(trend)), trend, label=f"{label} Trend", color="red")
    if seasonality:
        plt.plot(range(len(seasonality)), seasonality, label=f"{label} Seasonality", color="green")
    plt.title(f"{label} Trend and Seasonality Analysis for {filename}")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.legend()
    graph_filename = os.path.join(output_folder, f"{filename}_{label.lower()}_trend_seasonality.png")
    plt.savefig(graph_filename)
    plt.close()
    return graph_filename


def save_volume_to_marketcap_graph(ratios, filename, output_folder="graphs"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(ratios)), ratios, label="Volume-to-Marketcap Ratio", color="blue", alpha=0.7)
    plt.title(f"Volume-to-Marketcap Ratio for {filename}")
    plt.xlabel("Index")
    plt.ylabel("V/M Ratio")
    plt.legend()

    graph_filename = os.path.join(output_folder, f"{filename}_volume_to_marketcap.png")
    plt.savefig(graph_filename)
    plt.close()

    return graph_filename

for csv_filename, data in csv_processor.files_data.items():
    filename = csv_filename.replace(".csv", "")

    trend_close = trends_seasonality[csv_filename]['trend_close']
    seasonality_close = trends_seasonality[csv_filename]['seasonality_close']

    trend_open = trends_seasonality[csv_filename]['trend_open']
    seasonality_open = trends_seasonality[csv_filename]['seasonality_open']

    graph_filepath_close = save_graph(data['closes'], trend_close, seasonality_close, filename, "Close")
    graph_filepath_open = save_graph(data['opens'], trend_open, seasonality_open, filename, "Open")

    graph_relative_path_close = os.path.relpath(graph_filepath_close, html_folder)
    graph_relative_path_open = os.path.relpath(graph_filepath_open, html_folder)

    ratios = volume_to_marketcap_ratios[csv_filename]

    graph_path_ratios = save_volume_to_marketcap_graph(ratios, filename)
    graph_relative_path_ratios = os.path.relpath(graph_path_ratios, html_folder)

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
        
        <h2>Trend and Seasonality Graphs</h2>
        <h3>Close Price</h3>
        <img src="{graph_relative_path_close}" alt="Close Price Trend and Seasonality Graph">
        <h3>Open Price</h3>
        <img src="{graph_relative_path_open}" alt="Open Price Trend and Seasonality Graph">
        <h2>Volume-to-Marketcap Ratio Graph</h2>
        <img src="{graph_relative_path_ratios}" alt="Volume-to-Marketcap Ratio Graph">
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

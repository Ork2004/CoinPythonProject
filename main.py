import os
import webbrowser

csv_folder = "csv"
html_folder = "html"

main_html_filepath = os.path.join(html_folder, "index.html")
links = []

for csv_filename in os.listdir(csv_folder):
    if csv_filename.endswith(".csv"):
        csv_filepath = os.path.join(csv_folder, csv_filename)

        filename = csv_filename.replace(".csv", "")

        html_content = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{filename}</title>
</head>
<body>
    <h1>{filename}</h1>
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
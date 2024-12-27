import os
import webbrowser

archive_path = "archive"
html_folder = "html"

for csv_filename in os.listdir(archive_path):
    if csv_filename.endswith(".csv"):
        file_path = os.path.join(archive_path, csv_filename)

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
            with open(html_filename, "w", encoding="utf-8") as file:
                file.write(html_content)
            print(filename + " HTML File Created")
        except: print("HTML File Creation Failed")
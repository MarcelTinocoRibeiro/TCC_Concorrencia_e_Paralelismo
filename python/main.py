from downloader import Download

url = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
# useConcurrency = false
file_path = ''
total_partitions = 28 # care about website server limit


d = Download(url, file_path, total_partitions)
d.do()
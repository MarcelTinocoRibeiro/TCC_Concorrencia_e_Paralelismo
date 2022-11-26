from downloader import Download
import word_finder

##### Download #####
url = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
# use_concurrency = false
file_path = ''
total_partitions = 30 # care about website server limit


# d = Download(url, file_path, total_partitions)
# d.do()
##### Download #####
##### Word Finder #####
file_path = '..\\temp_files\\exemplo_menor.txt'
finder = word_finder.WordFinder('junior')
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
finder.word_finder(lines)
for line in finder.matchs:
    print(line)
print(len(line))

##### Word Finder #####




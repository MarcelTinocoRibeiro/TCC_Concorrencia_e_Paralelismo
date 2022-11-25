from downloader import Download
import word_finder

##### Download #####
url = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
# use_concurrency = false
file_path = ''
total_partitions = 28 # care about website server limit


# d = Download(url, file_path, total_partitions)
# d.do()
##### Download #####
##### Word Finder #####
lines = []
with open('../temp_files/exemplo.txt') as f:
    line = f.readline()
    while line != '':
        value = word_finder.find_word(word='junior', line=line)
        if value != '':
            lines.append(value)
            
    

##### Word Finder #####




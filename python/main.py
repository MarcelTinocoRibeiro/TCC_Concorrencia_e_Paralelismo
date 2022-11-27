from downloader import Download
import word_finder
import time
import datetime
start =  datetime.datetime.now().time()
##### Download #####
# url = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
# file_path = '../temp_files/python/text_sample.csv'
# url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_10mb.mp4'
url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_30mb.mp4'
file_path = '../temp_files/python/video_sample.mp4'
total_partitions = 10 # care about website server limit

with open(f'../temp_files/python/results.csv', '+w', encoding='utf-8') as f:
    d = Download(url, file_path, total_partitions, f)
    # d.do()
    d.do_sequencial()
    # d.do_sequencial_divided()
    # d.do_threading_divided()
##### Download #####
##### Word Finder #####
# file_path = '..\\temp_files\\exemplo_maior.txt'
# finder = word_finder.WordFinder('junior')
# with open(file_path, 'r', encoding='utf-8') as f:
#     lines = f.readlines()
# # finder.word_finder_without_threads(lines)
# finder.word_finder_with_threads(lines)
# # finder.pool('junior', lines[1])
# for line in finder.matches:
#     if line: print(line.strip())
# print(len(finder.matches))
print('start', start)
print('finish', datetime.datetime.now().time())

##### Word Finder #####




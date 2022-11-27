from downloader import Download
import word_finder
import time
import datetime
##### Download #####
# for i in range(7):
#     total_partitions = 2**i
#     with open(f'../temp_files/python/results_sequencial_divided_{total_partitions}_video.csv', '+w', encoding='utf-8') as f:
#         f.write(f'total_runs,run,mode,partitions,partition_size,total_file_size,start_time,finish_time,time_elapsed\n')
#         # url = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
#         # file_path = '../temp_files/python/text_sample.csv'
#         # url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_10mb.mp4'
#         url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_30mb.mp4'
#         file_path = '../temp_files/python/video_sample.mp4'
#         # total_partitions = 64 # care about website server limit
#         runs = 10
#         d = Download(url, file_path, total_partitions, f)
    
        
#         # d.do_sequencial(runs)
#         d.do_sequencial_divided(runs)
#         # d.do_threading_divided(runs)

##### Download #####
##### Word Finder #####
file_path = '..\\temp_files\\exemplo.txt'
finder = word_finder.WordFinder('junior')
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
# finder.word_finder_without_threads(lines)
finder.word_finder_with_threads(lines)
# finder.pool('junior', lines[1])
for line in finder.matches:
    if line: print(line.strip())
print(len(finder.matches))

##### Word Finder #####




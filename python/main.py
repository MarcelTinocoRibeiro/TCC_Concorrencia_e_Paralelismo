from downloader import Download
import word_finder
import time
import datetime
##### Download #####
for i in range(7):
    total_partitions = 2**i
    with open(f'../temp_files/python/results_threading_text_{total_partitions}.csv', '+w', encoding='utf-8') as f:
    # with open(f'../temp_files/python/results_threading_text.csv', '+w', encoding='utf-8') as f:
        # total_partitions = 1
        f.write(f'total_runs,run,mode,partitions,partition_size,total_file_size,start_time,finish_time,time_elapsed\n')
        url = "https://www.sample-videos.com/csv/Sample-Spreadsheet-500000-rows.csv"
        file_path = '../temp_files/python/text_sample.csv'
        # url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_10mb.mp4'
        # url = 'https://www.sample-videos.com/video123/mp4/720/big_buck_bunny_720p_30mb.mp4'
        # file_path = '../temp_files/python/video_sample.mp4'
        # total_partitions = 64 # care about website server limit
        runs = 10
        d = Download(url, file_path, total_partitions, f)

        
        # d.do_sequencial(runs)
            # d.do_sequencial_divided(runs)
        d.do_threading_divided(runs)


##### Download #####
##### Word Finder #####
# total_runs = 10
# # for run in range(total_runs):
#     # threads_used = 1
# with open(f'../temp_files/python/results_word_finder_with_threads.csv', '+a', encoding='utf-8') as f:
#     f.write(f'total_runs,run,mode,total_file_lines,word_matches,start_time,finish_time,time_elapsed\n')
# for i in range(10):
#     for run in range(total_runs):
#         threads_used = 2**i
#         with open(f'../temp_files/python/results_word_finder_with_threads.csv', '+a', encoding='utf-8') as f:
#             start_time = datetime.datetime.now().time()
#             file_path = '..\\temp_files\\exemplo_maior.txt'
#             finder = word_finder.WordFinder('junior')
#             with open(file_path, 'r', encoding='utf-8') as example_file:
#                 lines = example_file.readlines()
#             # finder.word_finder(lines)
#             # finder.word_finder_with_threads(lines)
#             finder.word_finder_with_threads_max_threads_selected(lines, max_threads=threads_used)
#             print(len(finder.matches))
#             finish_time = datetime.datetime.now().time()
#             print(f'start_time = {start_time}')
#             print(f'finish_time = {finish_time}')
#             t1 = datetime.datetime.strptime(start_time.strftime("%H:%M:%S"), "%H:%M:%S")
#             t2 = datetime.datetime.strptime(finish_time.strftime("%H:%M:%S"), "%H:%M:%S")
#             time_elapsed = (t2.microsecond - t1.microsecond)
#             f.write(f'{total_runs},{run},with {threads_used} threads,{len(lines)},{len(finder.matches)},{start_time},{finish_time},{time_elapsed}\n')
##### Word Finder #####




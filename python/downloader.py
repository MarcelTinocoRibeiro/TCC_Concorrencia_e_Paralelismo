import threading
import datetime
import requests
import time
import os
class Download():
    def __init__(self, url, file_path, total_partitions, file_results_comparator):
        self.url = url
        self.file_path = file_path
        self.total_partitions = total_partitions
        self.file_results_comparator = file_results_comparator
    
    def get_elapsed(self, start):
        print('start', start)
        finish = datetime.datetime.now().time()
        t1 = datetime.datetime.strptime(start.strftime("%H:%M:%S"), "%H:%M:%S")
        print('finish', finish)
        t2 = datetime.datetime.strptime(finish.strftime("%H:%M:%S"), "%H:%M:%S")
        elapsed = t2 - t1
        print('elapsed', elapsed.total_seconds())
        return finish, elapsed.total_seconds()

    def do_sequencial(self, runs):
        for run in range(runs):
            start =  datetime.datetime.now().time()
            header = {"User-Agent":"Python Downloader"}
            response = requests.request('GET', self.url, headers=header, stream=True)
            size = int(response.headers['content-length'])
            print(f'Download file size is {size} bytes.')
            with open(self.file_path, '+wb') as f:
                f.write(response.content)
                f.flush()
            finish, elapsed = self.get_elapsed(start)
            self.file_results_comparator.write(f'{runs},{run},sequencial_video,{self.total_partitions},{size},{size},{start},{finish},{elapsed}\n')

    def merge_files(self):
        start_rewrite = datetime.datetime.now().time()
        with open(self.file_path, '+wb') as fw:
            for index in range(self.total_partitions):
                temp_file = f'../temp_files/python/python_partition_{index}.tmp'
                with open(temp_file, 'rb') as ff:
                    fw.write(ff.read())
                os.remove(temp_file)
        finish_rewrite = datetime.datetime.now().time()
        print(f'start_rewrite = {start_rewrite}')
        print(f'finish_rewrite = {finish_rewrite}')
    
    # Thread function to download partition
    def thread_download_partition(self, index, each_size):
        start_byte = 0 if index == 0 else index * each_size + 1
        end_byte = index * each_size + each_size if index < self.total_partitions - 1 else each_size * self.total_partitions - 1
        header = {'Range':f'bytes={int(start_byte)}-{int(end_byte)}'}
        response = requests.request('GET', self.url, headers=header, stream=True)
        print(f' Working on chunk {index+1} of {self.total_partitions}')
        with open(f'../temp_files/python/python_partition_{index}.tmp', '+wb') as f:
            f.write(response.content)
            f.flush()
        return

    def do_threading_divided(self, runs):
        for run in range(runs):
            start =  datetime.datetime.now().time()
            header = {"User-Agent":"Python Downloader"}
            response = requests.request('HEAD', self.url, headers=header, stream=True)
            if response.status_code > 299:
                raise Exception(f"Error: {response.status_code} {response.reason}")
            size = int(response.headers["Content-Length"])
            print(f'Download file size is {size} bytes.')
            each_size = int(size / self.total_partitions)
            print(f'Each size is {each_size} bytes.')
            threads = []
            for index in range(self.total_partitions):
                thread = threading.Thread(name=f'Chunk Downloader Thread {index+1}', target=self.thread_download_partition, args=(index, each_size))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
            while threading.active_count() != 1:
                continue
            ## Merging files into final file_path
            self.merge_files()
            finish, elapsed = self.get_elapsed(start)
            self.file_results_comparator.write(f'{runs},{run},threading_text,{self.total_partitions},{size},{size},{start},{finish},{elapsed}\n')
            self.file_results_comparator.flush()

    def do_sequencial_divided(self, runs):
        for run in range(runs):
            start =  datetime.datetime.now().time()
            header = {"User-Agent":"Python Downloader"}
            response = requests.request('HEAD', self.url, headers=header, stream=True)
            if response.status_code > 299:
                raise Exception(f"Error: {response.status_code} {response.reason}")
            size = int(response.headers["Content-Length"])
            print(f'Download file size is {size} bytes.')
            each_size = int(size / self.total_partitions)
            print(f'Each size is {each_size} bytes.')
            for index in range(self.total_partitions):
                start_byte = 0 if index == 0 else index * each_size + 1
                end_byte = index * each_size + each_size if index < self.total_partitions - 1 else size - 1
                header = {'Range':f'bytes={int(start_byte)}-{int(end_byte)}'}
                response = requests.request('GET', self.url, headers=header, stream=True)
                print(f' Working on chunk {index+1} of {self.total_partitions}')
                with open(f'../temp_files/python/python_partition_{index}.tmp', '+wb') as f:
                    f.write(response.content)
                    f.flush()
            ## Merging files into final file_path
            self.merge_files()
            finish, elapsed = self.get_elapsed(start)
            self.file_results_comparator.write(f'{runs},{run},threading_divided,{self.total_partitions},{size},{size},{start},{finish},{elapsed}\n')

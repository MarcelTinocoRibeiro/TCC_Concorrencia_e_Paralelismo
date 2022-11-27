import threading
import datetime
import requests
import time
import os

def clean_rewrite_file():
    # Reescrevendo o arquivo para que fique mais legível
    while True:
        try:
            start_rewrite = datetime.datetime.now().time()
            with open('test_temp.txt', 'r', encoding='utf-8') as ff:
                with open('test.txt', '+w', encoding='utf-8') as fw:
                        line = ff.readline()
                        while line != '':
                            if line != '' and line != '\n':
                                fw.write(f'{line}')
                                fw.flush()
                            line = ff.readline()
            os.remove('test_temp.txt')
            finish_rewrite = datetime.datetime.now().time()
            print(f'start_rewrite = {start_rewrite}')
            print(f'finish_rewrite = {finish_rewrite}')
            return
        except Exception as e:
            print(e)
class Download():
    def __init__(self, url, file_path, total_partitions, file_results_comparator):
        self.url = url
        self.file_path = file_path
        self.total_partitions = total_partitions
        self.file_results_comparator = file_results_comparator
    

    def do_sequencial(self):
        header = {"User-Agent":"Python Downloader"}
        response = requests.request('GET', self.url, headers=header, stream=True)
        size = int(response.headers['content-length'])
        print(f'Download file size is {size} bytes.')
        with open(self.file_path, '+wb') as f:
            f.write(response.content)
            f.flush()

    def merge_files(self):
        start_rewrite = datetime.datetime.now().time()
        try:
            os.remove(self.file_path)
        except:
            pass
        with open(self.file_path, '+ab') as fw:
            for index in range(self.total_partitions):
                temp_file = f'../temp_files/python/python_partition_{index}.tmp'
                with open(temp_file, 'rb') as ff:
                    fw.write(ff.read())
                os.remove(temp_file)
        finish_rewrite = datetime.datetime.now().time()
        print(f'start_rewrite = {start_rewrite}')
        print(f'finish_rewrite = {finish_rewrite}')
    
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

    def do_threading_divided(self):
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
            print(thread.name)
        while threading.active_count() != 1:
            continue
        ## Merging files into final file_path
        self.merge_files()

    def do_sequencial_divided(self):
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

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
    def __init__(self, url, file_path, total_partitions):
        self.url = url
        self.file_path = file_path
        self.total_partitions = total_partitions
    
    def get_new_request(self, method, header):
        # stream=True permite baixar o arquivo por partes assim que estiver disponível
        # sem a necessidade de aguardar todo o arquivo ser baixado
        response = requests.request(method, self.url, headers=header, stream=True)
        return response

    def do(self):
        header = {"User-Agent":"Python Downloader"}
        response = requests.request('HEAD', self.url, headers=header, stream=True)
        # response = self.get_new_request('GET', header={"User-Agent":"Python Downloader"})
        if response.status_code > 299:
            raise Exception(f"Error: {response.status_code} {response.reason}")
        size = response.headers["Content-Length"]
        print(f'Download file size is {size} bytes.')
        each_size = float(size) / self.total_partitions
        print(f'Each size is {float(each_size)} bytes.')
        with open('test_temp.txt', '+w', encoding='utf-8') as f:
            for index, chunk in enumerate(response.iter_content(chunk_size=int(each_size), decode_unicode=True)):
                print(f' Working on chunk {index+1} of {self.total_partitions}')
                if chunk:
                    try:
                        for line in str(chunk).split('\n'):
                            f.write(line + '\n')
                    except Exception as e:
                        print(e)
                    f.flush()
        ## Reescrevendo o arquivo para que fique mais legível
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




    def download_partition(self, index, content_start, content_end):
        response = self.get_new_request('GET', header={"Range":f'bytes={content_start}-{content_end}'})
        print(f'Downloaded {response.headers["Content-Length"]} bytes for partition {index+1}')
        bytes_to_write = response.content
        with open(f'partition-{index}.tmp', '+w', encoding='utf-8') as f:
            f.write(str(bytes_to_write))
            f.flush()

    def merge_files(self):
        with open(self.file_path, '+w', encoding='utf-8') as f:
            #
            for index in range(self.total_partitions):
                temp_file_path = f'partition-{index}.tmp'
                with open(temp_file_path, 'r', encoding='utf-8') as temp_file:
                    lines_to_merge = temp_file.readlines()
                f.writelines(lines_to_merge)
                f.flush()
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    print(e)



    def do_threading_divided(self):
        header = {"User-Agent":"Python Downloader"}
        response = requests.request('HEAD', self.url, headers=header, stream=True)
        if response.status_code > 299:
            raise Exception(f"Error: {response.status_code} {response.reason}")
        size = int(response.headers["Content-Length"])
        print(f'Download file size is {size} bytes.')
        each_size = int(size / self.total_partitions)
        print(f'Each size is {each_size} bytes.')
        for index in range(self.total_partitions):
            with open('test_temp.txt', '+w', encoding='utf-8') as f:
                threads = []
                start_byte = 0 if index == 0 else index * each_size + 1
                end_byte = index * each_size + each_size if index < self.total_partitions - 1 else size - 1
                header = {'Range':f'bytes={int(start_byte)}-{int(end_byte)}'}
                # response = requests.request('GET', self.url, headers=header, stream=True)
                # print(f' Working on chunk {index+1} of {self.total_partitions}')
                thread = threading.Thread(name=f'Chunk Downloader Thread {index+1}', target=thread_download, args=(header, index, each_size))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
                print(thread.name)
            # ## Reescrevendo o arquivo para que fique mais legível
            # start_rewrite = datetime.datetime.now().time()
            # with open('test_temp.txt', 'r', encoding='utf-8') as ff:
            #     with open('test.txt', '+w', encoding='utf-8') as fw:
            #             line = ff.readline()
            #             while line != '':
            #                 if line != '' and line != '\n':
            #                     fw.write(f'{line}')
            #                     fw.flush()
            #                 line = ff.readline()
            # os.remove('test_temp.txt')
            # finish_rewrite = datetime.datetime.now().time()
            # print(f'start_rewrite = {start_rewrite}')
            # print(f'finish_rewrite = {finish_rewrite}')

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
            with open(f'../temp_files/python/python_partition_{index}.tmp', '+w', encoding='utf-8') as f:
                for line in response.iter_content(chunk_size=each_size, decode_unicode=True):
                    f.writelines(line.split('\n'))
                    f.flush()
        ## Reescrevendo os arquivos em um único
        start_rewrite = datetime.datetime.now().time()
        os.remove(self.file_path)
        for index in range(self.total_partitions):
            temp_file = f'../temp_files/python/python_partition_{index}.tmp'
            with open(temp_file, 'r', encoding='utf-8') as ff:
                with open(self.file_path, '+a', encoding='utf-8') as fw:
                        line = ff.readline()
                        while line != '':
                            fw.write(f'{line}')
                            fw.flush()
                            line = ff.readline()
            os.remove(temp_file)
            finish_rewrite = datetime.datetime.now().time()
            print(f'start_rewrite = {start_rewrite}')
            print(f'finish_rewrite = {finish_rewrite}')




def thread_write(chunk, to_write):
    line = str(chunk)
    if line != '' and line != '\n':
        to_write.write(f'{line}')
        to_write.flush()

def thread_download(self, header, index, each_size):
    response = requests.request('GET', self.url, headers=header, stream=True)
    print(f' Working on chunk {index+1} of {self.total_partitions}')
    with open(f'../temp_files/python/python_partition_{index}.tmp', '+w', encoding='utf-8') as f:
        for line in response.iter_content(chunk_size=each_size, decode_unicode=True):
            f.writelines(line.split('\n'))
            f.flush()
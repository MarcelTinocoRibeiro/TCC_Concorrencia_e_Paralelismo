import requests
import time
import os

class Download():
    def __init__(self, url, file_path, total_partitions):
        self.url = url
        self.file_path = file_path
        self.total_partitions = total_partitions
    
    def get_new_request(self, method, header):
        response = requests.request(method, self.url, headers=header, stream=True)
        return response

    def do(self):
        response = self.get_new_request('HEAD', header={"User-Agent":"Python Downloader"})
        if response.status_code > 299:
            raise Exception(f"Error: {response.status_code} {response.reason}")
        size = response.headers["Content-Length"]
        print(f'Size is {size} bytes.')
        each_size = float(size) / self.total_partitions
        print(f'Each size is {float(each_size)} bytes.')
        r = requests.get(self.url, stream=True)
        with open('test.txt', '+w', encoding='utf-8') as f:
            for index, chunk in enumerate(r.iter_content(chunk_size=int(each_size))):
                print(f' Working on chunk {index+1} of {self.total_partitions+1}')
                if chunk:
                    f.write(str(chunk))
                    f.flush()
        # partitions = []
        # for index in range(self.total_partitions):
        #     if index == 0:
        #         partitions.append((index, float(each_size)-1))
        #     else:    
        #         partitions.append((index*float(each_size), index*float(each_size) + float(each_size) - 1))
        # print(partitions)
        # for index, content in enumerate(partitions):
        #     content_start = content[0]
        #     content_end = content[1]
        #     self.download_partition(index, content_start, content_end)
        # self.merge_files()

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

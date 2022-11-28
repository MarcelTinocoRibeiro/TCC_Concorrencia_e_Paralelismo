import threading
import time
import datetime


class WordFinder():
    def __init__(self, word):
        self.word = word
        self.threads = []
        self.threads_started_time = []
        self.matches = []

    def find_word(self, line):
        if self.word in line:
            return line
        return ''

    def find_word_threading(self, line, word, index):
        # print(f'line = {line.strip()}') # Print apenas para observarmos o comportamento da execução
        # print(f'index = {index}') # Print apenas para observarmos o comportamento da execução
        # Ao usarmos Threads em Python, é necessário que
        # criemos estruturas para armazenarmos o que seria
        # um retorno da Thread executada
        if word in line:
            self.matches.append(line)

    def set_word(self, word):
        self.word = word
    
    def word_finder(self, lines):
        for index, line_to_check in enumerate(lines):
            line = self.find_word(line_to_check)
            if line != '':
                self.matches.append(line)

    def word_finder_with_threads_x_lines_per_thread(self, lines, lines_per_thread=30):
        start_rewrite = datetime.datetime.now().time()
        try:
            line_counter = times = thread_counter = 0
            # Definimos uma lista do mesmo tamanho que a quantidade de linhas percorridas
            while line_counter < len(lines):
                start = times * lines_per_thread
                end = len(lines) if len(lines) - line_counter <= 30 else times * lines_per_thread + lines_per_thread
                thread_name = f'thread {thread_counter} working'
                thread_counter += 1
                lines_to_thread = lines[start:end]
                thread = threading.Thread(name=thread_name, target=self.word_finder, args=[lines_to_thread])
                self.threads.append(thread)
                self.threads_started_time.append(datetime.datetime.now().time())
                thread.start()
                line_counter += len(lines_to_thread)
                times += 1
            for thread in self.threads:
                thread.join()
        except Exception as e:
            print(e)
        finish_rewrite = datetime.datetime.now().time()
        print(f'start_rewrite = {start_rewrite}')
        print(f'finish_rewrite = {finish_rewrite}')

    def word_finder_with_threads_max_threads_selected(self, lines, max_threads=30):
        try:
            thread_counter = 0
            # Definimos uma lista do mesmo tamanho que a quantidade de linhas percorridas
            for thread_counter in range(max_threads):
                start = 0 if thread_counter == 0 else int(len(lines) / max_threads) * thread_counter
                end = len(lines) if thread_counter == max_threads-1 else int(len(lines) / max_threads) * thread_counter + int(len(lines) / max_threads)
                lines_to_thread = lines[start:end]
                thread = threading.Thread(name=f'thread {thread_counter} working', target=self.word_finder, args=[lines_to_thread])
                self.threads.append(thread)
                self.threads_started_time.append(datetime.datetime.now().time())
                thread.start()
            for thread in self.threads:
                thread.join()
            while threading.active_count() != 1:
                continue
        except Exception as e:
            print(e)
        
# class CustomThread(threading.Thread):
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
#         super(CustomThread, self).__init__(group=group, target=target, args=args, name=name)
#         self.name = name
#         self.target = target
#         self.args = args
#         self.kwargs = kwargs
#         return

#     def run(self):
#         try:
#             if self._target:
#                 self._target(*self._args, **self._kwargs)
#         except Exception as e:
#             print(e)

#     def set_args(self, line, word, thread_counter):
#         self.args = line, word, thread_counter
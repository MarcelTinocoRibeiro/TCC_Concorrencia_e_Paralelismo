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
        # self.matches.append(line) = line if word in line else ''
        if word in line:
            self.matches.append(f'thread {index} got line: {line.strip()}')

    def set_word(self, word):
        self.word = word
    
    def word_finder_without_threads(self, lines):
        for line_to_check in lines:
            line = self.find_word(line_to_check)
            if line != '':
                self.matches.append(line)

    def word_finder_with_threads(self, lines, max_threads=30):
        try:
            # Definimos uma lista do mesmo tamanho que a quantidade de linhas percorridas
            self.matches = ['' for x in lines]
            for index, line in enumerate(lines):
                thread = threading.Thread(name=f'thread {index} working on line {line}', target=self.find_word_threading, args=[line, self.word, index])
                self.threads.append(thread)
                self.threads_started_time.append(datetime.datetime.now().time())
                thread.start()
            # for index, thread in enumerate(self.threads):
            #     thread.join()
        except Exception as e:
            print(e)
        for index, thread in enumerate(self.threads):
            print(f'thread.name = {thread.name} and self.threads_started_time[index] = {self.threads_started_time[index]}')
        self.matches = list(filter(None, self.matches))
        for line in self.matches:
            if line: print(f'line = {line.strip()}')
        
        


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
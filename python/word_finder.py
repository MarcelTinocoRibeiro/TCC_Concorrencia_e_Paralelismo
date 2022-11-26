import threading
import time
from datetime import datetime

def find_word(word, line):
    if word in line:
        return line
    return ''

class WordFinder():
    def __init__(self, word):
        self.word = word
        self.threads = []
        self.threads_stated_time = []
        self.matchs = []

    def set_word(self, word):
        self.word = word                
    
    def word_finder(self, lines):
        for line in lines:
            word = find_word(self.word, line)
            if word != '':
                self.matchs.append(word)

    def word_finder_with_thread(self, lines):
        for line in lines:
            self.threads.append(threading.Thread(name=line, target=self.find_word, args=(self.word, line)))
            self.threads_stated_time.append(datetime.time())
            self.threads[-1].start()
            self.threads[-1].join()

    def checking_threads(self):
        for thread in self.threads:
            print(thread.value)


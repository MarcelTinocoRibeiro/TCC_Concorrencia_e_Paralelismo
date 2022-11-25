import threading

def find_word(word, line):
    if word in line:
        return line
    return ''


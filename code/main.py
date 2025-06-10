import os
from word_search import *
from generate_pdf import *
from file_io import *

filePath = "C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\word_lists\\"
fileName = "test.txt"

if __name__ == '__main__':
    themes, masks, sizes, words = parse_word_list(filePath+fileName, default_size=(20,20))
    print(themes)
    print(masks)
    print(sizes)
    print(words)
    #width = 15
    #height = 15
    puzzles = []
    puzzles.append(Word_Search(themes[0], words[0], sizes[0], mask=masks[0],mode='m'))
    print(puzzles[0].solutions)
    create_word_search_pdf(puzzles[0], puzzles[0].words, "test.pdf")
    os.startfile("test.pdf")
    #for i in range(len(themes)):
    #    puzzles.append(Word_Search(themes[i], words[i], sizes[i], mode='a'))

    #create_word_search_pdf(puzzles[0], puzzles[0].words, 'test0.pdf')
    #create_word_search_pdf(puzzles[1], puzzles[1].words, 'test1.pdf')
    #create_word_search_pdf(puzzles[2], puzzles[2].words, 'test2.pdf')
    #for word in words:
    #    puzzles.append(Word_Search(word[0], word[1:6], (15,15), mode='auto'))
    #    break

    #create_word_search_pdf(puzzles[0], puzzles[0].words, "test.pdf")
    #print('complete')


    #os.startfile("test0.pdf")
    #os.startfile("test1.pdf")
    #os.startfile("test2.pdf")
    #puzzles[2].display_puzzle()
    #puzzles[7].display_puzzle()
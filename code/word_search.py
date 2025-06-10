import random
import string
from PIL import Image
import numpy as np
import cv2

"""
TODO:
Mask: Option to edit mask or reject if it doesn't turn out well
Manual: option to automate rest of word placements

"""
MASK_FILEPATH = '..\\word searches\\masks\\'

class Word_Search:
    def __init__(self, title='Word Search', subtitle='', word_list=None, size=(15,15), mask='', board=False, solutions=None, backwards=True, mode='auto'):
        self.title = title # title/theme of puzzle
        self.subtitle = subtitle
        if not word_list:
            self.words = [] # words to be found in puzzle
        else:
            self.words = word_list
        self.rows = size[0] # num rows
        self.cols = size[1] # num cols
        self.backwards = backwards # allow backward words?
        self.mask = mask # optional mask, default is rectangular
        self.mask_bool = False
        self.complete = False # Puzzle is completely generated
        if solutions:
            self.solutions = solutions
        elif self.words:
            self.solutions = [None] * len(self.words) # (row, col), (dx, dy), length
        else:
            self.solutions = []
        if board:
            self.board = board
        elif self.mask: # apply mask
            self.mask_bool = True
            img = create_mask(MASK_FILEPATH+mask, self.rows, self.cols)
            self.board = [[' ' if value == 0 else '-' for value in row] for row in img]
        else:
            self.board = [['-' for _ in range(self.cols)] for _ in range(self.rows)]
        # set mode to auto or manual
        if mode == 'auto' or mode == 'a':
            self.mode = 0
        elif mode == 'manual' or mode == 'm':
            self.mode = 1
        elif mode == 'gui':
            self.mode = 2
        else:
            print('Invalid Mode')
            exit()
        self.create_puzzle()
    
    def resize(self, row, col):
        # Resize the grid and create a blank grid of new size
        self.rows = row
        self.cols = col
        if self.mask and self.mask_bool: # apply mask
            img = create_mask(MASK_FILEPATH+self.mask, row, col)
            self.board = [[' ' if value == 0 else '-' for value in row] for row in img]
        else:
            self.board = [['-' for _ in range(col)] for _ in range(row)]
        self.solutions = [None] * len(self.words)
        self.complete = False

    def add_word(self, word):
        self.words.append(word)
        self.solutions.append(None)

    def remove_word(self, word):
        # remove word from puzzle
        index = self.words.index(word)
        self.words.remove(word)
        self.solutions.pop(index)
        self.complete = False

    def remove_solution(self, sol_index):
        # Solution Format: (row, col), (dx, dy), length
        solution = self.solutions[sol_index]
        if solution:
            row = solution[0][0]
            col = solution[0][1]
            for _ in range(solution[2]):
                self.board[row][col] = '-'
                row += solution[1][1]
                col += solution[1][0]
            self.solutions[sol_index] = None
            self.complete = False


    def create_puzzle(self):
        if not self.mode: # automatic
            for word in self.words:
                self.place_word(word)
        elif self.mode == 1: # manual
            for word in self.words:
                self.place_word_manual(word)
            self.display_puzzle(list_pos='r', rows_nums=True, cols_nums=True)
        elif self.mode == 2: #GUI
            return
        self.fill()
        

    def display_puzzle(self, list_pos='bottom', rows_nums=False, cols_nums=False):
        display = f"       {self.title}\n"
        row_num = 0
        word_num = 0
        if cols_nums:
            display += "    "
            for col in range(self.cols):
                display = display + str(col%10) + " "
            display += "\n"

        for row in self.board:
            if rows_nums:
                if row_num < 10:
                    display = display + str(row_num) + " | "
                else:
                    display = display + str(row_num) + "| "
                row_num += 1
            for col in row:
                display = display + col + " "
            
            if (list_pos.lower() == 'right' or list_pos.lower() == 'r') and word_num < len(self.words):
                display += self.words[word_num]
                word_num += 1
            display += "\n"
        
        if list_pos.lower() == 'bottom' or list_pos.lower() == 'b':    
            for word in self.words:
                display = display + word + "\n"
        print(display)
    
    def fill(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '-':
                    self.board[row][col] = random.choice(string.ascii_uppercase)
        self.complete = True
    
    def clear_board(self):
        for i in range(len(self.solutions)):
            self.solutions[i] = None
        for ii in range(self.rows):
            for jj in range(self.cols):
                if self.board[ii][jj] not in (' ', ''):
                    self.board[ii][jj] = '-'
        self.complete = False

    def test_candidate(self, word, dir, row, col):
        """ Test if location col, row is valid for word and orientation"""
        for ii in range(len(word)):
            if word[ii] == ' ': # ignore spaces
                continue
            if row >= self.rows or col >= self.cols or row < 0 or col < 0:
                return False
            if self.board[row][col] not in ('-', word[ii]):
                return False

            row += dir[1]
            col += dir[0]
        return True

    def place_word(self, word, row, col, dir):
        """place the word on the board after verifying valid placement"""
        for ii in range(len(word)):
            if word[ii] != ' ': # ignore spaces
                self.board[row][col] = word[ii]
                row += dir[1]
                col += dir[0]

    def place_word_manual(self, word_org):
        """Place a word on the board manually by choosing the row, column, and direction 
        (orientation) of the word"""
        # Display directions and board
        print(f"Place Word \"{word_org}\":")
        print('Enter Row Column Direction of the word\nDirection can be L, R, U, D, UR, UL, DR, DL')
        print("Other Commands: \'reset\' to remove all words from the grid\n  \
              \'show\' to display the grid\n  \
              \'q\' to quit program")
        self.display_puzzle(list_pos='r', rows_nums=True, cols_nums=True)
        word = word_org.replace(" ","").upper()
        
        valid_input = False
        while not valid_input: # loop until valid command given
            command = input("Enter Row Column Direction: ").strip().upper().split(" ")
            if len(command) == 1:
                if command[0] == 'RESET': # Remove all previously placed words from the board
                    self.clear_board()
                    self.create_puzzle()
                    break
                elif command[0] == 'Q' or command[0] == 'QUIT': # Exit program
                    exit(0)
                elif command[0] == 'S' or command[0] == 'SHOW': # Display board
                    self.display_puzzle(list_pos='r', rows_nums=True, cols_nums=True)
                    continue
                else:
                    print('Invalid Command')
                    continue
            elif len(command) != 3:
                print('Invalid Command')
                continue
            
            # split command
            row = int(command[0])
            col = int(command[1])
            dir = command[2]
            
            # validate row and col input
            if row >= self.rows or row < 0:
                print('Invalid Row, Try again')
                continue
            if col >= self.cols or col < 0:
                print('Invalid Column, Try again')
                continue

            if dir == 'L': # left orientation
                dir = (-1,0)
            elif dir == 'R': # right orientation
                dir = (1,0)
            elif dir == 'U': # upwards orientation
                dir = (0,-1)
            elif dir == 'D': # Down orientation
                dir = (0,1)
            elif dir == 'UR': # Up Right orientation
                dir = (1,-1)
            elif dir == 'UL': # Up Left orientation
                dir = (-1,-1)
            elif dir == 'DR': # Down right orientation
                dir = (1,1)
            elif dir == 'DL': # Down left orientation
                dir = (-1,1)
            else:
                print('Invalid Placement')
                continue
            if self.test_candidate(word, dir, row, col):
                    self.place_word(word, row, col, dir)
                    valid_input = True
                    self.solutions[self.words.index(word_org)] = [(row, col), dir, len(word)]

            else:
                print(f'ERROR: Cannot place {word_org}, Try Again!')
            
    def place_word_auto(self, word):
        # 0 - Horz, 1 - Vert, 2 - Diagonal (TL -> BR), 3- Diagonal (BL -> TR)
        # No option not to place words backwards
        word_i = word.replace(" ","").upper()
        direction = [(0,1), (1,0), (1,1), (1,-1)]
        random.shuffle(direction)
        placed = False
        word_length = len(word_i)
        for (dx, dy) in direction:
            if self.backwards and random.randint(0,1):
                word_i = word_i[::-1]
            min_col = 0
            max_col = self.cols - word_length if dx else self.cols-1
            min_row = 0 if dy >= 0 else word_length - 1
            max_row = self.rows - word_length if dy >= 0 else self.rows-1
            if min_col > max_col or min_row > max_row: # no possible placement
                continue
            poss = [] 
            for i in range(min_row, max_row+1):
                for j in range(min_col, max_col+1):
                    if self.test_candidate(word_i, (dx, dy), i, j):
                        poss.append((i, j))
            if not poss:
                continue
            location = random.choice(poss)
            row, col = location[0], location[1]
            index = self.words.index(word)
            self.solutions[index] = [(row, col), (dx, dy), word_length]
            for k in range(word_length):
                self.board[row][col] = word_i[k]
                row += dy
                col += dx
            placed = True
            break

        return placed


def create_mask(image_path, rows, cols, threshold=256):
    image = cv2.imread(image_path, 0)
# Apply a binary threshold to create a mask
    _, mask = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY_INV)
    image=cv2.bitwise_not(mask)
    img_resized = cv2.resize(mask, (rows, cols),  Image.NEAREST)
    return img_resized

    
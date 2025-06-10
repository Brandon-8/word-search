from ws_manager import Word_Search_Manager
from word_search import Word_Search
from tkinter import filedialog, messagebox
import os
import subprocess
import sys
from generate_pdf import *
from PyPDF2 import PdfReader, PdfWriter

"""
TODO:
    export pdf specific pages
"""
def parse_word_list(filePath, default_size=(20,20)):
    themes, masks, sizes, words, boards, solutions, subtitles = [], [], [], [], [], [], []
    index = -1
    saved = False
    if 'word searches' or 'saved' in filePath:
        with open(filePath, "r",encoding='utf-8') as f:
            for line in f:
                l = line.strip()
                if l:
                    # get theme, new puzzle
                    if l[0].isdigit() or l[0] == '#' or l[:6].lower() == 'theme:' or l[:6].lower() == 'title:':
                        themes.append(' '.join(l.split(" ")[1:]))
                        index += 1
                        masks.append('')
                        sizes.append(default_size)
                        words.append([])
                        boards.append([])
                        solutions.append([])
                        subtitles.append('')
                        word_list = False
                        grid = False
                        sols = False
                    elif l[:9].lower() == 'subtitle:':
                        subtitles[index] = ' '.join(l.split(" ")[1:])
                    elif l[:5].lower() == 'mask:': # get mask file name
                        print(l)
                        masks[index] = l.split(" ")[1]
                    elif l[:5].lower() == 'size:' and 'x' not in l.lower(): # Size: 15 15
                        temp = l.split(" ")[1:]
                        sizes[index] = (int(temp[0]), int(temp[1]))
                    elif l[:5].lower() == 'size:' and 'x' in l.lower():
                        temp = l.lower().split(" ")
                        print(temp)
                        if len(temp) == 2: # Size: 15x15
                            temp = temp[1].lower().split('x')
                            sizes[index] = (int(temp[0]), int(temp[1]))
                        elif len(temp) == 4: # Size: 15 x 15
                            sizes[index] = (int(temp[1]), int(temp[3]))
                        print(sizes[index])  
                    elif 'puzzle grid:' in l.lower():
                        saved = True
                        grid = True
                        word_list = False
                        sols = False
                    elif 'word list:' in l.lower():
                        word_list = True
                        grid = False
                        sols = False
                    elif 'solutions:' in l.lower():
                        word_list = False
                        grid = False
                        sols = True
                    elif grid and len(boards[index]) < sizes[index][0]:
                        temp_board = []
                        for i,char in enumerate(line):
                            if not i%2:
                                temp_board.append(char)
                        boards[index].append(temp_board)

                    elif sols:
                        if l:
                            parse = l.replace('(', '').replace(')', '').replace(',', '').split(' ')
                            solutions[index].append([(int(parse[0]), int(parse[1])), 
                                              (int(parse[2]), int(parse[3])), int(parse[4])])
                        else:
                            solutions[index].append(None)
                    elif l != '' and words: # word_list
                        words[index].append(l.upper())
    else:
        print('Invalid FilePath')
        exit(-1)
    return themes, subtitles, masks, sizes, words, boards, solutions, saved

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}_{counter}{ext}"
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base}_{counter}{ext}"
    return new_filename

def save_word_searches(fileName, puzzles):
    try:
        # Open the file in write mode (creates the file if it doesn't exist)
        with open(fileName, 'w') as file:
            if not puzzles:
                exit()
            for index in range(len(puzzles)):
                # Write the puzzle grid
                file.write(f"Theme: {puzzles[index].title}\n")
                file.write(f"Subtitle: {puzzles[index].subtitle}\n")
                file.write(f"Size: {puzzles[index].rows} x {puzzles[index].cols}\n")
                if puzzles[index].mask:
                    file.write(f"Mask: {puzzles[index].mask}\n")

                file.write("Puzzle Grid:\n")
                for row in puzzles[index].board:
                    file.write(' '.join(row) + '\n')  # Write each row of the grid

                # Write the word list
                file.write("\nWord List:\n")
                for word in puzzles[index].words:
                    file.write(word + '\n')
                

                file.write("Solutions:\n")
                for sol in puzzles[index].solutions:
                    if sol:
                        for ele in sol:
                            file.write(str(ele) + ' ')
                    file.write('\n')
                file.write("\n")

        print(f"Puzzles saved successfully to {fileName}.")

    except Exception as e:
        print(f"An error occurred while saving the puzzle: {e}")    

def new_file(file_path=None):
    if file_path:
        main_script = os.path.join(os.path.dirname(__file__), "gui.py")
        subprocess.Popen([sys.executable, main_script, file_path])    
    else:
        main_script = os.path.join(os.path.dirname(__file__), "gui.py")
        subprocess.Popen([sys.executable, main_script])

def open_file(manager):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], initialdir='..\\word searches')
    if manager.puzzles and file_path:
        new_file(file_path)
    else:    
        load_word_search(manager, file_path)

def save_file(ws_manager):
    if ws_manager.prev_file:
        save_word_searches(ws_manager.file_path, ws_manager.puzzles)
    else:
        save_as(ws_manager)

def save_as(ws_manager):
    print('save as')
    puzzles = ws_manager.puzzles
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")],
                                             initialfile= ws_manager.title,
                                             initialdir='..\\word searches')
    if file_path:
        save_word_searches(file_path, puzzles)

def load_word_search(ws_manager, file_path):
    if file_path:
        ws_manager.title = os.path.splitext(os.path.basename(file_path))[0]
        themes, subtitles, masks, sizes, words, boards, solutions, saved = parse_word_list(file_path)
        ws_manager.prev_file = saved
        for i in range(len(themes)):
            ws_manager.puzzles.append(Word_Search(themes[i], subtitles[i], words[i], sizes[i], masks[i], boards[i], solutions[i], mode='gui'))
        ws_manager.puzzle_index=0
        ws_manager.file_path = file_path
        ws_manager.display_current_puzzle()

def export(window, manager, page_options, sol_options, puzz_filePath, sol_filePath, size, view=None):
    print('size', size)
    puzzles = []
    if type(page_options) is tuple: # Pages
        pass
    elif page_options == 'All':
        export_all(manager, puzz_filePath, size)
        puzzles = manager.puzzles
    elif page_options == 'Current':
        export_to_pdf(manager, puzz_filePath, size)
        puzzles = manager.puzzles[manager.puzzle_index]

    if type(sol_options) is tuple:
        print('Separate Sol File')
        if not sol_options[1]:
            sol_filePath = f'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\{manager.title}_solutions.pdf'
        create_ws_solutions(puzzles, sol_filePath, size)
    elif sol_options == 'Same File':
        print('Same Sol File')
        temp = f'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\temp56789120456892_solutions.pdf'
        create_ws_solutions(puzzles, temp, size)
        merge_pdfs(puzz_filePath, temp)

    if view:
        os.startfile(puzz_filePath)
        print(sol_options, sol_filePath)
        if sol_filePath:
            os.startfile(sol_filePath)

    window.destroy()

def export_to_pdf(ws_manager, file_path=None, page_size=letter):
    curr = ws_manager.puzzles[ws_manager.puzzle_index]
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], 
                                                initialfile=curr.title,
                                                initialdir='..\\word searches',
                                                title='Save as PDF')
        
    create_word_search_pdf([curr], file_path, page_size)

def export_all(ws_manager, file_path=None, page_size=letter):
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], 
                                                initialfile=ws_manager.title,
                                                initialdir='..\\word searches',
                                                title='Save as PDF')
        
    create_word_search_pdf(ws_manager.puzzles, file_path, page_size)

def merge_pdfs(pdf1_path, pdf2_path):
    # Open both PDF files
    pdf1 = PdfReader(pdf1_path)
    pdf2 = PdfReader(pdf2_path)

    # Create a PdfWriter object to hold the merged PDF
    pdf_writer = PdfWriter()

    # Add all pages from the first PDF
    for page_num in range(len(pdf1.pages)):
        pdf_writer.add_page(pdf1.pages[page_num])

    # Add all pages from the second PDF
    for page_num in range(len(pdf2.pages)):
        pdf_writer.add_page(pdf2.pages[page_num])

    # Write the combined PDF to a new file
    with open(pdf1_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    os.remove(pdf2_path)
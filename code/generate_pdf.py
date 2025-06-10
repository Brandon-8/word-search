from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
#from reportlab.lib import pdfmetrics
from reportlab.pdfbase import ttfonts
from reportlab.pdfgen import canvas

SIX_BY_NINE = (6*72, 9*72)
from math import cos, degrees, radians

from word_search import *

"""
TODO:
Different Fonts
works only on 20x20, find a way to scale so it works on all sizes
Other graphics separate from puzzle?
"""
# Centering helper
def center_text(pdf, y, x_start, width, text, font="Courier", size=12):
    pdf.setFont(font, size)
    text_width = pdf.stringWidth(text, font, size)
    pdf.drawString(x_start + (width - text_width) / 2, y, text)

def draw_rounded_rectangle(c, direction, x1, y1, x2, y2, radius=10):
    """
    Draws a diagonal rectangle with rounded corners.
    :param c: The canvas object.
    :param x1, y1: Coordinates of one corner of the rectangle.
    :param x2, y2: Coordinates of the opposite corner of the rectangle.
    :param radius: Radius of the rounded corners.
    """
    corner_radius = 5
    if direction == (0, 1):
        x2 += 10
        c.roundRect(x1, y1, x2-x1, y2-y1, corner_radius, fill=0)
    elif direction == (1,0):
        y2 += 10
        c.roundRect(x1, y1, x2-x1, y2-y1, corner_radius, fill=0)
    elif direction == (1,1):
        c.saveState()
        x2 = x1 + 6
        h = (y2-y1) / cos(radians(45)) + 5
        y2=h
        c.translate(x1+0.5, y1-4.5)
        c.rotate(45)
        c.roundRect(0, 0, x2-x1, h, 3, stroke=1, fill=0)
        c.restoreState()

    elif direction == (1,-1):
        c.saveState()
        x2 = x1 + 6
        h = (y2-y1) / cos(radians(45)) - 5
        y2=h
        c.translate(x1, y1+3.5)
        c.rotate(-45)
        c.roundRect(0, 0, x2-x1, h, 3, stroke=1, fill=0)
        c.restoreState()
    else:
        print('UhOh: Dir is ', direction)
        return

def create_word_search_pdf(puzzles, filename, pageSize):
    # Only works for explicit grid sizes
    max_grid_size = (0,0)
    for puzz in puzzles:
        size = (puzz.rows, puzz.cols)
        if size[0] > max_grid_size[0] and size[1] > max_grid_size[1]: # Assume square
            max_grid_size = size

    if (pageSize == '8.5 x 11' or pageSize == letter) and max_grid_size >= (20, 20):
        ws_pdf_20x20_letter(puzzles, filename)
    elif (pageSize == '6 x 9') and max_grid_size == (20, 20):
        ws_pdf_20x20_6x9(puzzles, filename)
    elif (pageSize == '6 x 9'):
        ws_pdf_10x10_6x9(puzzles, filename)

def ws_pdf_20x20_letter(puzzles, filename):
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    for index, wordSearch in enumerate(puzzles):       
        puzzle = wordSearch.board
        words = wordSearch.words
        title = wordSearch.title
        subtitle = wordSearch.subtitle

        # Title
        center_text(pdf, height - 50, 0, width, title.upper(), font="Courier-Bold", size=16)

        # Subtitle
        if not subtitle:
            subtitle = "Can you find all of the words hidden in the puzzle below?"
        center_text(pdf, height - 75, 0, width, subtitle, font="Courier", size=12)
        # Draw the puzzle
        square_size = 400  # Size of the puzzle square
        letter_spacing = square_size / wordSearch.rows  # Spacing based on puzzle size
        start_x = (width - square_size) / 2  # Centered position for the puzzle
        start_y = height - 100

        # Draw border around the puzzle
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(1)
        corner_radius = 10
        pdf.roundRect(start_x - 5, start_y - square_size + 5, square_size + 10, square_size + 10, corner_radius, fill=0)  # Draw rectangle border

        
        # Draw the puzzle inside the border
        pdf.setFont("Courier", 12)
        for i, row in enumerate(puzzle):
            for j, l in enumerate(row):
                pdf.drawString(start_x + j * letter_spacing+5, start_y - (i * letter_spacing), l)
        
        word_list_start_y = start_y - square_size - 50  # Position below the puzzle
        left_column_x = start_x  # X position for the left column
        middle_column_x = start_x + (width - 140) / 3  # X position for the middle column
        right_column_x = start_x + 2 * (width - 140) / 3  # X position for the right column

        pdf.setFont("Courier", 12)
        max_words_per_column = (len(words) + 2) // 3  # Split words into three columns

        # Word list title
        pdf.drawString(left_column_x, word_list_start_y + 20, "Words to find:")
        # Underline
        word_width = pdf.stringWidth("Words to find:", "Courier", 12)
        pdf.line(left_column_x, word_list_start_y + 18, left_column_x + word_width, word_list_start_y + 18)

        # Draw the word list in three columns
        for i, word in enumerate(words):
            if i < max_words_per_column:
                pdf.drawString(left_column_x, word_list_start_y - i * 15, word)  # Left column
            elif i < 2 * max_words_per_column:
                pdf.drawString(middle_column_x, word_list_start_y - (i - max_words_per_column) * 15, word)  # Middle column
            else:
                pdf.drawString(right_column_x, word_list_start_y - (i - 2 * max_words_per_column) * 15, word)  # Right column
        pdf.showPage()
  
    pdf.save()

def ws_pdf_20x20_6x9(puzzles, filename):
    pdf = canvas.Canvas(filename, pagesize=SIX_BY_NINE)
    width, height = SIX_BY_NINE

    for index, wordSearch in enumerate(puzzles):       
        puzzle = wordSearch.board
        words = wordSearch.words
        title = wordSearch.title
        subtitle = wordSearch.subtitle

        # Title
        center_text(pdf, height - 50, 0, width, title.upper(), font="Courier-Bold", size=16)

        # Subtitle
        if not subtitle:
            subtitle = "Can you find all of the words hidden in the puzzle below?"
        center_text(pdf, height - 75, 0, width, subtitle, font="Courier", size=12)
        # Draw the puzzle
        square_size = 300  # Size of the puzzle square
        letter_spacing = square_size / wordSearch.rows  # Spacing based on puzzle size
        start_x = (width - square_size) / 2  # Centered position for the puzzle
        start_y = height - 100

        # Draw border around the puzzle
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(1)
        corner_radius = 10
        pdf.roundRect(start_x - 5, start_y - square_size + 5, square_size + 10, square_size + 10, corner_radius, fill=0)  # Draw rectangle border

        
        # Draw the puzzle inside the border
        pdf.setFont("Courier", 12)
        for i, row in enumerate(puzzle):
            for j, l in enumerate(row):
                pdf.drawString(start_x + j * letter_spacing+5, start_y - (i * letter_spacing), l)
        
        word_list_start_y = start_y - square_size - 50  # Position below the puzzle
        left_column_x = start_x  # X position for the left column
        middle_column_x = start_x + (width - 140) / 3  # X position for the middle column
        right_column_x = start_x + 2 * (width - 140) / 3  # X position for the right column

        pdf.setFont("Courier", 12)
        max_words_per_column = (len(words) + 2) // 3  # Split words into three columns

        # Word list title
        pdf.drawString(left_column_x, word_list_start_y + 20, "Words to find:")
        # Underline
        word_width = pdf.stringWidth("Words to find:", "Courier", 12)
        pdf.line(left_column_x, word_list_start_y + 18, left_column_x + word_width, word_list_start_y + 18)

        # Draw the word list in three columns
        for i, word in enumerate(words):
            if i < max_words_per_column:
                pdf.drawString(left_column_x, word_list_start_y - i * 15, word)  # Left column
            elif i < 2 * max_words_per_column:
                pdf.drawString(middle_column_x, word_list_start_y - (i - max_words_per_column) * 15, word)  # Middle column
            else:
                pdf.drawString(right_column_x, word_list_start_y - (i - 2 * max_words_per_column) * 15, word)  # Right column
        pdf.showPage()
  
    pdf.save()

def ws_pdf_10x10_6x9(puzzles, filename):
    pdf = canvas.Canvas(filename, pagesize=SIX_BY_NINE)
    width, height = SIX_BY_NINE

    for index, wordSearch in enumerate(puzzles):       
        puzzle = wordSearch.board
        words = wordSearch.words
        title = wordSearch.title
        subtitle = wordSearch.subtitle

        # Title
        center_text(pdf, height - 50, 0, width, title.upper(), font="Courier-Bold", size=16)

        # Subtitle
        if not subtitle:
            subtitle = "Can you find all of the words hidden in the puzzle below?"
        center_text(pdf, height - 75, 0, width, subtitle, font="Courier", size=12)
        # Draw the puzzle
        square_size = 300  # Size of the puzzle square
        letter_spacing = square_size / wordSearch.rows  # Spacing based on puzzle size
        start_x = (width - square_size) / 2  # Centered position for the puzzle
        start_y = height - 100

        # Draw border around the puzzle
        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(1)
        corner_radius = 10
        pdf.roundRect(start_x - 5, start_y - square_size + 5, square_size + 10, square_size + 10, corner_radius, fill=0)  # Draw rectangle border

        
        # Draw the puzzle inside the border
        pdf.setFont("Courier", 16)
        for i, row in enumerate(puzzle):
            for j, l in enumerate(row):
                pdf.drawString(start_x + j * letter_spacing+5, start_y - (i * letter_spacing), l)
        
        word_list_start_y = start_y - square_size - 50  # Position below the puzzle
        left_column_x = start_x  # X position for the left column
        middle_column_x = start_x + (width - 140) / 3  # X position for the middle column
        right_column_x = start_x + 2 * (width - 140) / 3  # X position for the right column

        pdf.setFont("Courier", 12)
        max_words_per_column = (len(words) + 2) // 3  # Split words into three columns

        # Word list title
        pdf.drawString(left_column_x, word_list_start_y + 20, "Words to find:")
        # Underline
        word_width = pdf.stringWidth("Words to find:", "Courier", 12)
        pdf.line(left_column_x, word_list_start_y + 18, left_column_x + word_width, word_list_start_y + 18)

        # Draw the word list in three columns
        for i, word in enumerate(words):
            if i < max_words_per_column:
                pdf.drawString(left_column_x, word_list_start_y - i * 15, word)  # Left column
            elif i < 2 * max_words_per_column:
                pdf.drawString(middle_column_x, word_list_start_y - (i - max_words_per_column) * 15, word)  # Middle column
            else:
                pdf.drawString(right_column_x, word_list_start_y - (i - 2 * max_words_per_column) * 15, word)  # Right column
        pdf.showPage()
  
    pdf.save()

def create_ws_solutions(puzzles, output_file, pageSize):
    if type(puzzles) == Word_Search:
        puzzles = [puzzles]
    if (pageSize == '8.5 x 11' or pageSize == letter):
        ws_sol_20x20_6x9(puzzles, output_file)
    elif (pageSize == '6 x 9'):
        ws_sol_20x20_6x9(puzzles, output_file)

def ws_sol_20x20_6x9(puzzles, output_file):
    from reportlab.lib.pagesizes import letter
    #output_file = 'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\test_solutions.pdf'
    #c = canvas.Canvas(output_file, pagesize=letter)
    #page_width, page_height = letter
    c = canvas.Canvas(output_file, pagesize=SIX_BY_NINE)
    page_width, page_height = SIX_BY_NINE
    margin = 1 * inch
    cell_size = 10  # Size of each grid cell in points
    puzzles_per_page = 4
    puzzle_area_height = (page_height - 2 * margin) / puzzles_per_page
    # Title
    center_text(c, page_height - margin, 0, page_width, 'Solutions', font="Courier-Bold", size=16)

    # When Margin == 1
    quadrants = [
        (margin, page_height - 2*margin),  # Top-left
        (page_width - margin - cell_size*20, page_height - 2*margin),  # Top-right
        (margin, page_height/2 - margin),  # Bottom-left
        (page_width - margin - cell_size*20, page_height/2 - margin),  # Bottom-right
    ]

    # When Margin == 0.5
    #quadrants = [
    #    (margin, page_height - 3*margin),  # Top-left
    #    (page_width/2 + 2*margin, page_height - 3*margin),  # Top-right
    #    (margin, margin + page_height/2),  # Bottom-left
    #    (page_width / 2 + 2*margin, margin + page_height/2),  # Bottom-right
    #]
    
    for page_index in range(0, len(puzzles), puzzles_per_page):
        # Get puzzles for this page
        page_puzzles = puzzles[page_index:page_index + puzzles_per_page]
        page_solutions = []
        for p in page_puzzles:
            page_solutions.append(p.solutions)

        for idx, (puzzle, puzzle_solutions) in enumerate(zip(page_puzzles, page_solutions)):

            x_start, y_start = quadrants[idx]
            rows, cols = puzzle.rows, puzzle.cols
            if idx == 0 or idx == 2:
                #w = (page_width-2*margin)/2
                w = (page_width-1*margin)/2
            else:
                w = page_width*2-4*margin

            #center_text(c, y_start+(margin/2), w, puzzle.title, font="Courier-Bold", size=12) 
            center_text(c, y_start+(margin/4), x_start, cell_size*cols, puzzle.title, font="Courier-Bold", size=12)         
            c.setFont("Courier", 8)
            # Adjust puzzle size and align to quadrant
            puzzle_width = cols * cell_size
            puzzle_height = rows * cell_size
            #x_start += (page_width / 2 - margin - puzzle_width) / 2
            #y_start += (page_height / 2 - margin - puzzle_height) / 2

            # Draw the puzzle grid
            for i, row in enumerate(puzzle.board):
                for j, letter in enumerate(row):
                    x = x_start + j * cell_size
                    y = y_start - i * cell_size
                    #c.rect(x, y, cell_size, cell_size, stroke=1, fill=0)
                    if letter.strip():
                        c.drawString(x + 3, y + 3, letter)
                        #c.drawString(x, y, letter)

            # Draw solutions
            for solution in puzzle_solutions:
                if solution:
                    start, direction, length = solution
                    x, y = start
                    dx, dy = direction

                    # Calculate start and end positions
                    x_puzzle_start = x_start + y * cell_size
                    y_puzzle_start = y_start - x * cell_size
                        
                    if direction == (0,1) or direction == (1,1): # Not sure why this is needed
                        y_puzzle_start += cell_size

                    x_end = x_puzzle_start + (length) * dx * cell_size
                    y_end = y_puzzle_start - (length) * dy * cell_size

                    # Draw an oval around the word
                    left = min(x_start, x_end) - cell_size / 2
                    right = max(x_start, x_end) + cell_size / 2
                    bottom = min(y_start, y_end) - cell_size / 2
                    top = max(y_start, y_end) + cell_size / 2
                    x1, y1, x2, y2 = x_puzzle_start, y_puzzle_start, x_end, y_end
                    draw_rounded_rectangle(c, direction, x1, y1, x2, y2)
        c.showPage()
        center_text(c, page_height - margin, 0, page_width, 'Solutions', font="Courier-Bold", size=16)

    c.save()


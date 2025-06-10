import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from word_search import *
from file_io import *
from generate_pdf import *
import math
import os
from options.options_globals import highlight_colors, ws_min_size, ws_max_size # background, foreground




"""
TODO: 
"""


class Word_Search_Manager:
    def __init__(self, frame):
        self.title = 'wordSearch'
        self.file_path = None
        self.prev_file = False
        self.frame = frame
        self.options_frame = None
        self.puzzle_dropdown = None

        self.word_list_frame = None
        self.word_list_text = None
        self.word_entry =  None

        self.puzzle_frame = None
        self.puzzle_text_area = None
        self.puzzle_title_label = None
        
        self.unplace_button = None
        self.remove_button = None
        self.place_button = None

        self.selected_puzzle = None
        self.show_solutions_var = None

        self.puzzles = []
        self.puzzle_index = -1
        self.selected_word = None
        self.start_row = None
        self.start_col = None
        self.direction = None
        self.prev_direction = None
        self.button_position = () #x,y

        self.generate_word_search_gui()

    def generate_word_search_gui(self):
        # Create a PanedWindow to split the GUI into left (options) and right (puzzle display)
        paned_window = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, sashwidth=10, sashrelief='raised')
        paned_window.pack(expand=1, fill="both")


        # Left Frame for options
        self.options_frame = ttk.Frame(paned_window, width=200)
        paned_window.add(self.options_frame)

        right_paned_window = tk.PanedWindow(paned_window, orient=tk.HORIZONTAL, sashwidth=10, sashrelief='raised')
        paned_window.add(right_paned_window)

        # Middle Frame for displaying the puzzle
        self.puzzle_frame = ttk.Frame(right_paned_window)
        right_paned_window.add(self.puzzle_frame)

        # Right Frame for displaying the word list
        self.word_list_frame = ttk.Frame(right_paned_window)
        right_paned_window.add(self.word_list_frame)

        self.generate_options_gui()
        self.generate_puzzle_area_gui()
        self.generate_word_list_gui()
        self.configure_highlights()

    def generate_options_gui(self):
        # ----------- Left Sidebar (Word Search Options) -----------
        options_title_label = tk.Label(self.options_frame, text="Options", font=("Helvetica", 16))
        options_title_label.pack(pady=10)

        # Frame to hold the Prev, Dropdown, and Next buttons
        nav_frame = tk.Frame(self.options_frame)
        nav_frame.pack(anchor="w", pady=10)

        # Prev button
        prev_button = tk.Button(nav_frame, text="<<", command=self.prev_puzzle)
        prev_button.pack(side="left", padx=5)

        # Dropdown for selecting puzzles
        self.selected_puzzle = tk.StringVar()
        self.selected_puzzle.set("Select Puzzle")

        self.puzzle_dropdown = ttk.OptionMenu(nav_frame, self.selected_puzzle, None)
        self.puzzle_dropdown.pack(side='left', padx=5)

        # Next button
        next_button = tk.Button(nav_frame, text=">>", command=self.next_puzzle)
        next_button.pack(side="left", padx=5)

        # Grid Size Label
        grid_size_label = tk.Label(self.options_frame, text="Grid Size:")
        grid_size_label.pack(anchor="w")
        grid_size_label2 = tk.Label(self.options_frame, text="Rows   x  Cols")
        grid_size_label2.pack(anchor="w", pady=0)

        # Frame to hold Row and Column size inputs next to each other
        size_frame = tk.Frame(self.options_frame)
        size_frame.pack(anchor="w", pady=(0,0))

            
        row_size_entry = tk.Entry(size_frame, width=5)
        row_size_entry.pack(side="left", padx=5, pady=0)


        column_size_entry = tk.Entry(size_frame, width=5)
        column_size_entry.pack(side="left", padx=5, pady=0)
        resize_button = tk.Button(size_frame, text='Resize', width=5, command=lambda: self.resize_grid(row_size_entry, column_size_entry))
        resize_button.pack(pady=10, padx=10, anchor='w')
        
        # Generate button
        generate_button = tk.Button(self.options_frame, text="Generate Word Search", command=lambda: self.generate(self.puzzle_index))
        generate_button.pack(pady=10, padx=10, anchor='w')

        # Clear button
        clear_button = tk.Button(self.options_frame, text="Clear Grid", command=self.clear_board)
        clear_button.pack(pady=10, padx=10, anchor='w')

        # Add Puzzle button
        add_button = tk.Button(self.options_frame, text="Add Puzzle", command=self.add_puzzle)
        add_button.pack(pady=10, padx=10, anchor='w')

        # Create a BooleanVar to store the state of the checkbox
        self.apply_mask_var = tk.BooleanVar()
        # Create the "Show Solutions" checkbox
        self.apply_mask_checkbox = tk.Checkbutton(
            self.options_frame,
            text="Apply Mask",
            variable=self.apply_mask_var,
            command=self.toggle_mask  # Trigger when the checkbox is clicked
        )

        # Create a BooleanVar to store the state of the checkbox
        self.show_solutions_var = tk.BooleanVar()
        # Create the "Show SOlutions" checkbox
        self.show_solutions_checkbox = tk.Checkbutton(
            self.options_frame,
            text="Show Solutions",
            variable=self.show_solutions_var,
            command=self.toggle_solutions  # Trigger when the checkbox is clicked
        )
        self.show_solutions_checkbox.pack(anchor="w")  # Align to the left of the frame
        self.apply_mask_checkbox.pack(anchor="w")  # Align to the left of the frame

        #apply_mask_checkbox.select()

    def add_puzzle(self):
        num = len(self.puzzles)
        self.puzzles.append(Word_Search(title=f'Word Search {num+1}', mode='gui'))
        
        self.puzzle_index = num
        self.display_current_puzzle()

    def resize_grid(self, row_entry, col_entry):
        try:
            row = int(row_entry.get().strip())
            col = int(col_entry.get().strip())
            print(row, col)
            # Maybe do more advanced size checking by finding the minimum grid to place all the words
            if row <= ws_max_size[0] and row >= ws_min_size[0] and col <= ws_max_size[1] and col >= ws_min_size[1]:
                print('yip')
                if self.puzzle_index == -1:
                    self.add_puzzle()
                self.puzzles[self.puzzle_index].resize(row, col)
                print('yop')
                self.display_current_puzzle()
        
        except:
            print('Resize: Invalid Input')


    def generate(self, index):
        puzzle = self.puzzles[index]
        for i, word in enumerate(puzzle.words):
            if not puzzle.solutions[i]:
                if not self.puzzles[index].place_word_auto(word):
                    print(f'No valid location to place \'{word}\'')
                    self.clear_board(index)
                    self.display_current_puzzle()
                    return False
        self.puzzles[index].fill()
        self.display_current_puzzle()
        return True

    def clear_board(self, index=-1):
        if index == -1:
            index = self.puzzle_index
        self.puzzles[index].clear_board()
        self.display_current_puzzle()

    def generate_puzzle_area_gui(self):
        # ----------- Right Puzzle Display Area (Top) -----------
        # Title label for the puzzle
        self.puzzle_title_label = tk.Label(self.puzzle_frame, text="Puzzle 1", font=("Helvetica", 16), cursor='hand2')
        self.puzzle_title_label.pack(pady=10)
        self.puzzle_title_label.bind("<Button-1>", self.update_title)
        # Add vertical and horizontal scrollbars
        scroll_y = tk.Scrollbar(self.puzzle_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = tk.Scrollbar(self.puzzle_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        # Text area to display the word search
        self.puzzle_text_area = tk.Text(self.puzzle_frame, height=20, width=40, wrap='none', yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.puzzle_text_area.pack(pady=10, padx=20)
        self.puzzle_text_area.config(state=tk.DISABLED)
        self.puzzle_text_area.bind("<Enter>", self.puzzle_text_area.config(cursor="arrow"))

        self.puzzle_text_area.bind("<Button-1>", self.on_grid_click)

        # Attach scrollbars to the text area
        scroll_y.config(command=self.puzzle_text_area.yview)
        scroll_x.config(command=self.puzzle_text_area.xview)

    def update_title(self, event):
        
        self.title_x, self.title_y = self.puzzle_title_label.winfo_x(), self.puzzle_title_label.winfo_y()
        self.title_width, self.title_height = self.puzzle_title_label.winfo_width(), self.puzzle_title_label.winfo_height()
        if self.puzzle_index == -1:
            self.add_puzzle()
        
        self.puzzle_title_label.config(text='')
        self.title_entry = tk.Entry(self.puzzle_frame)
        self.title_entry.place(x=self.title_x, y=self.title_y, width=self.title_width, height=self.title_height)
        self.title_entry.focus()

        self.title_entry.bind("<Return>", self.finish_update_title)
        self.title_entry.bind("<FocusOut>", self.finish_update_title)

    def finish_update_title(self, event):
        self.puzzles[self.puzzle_index].title = self.title_entry.get().strip()
        self.puzzle_title_label.config(text=self.puzzles[self.puzzle_index].title, fg='black')
        self.title_entry.place_forget()
        self.title_entry.destroy()
        self.display_current_puzzle()

    def generate_word_list_gui(self):
        # ----------- Right Word List Display Area (Bottom) -----------
        # Title label for the Words
        word_title_label = tk.Label(self.word_list_frame, text="Words", font=("Helvetica", 16))
        word_title_label.pack(pady=10)

        # Text area to display the word list
        self.word_list_text = tk.Text(self.word_list_frame, height=10, width=40)
        self.word_list_text.pack(pady=10, padx=10)
        self.word_list_text.config(state=tk.DISABLED)

        # Frame to hold the word entry and add button side by side
        word_input_frame = tk.Frame(self.word_list_frame)
        word_input_frame.pack(pady=5, padx=10, anchor='w')

        # Entry box for the word
        self.word_entry = tk.Entry(word_input_frame)
        self.word_entry.pack(side=tk.LEFT)

        # Add Word button, placed directly to the right of the word_entry
        add_word_button = tk.Button(word_input_frame, text="Add Word", command=self.add_word)
        add_word_button.pack(side=tk.LEFT, padx=5)


        # GUI setup for the remove button
        self.remove_button = tk.Button(self.word_list_frame, text="-", command=None, width=2, height=1, 
                                font=("Helvetica", 8), padx=1, pady=1, bd=1)
        self.remove_button.place_forget()  # Hide initially

        self.place_button = tk.Button(self.word_list_frame, text="Place", command=self.place_selected_word, width=6, height=1, 
                                font=("Helvetica", 8), padx=1, pady=1, bd=1)
        self.place_button.place_forget()  # Hide initially

        self.unplace_button = tk.Button(self.word_list_frame, text="Unplace", command=self.unplace_selected_word, width=6, height=1, 
                                font=("Helvetica", 8), padx=1, pady=1, bd=1)
        self.unplace_button.place_forget()  # Hide initially

        # Bind the word list click event to trigger word selection
        self.word_list_text.bind("<Button-1>", self.on_word_click)
        self.word_list_text.bind("<Enter>", self.word_list_text.config(cursor="arrow"))

        self.size_label = tk.Label(self.word_list_frame, text='', font=("Helvetica", 12))
        self.size_label.pack(pady=10)
    
    def display_size(self):
        label = ''
        if self.puzzle_index != -1:
            label = f'Size: {self.puzzles[self.puzzle_index].rows} x {self.puzzles[self.puzzle_index].cols}'
        
        self.size_label.config(text=label)
        
    
    def configure_highlights(self, colors=highlight_colors):
        for color in range(len(colors)):
            self.word_list_text.tag_configure("highlight"+str(color), background=colors[color][0], foreground=colors[color][1])
            self.puzzle_text_area.tag_configure("highlight"+str(color), background=colors[color][0], foreground=colors[color][1])
    

    def display_word_search(self, grid, text_widget):
        text_widget.delete(1.0, tk.END) # Clear the text area
        for row in grid:
            text_widget.insert(tk.END, ' '.join(row) + '\n')

    def display_word_list(self, words, highlight_answers=False):
        self.word_list_text.config(state=tk.NORMAL)
        self.word_list_text.delete(1.0, tk.END)
        self.word_list_text.tag_remove("highlight", "1.0", "end")
        for line_number, word in enumerate(words, start=1):
            word_start_index = f"{line_number}.0"
            word_end_index = f"{line_number}.{len(word)}"
            self.word_list_text.insert(tk.END, word + '\n')
            if highlight_answers:
                index = self.puzzles[self.puzzle_index].words.index(word)
                if self.puzzles[self.puzzle_index].solutions[index]:
                    color = index % len(highlight_colors)          
                    self.word_list_text.tag_add("highlight"+str(color), word_start_index, word_end_index)

            elif word == self.selected_word:
                index = self.puzzles[self.puzzle_index].words.index(word)
                color = index % len(highlight_colors)
                #word_list_text.tag_configure("highlight", background=highlight_colors[color][0], foreground=highlight_colors[color][1])
                self.word_list_text.tag_add("highlight"+str(color), word_start_index, word_end_index)

        self.word_list_text.config(state=tk.DISABLED)  # Make it read-only again
        self.display_size()

    # Function to display the current puzzle
    def display_current_puzzle(self):
        if self.puzzles:
            puzzle = self.puzzles[self.puzzle_index]
            if puzzle.mask_bool:
                self.apply_mask_checkbox.select()
            r = puzzle.rows
            c = puzzle.cols
            #self.puzzle_text_area.delete(1.0, tk.END)  # Clear the text area
            self.puzzle_title_label.config(text=self.puzzles[self.puzzle_index].title)
            self.puzzle_text_area.config(state=tk.NORMAL, height=r, width=c*2)
            self.display_word_search(self.puzzles[self.puzzle_index].board, self.puzzle_text_area)  # Display the current puzzle
            self.display_word_list(self.puzzles[self.puzzle_index].words)
            self.highlight()
            self.update_dropdown()
            self.puzzle_text_area.config(state=tk.DISABLED)

    # Function to update dropdown menu options
    def update_dropdown(self):
        self.puzzle_dropdown['menu'].delete(0, 'end')  # Clear existing menu options
        for i in range(len(self.puzzles)):
            self.puzzle_dropdown['menu'].add_command(label=self.puzzles[i].title, command=lambda index=i: self.select_puzzle(index))
        self.selected_puzzle.set(self.puzzles[self.puzzle_index].title)

    # Function to handle puzzle selection from dropdown
    def select_puzzle(self, index):
        self.puzzle_index = index
        self.selected_word = None
        self.remove_button.place_forget()
        self.place_button.place_forget()
        self.unplace_button.place_forget()
        self.show_solutions_checkbox.deselect()
        self.apply_mask_checkbox.deselect()
        self.display_current_puzzle()

        

    # Function to go to the previous puzzle
    def prev_puzzle(self):
        if self.puzzle_index > 0:
            self.puzzle_index -= 1
            self.selected_word = None
            self.remove_button.place_forget()
            self.place_button.place_forget()
            self.unplace_button.place_forget()
            self.show_solutions_checkbox.deselect()
            self.apply_mask_checkbox.deselect()
            self.display_current_puzzle()

            

    # Function to go to the next puzzle
    def next_puzzle(self):
        if self.puzzle_index < len(self.puzzles) - 1:
            self.puzzle_index += 1
            self.selected_word = None
            self.remove_button.place_forget()
            self.place_button.place_forget()
            self.unplace_button.place_forget()
            self.show_solutions_checkbox.deselect()
            self.apply_mask_checkbox.deselect()
            self.display_current_puzzle()


            
            print('selected', self.selected_word)

    def add_word(self):
        word = self.word_entry.get().strip().upper()
        if self.puzzle_index == -1:
            self.add_puzzle()
        if word and word not in self.puzzles[self.puzzle_index].words:
            self.puzzles[self.puzzle_index].add_word(word)
            self.display_word_list(self.puzzles[self.puzzle_index].words)  # Update the word list display
            self.word_entry.delete(0, tk.END)  # Clear the entry boxx

    # Function to remove the selected word from the word list
    def remove_word(self, word):
        self.unplace_selected_word()
        self.remove_button.place_forget()  # Hide the remove button after word is removed
        self.place_button.place_forget()

        self.puzzles[self.puzzle_index].remove_word(word)
        self.display_word_list(self.puzzles[self.puzzle_index].words)  # Update the word list display
        #word_list_text.tag_remove('highlight', '1.0', tk.END)  # Remove highlighting
        self.remove_highlight()

    def place_selected_word(self):
        # Example behavior: You can define your own action when the word is "placed"
        #place_button.config(text='Unplace', command=lambda: unplace_selected_word)
        self.place_button.place_forget()
        self.unplace_button.place(x=self.button_position[0], y=self.button_position[1])

    def unplace_selected_word(self):
        self.puzzle_text_area.unbind("<Motion>")
        #place_button.place_forget()
        #remove_button.place_forget()
        #place_button.config(text='Place', command=lambda: place_selected_word)
        self.unplace_button.place_forget()
        self.place_button.place(x=self.button_position[0], y=self.button_position[1])
        index = self.puzzles[self.puzzle_index].words.index(self.selected_word)
        if self.puzzles[self.puzzle_index].solutions[index]: # remove solution
            self.puzzles[self.puzzle_index].remove_solution(index)
        elif self.start_row: # clear start of temp placement
            self.puzzles[self.puzzle_index].board[self.start_row][self.start_col] = '-'
            self.clear_temporary_placement(override=True)

        self.reset_globals()
        self.display_current_puzzle()
        self.puzzle_text_area.unbind("<Motion>")
        self.puzzle_text_area.bind("<Button-1>", self.on_grid_click)


    # Event handler for word selection in the word list
    def on_word_click(self, event):
        #reset_globals()
        if self.start_row:
            self.unplace_selected_word()
            self.reset_globals()
        try:
            self.selected_word = None
            clicked_word = None
            # Get the index of the clicked position in the word list
            index = self.word_list_text.index("@%s,%s" % (event.x, event.y))
            # Get the line number
            line = int(index.split('.')[0])
            line_start = f"{line}.0"
            line_end = f"{line}.end"

            # Get the entire line text
            line_text = self.word_list_text.get(line_start, line_end).strip()

            mouse_index = int(index.split('.')[1])   
            if mouse_index < len(line_text):
                clicked_word = line_text

            # If a word was clicked, set it as selected
            if clicked_word:
                
                self.selected_word = clicked_word  # Set the selected word
                # Highlight the selected word
                self.remove_highlight()
                index = self.puzzles[self.puzzle_index].words.index(self.selected_word)
                color = index % len(highlight_colors)
                self.word_list_text.tag_add("highlight"+str(color), line_start, line_end)
                
                self.highlight()           

                # Get the position of the clicked word for button placement
                bbox = self.word_list_text.bbox(line_start)
                if bbox:
                    _, y, _, height = bbox
                    self.word_list_text.update_idletasks()  # Ensure the word_list_text updates dimensions
                    right_edge = self.word_list_text.winfo_width()  # Get the width of the word list text area
                    adjusted_y = y + self.word_list_text.winfo_rooty() - self.word_list_frame.winfo_rooty()

                    self.remove_button.config(command=lambda: self.remove_word(clicked_word))
                    self.remove_button.place(x=right_edge - 70, y=adjusted_y)  # Place remove button to the right side of the word list
                    
                    self.button_position = [right_edge-40, adjusted_y]
                    # Show place button to the right of the remove button
                    if self.puzzles[self.puzzle_index].solutions[self.puzzles[self.puzzle_index].words.index(clicked_word)]:
                        #place_button.config(text='Unplace', command=lambda: unplace_selected_word())
                        self.place_button.place_forget()
                        self.unplace_button.place(x=right_edge-40, y=adjusted_y)
                    else:
                        #place_button.config(text='Place', command=lambda: place_selected_word())
                        self.unplace_button.place_forget()
                        self.place_button.place(x=right_edge-40, y=adjusted_y)
                    # Adjusted position for "Place" button
                    
                    
                self.display_current_puzzle()
        except tk.TclError:
            pass

    # Function to handle selecting a cell in the puzzle grid
    def on_grid_click(self, event):
        puzzle_grid = self.puzzles[self.puzzle_index].board
        index = self.puzzle_text_area.index("@%s,%s" % (event.x, event.y))
        row, col = map(int, index.split('.'))
        col = math.ceil(col / 2)
        row -=1 # IDK but it fixes improper row number
        self.place_button.forget()
        self.unplace_button.place(x=self.button_position[0], y=self.button_position[1])

        if self.selected_word:
            first_letter = self.selected_word[0]

            # Check if the clicked position is valid
            if puzzle_grid[row][col] == '-' or puzzle_grid[row][col] == first_letter:
                self.start_row, self.start_col = row, col
                self.puzzle_text_area.bind("<Motion>", self.visualize_word_placement)
                

    def visualize_word_placement(self, event):
        self.puzzle_text_area.bind("<Button-1>", self.finalize_word_placement)
        try:
            # Get the index of the current mouse position
            self.prev_direction = self.direction
            index = self.puzzle_text_area.index("@%s,%s" % (event.x, event.y))
            hover_row, hover_col = map(int, index.split('.'))
            hover_col = math.ceil(hover_col / 2)
            hover_row -=1 # IDK but it fixes improper row number
            # Determine the direction based on the relative position of the hover
            delta_row = hover_row - self.start_row
            delta_col = hover_col - self.start_col
            
            self.direction = None
            if delta_row == 0 and delta_col > 0: # right
                self.direction = (1,0)
            elif delta_row == 0 and delta_col < 0: # left
                self.direction = (-1,0)
            elif delta_row > 0 and delta_col == 0: # down
                self.direction = (0,1)
            elif delta_row < 0 and delta_col == 0: # up
                self.direction = (0,-1)
            elif delta_row < 0 and delta_col > 0: # ur
                self.direction = (1,-1)
            elif delta_row < 0 and delta_col < 0: # ul
                self.direction = (-1,-1)
            elif delta_row > 0 and delta_col > 0: # dr
                self.direction = (1,1)
            elif delta_row > 0 and delta_col < 0: # dl
                self.direction = (-1,1)
            
            # Clear previous visualization
            self.clear_temporary_placement()

            # Temporarily place the word in the calculated direction
            if self.direction:
                self.place_word_temporarily(self.start_row, self.start_col, self.direction)
        
        except tk.TclError:
            print('error, visualize_word_placement')   

    # Function to clear temporary word placement
    def clear_temporary_placement(self, override=False):
        if override or (self.prev_direction and self.prev_direction != self.direction):
            row = self.start_row + self.prev_direction[1]
            col = self.start_col + self.prev_direction[0]
            for ii in range(len(self.selected_word)-1):
                if self.selected_word[ii+1] == ' ':
                    continue
                if row < 0 or row >= self.puzzles[self.puzzle_index].rows or \
                    col < 0 or col >= self.puzzles[self.puzzle_index].cols:
                    break
                if self.puzzles[self.puzzle_index].board[row][col] == self.selected_word[ii+1]:
                    self.puzzles[self.puzzle_index].board[row][col] = '-'
                    row += self.prev_direction[1]
                    col += self.prev_direction[0]
                else:
                    break
            self.display_current_puzzle()  # Update the displayed grid

    # Function to temporarily place the word in the specified direction
    def place_word_temporarily(self, row, col, direction):
        #puzzle_text_area.tag_remove("highlight", "1.0", "end")
        if self.puzzles[self.puzzle_index].test_candidate(self.selected_word, direction, row, col):
            self.puzzles[self.puzzle_index].place_word(self.selected_word, row, col, direction) 
        self.display_current_puzzle()

    def highlight(self):
        if not self.direction and self.selected_word:
            index = self.puzzles[self.puzzle_index].words.index(self.selected_word)
            solution = self.puzzles[self.puzzle_index].solutions[index]
            if solution:
                self.highlight_helper(self.selected_word, solution)
        elif not self.direction:
            return
        elif self.puzzles[self.puzzle_index].test_candidate(self.selected_word, self.direction, self.start_row, self.start_col):
            solution = [(self.start_row, self.start_col), self.direction, len(self.selected_word)]
            self.highlight_helper(self.selected_word, solution)

    def highlight_helper(self, word, solution):
        row_i = solution[0][0]
        col_i = solution[0][1]
        for ii in range(len(word)):
            if word[ii] == ' ':
                continue
            #col_i = solution[0][1] + ii*solution[1][0]
            start_index = f"{row_i+1}.{col_i * 2}"
            end_index = f"{row_i+1}.{col_i * 2 + 1}"
            index = self.puzzles[self.puzzle_index].words.index(word)
            color = index % len(highlight_colors)
            #puzzle_text_area.tag_config("highlight", background=highlight_colors[color][0], foreground=highlight_colors[color][1])
            self.puzzle_text_area.tag_add("highlight"+str(color), start_index, end_index)
            row_i  += solution[1][1]
            col_i += solution[1][0]

    def reset_globals(self):
        self.direction = None
        self.prev_direction = None
        #selected_word = None
        self.start_row = None
        self.start_col = None

    # Event handler to finalize the word placement
    def finalize_word_placement(self, event):
        if self.puzzles[self.puzzle_index].test_candidate(self.selected_word, self.direction, self.start_row, self.start_col):
            index = self.puzzles[self.puzzle_index].words.index(self.selected_word)
            self.puzzles[self.puzzle_index].solutions[index] = [(self.start_row, self.start_col), self.direction, len(self.selected_word)]
            self.puzzle_text_area.unbind("<Motion>")  # Unbind the motion event after placement
            self.puzzle_text_area.bind("<Button-1>", self.on_grid_click)
            self.place_button.place_forget()
            self.remove_button.place_forget()
            self.unplace_button.place_forget()
            
            self.reset_globals()
            self.selected_word = None
            self.display_current_puzzle()

    def toggle_solutions(self):
        # not highlighing word_list
        if self.show_solutions_var.get():
            self.display_word_list(self.puzzles[self.puzzle_index].words, True)
            for index in range(len(self.puzzles[self.puzzle_index].words)):
                solution = self.puzzles[self.puzzle_index].solutions[index]
                if solution:
                    self.highlight_helper(self.puzzles[self.puzzle_index].words[index], solution)
        else:
            #puzzle_text_area.tag_remove("highlight", "1.0", "end")
            #word_list_text.tag_remove("highlight", "1.0", "end")
            self.remove_highlight()
    
    def toggle_mask(self):
        puzzle = self.puzzles[self.puzzle_index]
        r = puzzle.rows
        c = puzzle.cols
        if self.apply_mask_var.get():
            self.puzzles[self.puzzle_index].mask_bool = True
        else:
            self.puzzles[self.puzzle_index].mask_bool = False

        self.puzzles[self.puzzle_index].resize(r,c)
        self.display_current_puzzle()


    def remove_highlight(self):
        for ii in range(len(highlight_colors)):
            self.word_list_text.tag_remove("highlight"+str(ii), "1.0", "end")
            self.puzzle_text_area.tag_remove("highlight"+str(ii), "1.0", "end")

    def generate_all(self):
        fail = []
        for i in range(len(self.puzzles)):
            if not self.puzzles[i].complete:
                f = self.generate(i)
                if not f:
                    fail.append(i)

        print('Failed to Generate:')
        for i in fail:
            print(self.puzzles[i].title)

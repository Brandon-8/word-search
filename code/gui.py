import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from word_search import *
from file_io import *
from generate_pdf import *
from ws_manager import *
from options.options import ws_adv_options, export_options

"""
RUN THIS FILE
"""
"""
TODO:
track changes to not ask to save everytime you close

"""
class Puzzle_Generator:
    def __init__(self, file_path= None):
        # Main GUI setup
        self.root = tk.Tk()
        #root.geometry("800x500")
        self.root.title("Puzzle Generator")
        #self.puzzle_manager = None
        

        # Create a Notebook (Tabbed interface)
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=1, fill="both")

        # Word Search Tab
        self.word_search_frame = ttk.Frame(notebook)
        notebook.add(self.word_search_frame, text="Word Search")

        # Sudoku Tab (Placeholder for now)
        self.sudoku_frame = ttk.Frame(notebook)
        notebook.add(self.sudoku_frame, text="Sudoku")
        place_text1 = tk.Label(self.sudoku_frame, text='PlaceHolder: Not Implemented')
        place_text1.pack(pady=10)

        # Crossword Tab (Placeholder for now)
        self.crossword_frame = ttk.Frame(notebook)
        notebook.add(self.crossword_frame, text="Crossword")
        place_text2 = tk.Label(self.crossword_frame, text='PlaceHolder: Not Implemented')
        place_text2.pack(pady=10)

        selected_tab = notebook.tab(notebook.select(), "text")
        self.puzzle_manager = self.get_puzzle_type(selected_tab)


        self.modify_menus()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
        if file_path:
            print(file_path)
            load_word_search(self.puzzle_manager, file_path)
            self.puzzle_manager.display_current_puzzle()
    
        #Keyboard Shorcuts
        self.root.bind("<Control-o>", lambda event: open_file(self.puzzle_manager))
        self.root.bind("<Control-S>", lambda event: save_as(self.puzzle_manager))
        self.root.bind("<Control-s>", lambda event: save_file(self.puzzle_manager))
        self.root.bind("<Control-q>", lambda event: self.close())
        self.root.bind("<Control-g>", lambda event: self.puzzle_manager.generate(self.puzzle_manager.puzzle_index))
        self.root.bind("<Control-G>", lambda event: self.puzzle_manager.generate_all())
   
    def get_puzzle_type(self, selected_tab):
        if selected_tab == 'Word Search':
            return Word_Search_Manager(self.word_search_frame)

    def modify_menus(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.root)

        # Create "File" menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command= lambda: open_file(self.puzzle_manager))
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command= lambda: save_file(self.puzzle_manager))
        file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command= lambda: save_file(self.puzzle_manager))
        file_menu.add_command(label="Export to PDF", command= lambda: export_options(self.root, self.puzzle_manager))
        #file_menu.add_command(label="Export All", command= lambda: export_all(self.puzzle_manager))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.close)
        
        menu_bar.add_cascade(label="File", menu=file_menu)

        
        # Create "Edit" menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        ws_edit_menu = tk.Menu(edit_menu, tearoff=0)
        ws_edit_menu.add_command(label='Generate All', accelerator="Ctrl+Shift+G", command=self.puzzle_manager.generate_all)
        ws_edit_menu.add_command(label='Open Manager (NA)')
        edit_menu.add_cascade(label='Word Search', menu=ws_edit_menu)
        
        
        #edit_menu.add_command(label="Undo")
        #edit_menu.add_command(label="Redo")
        #edit_menu.add_separator()
        #edit_menu.add_command(label="Cut")
        #edit_menu.add_command(label="Copy")
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Word Search", command= lambda: ws_adv_options(self.root, self.puzzle_manager))
        options_menu.add_command(label="Sudoku (NA)")
        options_menu.add_command(label="Crossword (NA)")
        menu_bar.add_cascade(label="Options", menu=options_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='Help', command=self.open_help)
        help_menu.add_command(label='Keyboard Shortcuts', command=self.open_help_shortcuts)
        help_menu.add_command(label='Bug Reports', command=self.open_bug_report)
        menu_bar.add_cascade(label='Help', menu=help_menu)

        # Display the menu
        self.root.config(menu=menu_bar)

    def close(self):
        file_path = self.puzzle_manager.file_path
        if messagebox.askyesno("Save Puzzle", "Do you want to save the puzzle before exiting?"):
            if not self.puzzle_manager.prev_file:
                file_path = filedialog.asksaveasfilename(defaultextension='.txt', 
                                                        filetypes=[("Text files", "*.txt")])
            save_word_searches(file_path, self.puzzle_manager.puzzles) 
        self.root.destroy()

    def open_bug_report(self):
        if os.path.exists('bug_report.txt'):
            subprocess.Popen(["notepad.exe", 'bug_report.txt'])
    
    def open_help_shortcuts(self):
        try:
            # Open the help.txt file and read content
            with open("shortcuts.txt", "r") as file:
                help_content = file.read()
            
            # Create a new popup window to display the help content
            help_window = tk.Toplevel(self.root)
            help_window.title("Keyboard Shortcuts")
            help_text = tk.Text(help_window, wrap="word", padx=10, pady=10)
            help_text.insert("1.0", help_content)
            help_text.config(state="disabled")  # Make text read-only
            help_text.pack(expand=True, fill="both")
        except FileNotFoundError:
            messagebox.showerror("Error", "The shortcuts.txt file could not be found.")  

    def open_help(self):
        try:
            # Open the help.txt file and read content
            with open("help.txt", "r") as file:
                help_content = file.read()
            
            # Create a new popup window to display the help content
            help_window = tk.Toplevel(self.root)
            help_window.title("Help")
            help_text = tk.Text(help_window, wrap="word", padx=10, pady=10)
            help_text.insert("1.0", help_content)
            help_text.config(state="disabled")  # Make text read-only
            help_text.pack(expand=True, fill="both")
        except FileNotFoundError:
            messagebox.showerror("Error", "The help.txt file could not be found.")        

if __name__ == '__main__':
    # auto load test 
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    app = Puzzle_Generator(file_path=file_path)
    app.root.mainloop()

    #load_word_search(app.puzzle_manager, 'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\saved\\states.txt')
    #create_word_search_pdf(app.puzzle_manager.puzzles,'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\states.pdf')
    #app.root.destroy()
    #os.startfile('C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\test_solutions.pdf')
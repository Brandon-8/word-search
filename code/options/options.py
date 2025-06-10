import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from options.option_methods import center_popup
from options.color_grid_widget import ColorGridWidget
from file_io import export



"""
TODO:
Export:
    export only certain pages
option:
    change alphabet
    change fill distribution
    edit mask
    directly edit grid (Here or ws_manager?)
"""

# Only built for one puzzle type, will have to redo
# for word search + sudoku in same program instance
# background, foreground
  
def ws_adv_options(root, ws_manager):
    ws_options = tk.Toplevel()
    ws_options.title("Word Search Options")
    width, height = 300, 200
    
    # Set the geometry of the popup to center it on the root window
    pos = center_popup(root, width, height)
    ws_options.geometry(pos)
    
    ws_options.grab_set()
    notebook = ttk.Notebook(ws_options)
    notebook.pack(expand=1, fill='both')
    ws_display_frame = ttk.Frame(notebook)
    notebook.add(ws_display_frame, text='Display')

    ws_display_options(ws_display_frame, root, ws_manager)
   

def ws_display_options(frame, root, ws_manager):
    color = tk.Button(frame, text='Highlight Color Options', command=lambda: ColorGridWidget(root, ws_manager))
    color.pack(side='left')


def export_options(root, manager):
    export_options = tk.Toplevel()
    export_options.title("Export Options")
    width, height = 650, 600
    pos = center_popup(root, width, height)
    export_options.geometry(pos)
    export_options.grab_set()
    title = tk.Label(export_options, text='Export Options', font=("Arial", 12, "bold"))
    title.grid(pady=10)
    
    #paned_window = tk.PanedWindow(export_options, orient=tk.HORIZONTAL)
    #range = ttk.Frame(paned_window, width=200)
    #paned_window.add(range)
    #sol_options = ttk.Frame(paned_window, width=200)
    #paned_window.add(sol_options)
        
    export_selector = ExportFileSelector(export_options, title= manager.title)
    export_selector.grid(padx=10, pady=10)

    checkbox_frame = tk.Frame(export_options)
    checkbox_frame.grid(padx=20, pady=20)

    which_puzzles = CheckBoxes(
        checkbox_frame,
        #range,
        options=["All", "Current", "Pages"],
        default="All",
        title='Range'
    )
    which_puzzles.grid(row=0, column=0, padx=10, sticky="nw")

    sols = CheckBoxes(
        checkbox_frame,
        options=['None', 'Same File', 'Separate File'],
        default= 'None',
        title='Export Solutions'
    )
    sols.grid(row=0, column=1, padx=10, sticky="nw")
    

    
    size_label = tk.Label(checkbox_frame, text="Size (in):")
    size_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

    export_size = tk.StringVar(value='6 x 9')
    size_options = ['6 x 9', '8.5 x 11']
    size_dropdown = ttk.OptionMenu(checkbox_frame, export_size, size_options[0], *size_options)
    size_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    view_bool = tk.BooleanVar()
    view_pdf_after_export_checkbox = tk.Checkbutton(
            export_options,
            text="View PDF after export",
            variable=view_bool,
        )
    view_pdf_after_export_checkbox.grid()

    bottom_frame = tk.Frame(export_options)
    bottom_frame.grid(pady=5, padx=20)

    export_button = tk.Button(bottom_frame, text='Export', anchor='e', 
                              command=lambda: export(export_options, manager, 
                                             which_puzzles.get_selected(), 
                                             sols.get_selected(), 
                                             export_selector.file_path.get(),
                                             sols.entry_field.get(),
                                             export_size.get(),
                                             view=view_bool))
    export_button.grid(row=0, column=0, padx=10, sticky='e')

    cancel_button = tk.Button(bottom_frame, text='Cancel', anchor='e', command=lambda: export_options.destroy())
    cancel_button.grid(row=0, column=1, padx=10, sticky='e')

class ExportFileSelector(tk.Frame):
    def __init__(self, master=None, title='export'):
        super().__init__(master)
        self.title = title
        default_path = f'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\{self.title}.pdf'
        self.grid_columnconfigure(1, weight=1)  # Make the entry field expand
        self.file_path = tk.StringVar(value=default_path)  # Variable to store selected path

        # Label for the field
        self.label = tk.Label(self, text="Export to:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Entry field for displaying the folder path
        self.entry = tk.Entry(self, textvariable=self.file_path)
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Button to open folder selection dialog
        self.browse_button = tk.Button(self, text="Browse", command=self.select_folder)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

    def select_folder(self):
        """Open a folder selection dialog and update the entry field."""
        folder = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], 
                                             initialfile=self.title,
                                             initialdir='..\\word searches',
                                             title='Save as PDF')
        if folder:  # If a folder was selected
            self.file_path.set(folder)

class CheckBoxes(tk.Frame):
    def __init__(self, master=None, options=None, default=None, title=''):
        super().__init__(master)
        self.variable = tk.StringVar(value=default)
        self.entry_field = None
        self.browse_button = None
        self.text = tk.StringVar()
        self.title = tk.Label(self, text=title, font=("Arial", 12, "bold"))
        self.title.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Align title to the left

        # Create the exclusive checkboxes (radio buttons styled as circles)
        for idx, option in enumerate(options):
            rb = tk.Radiobutton(
                self,
                text=option,
                variable=self.variable,
                value=option,
                indicatoron=True,
                width=10,  # Adjust width as needed
                command=self.update_entry_state,
                justify='left',
                anchor='w'
                #relief="groove"  # Make them visually distinct
            )
            rb.grid(row=idx+1, column=0, padx=5, pady=5, sticky="w")
            if option in ['Pages', 'Separate File']:
                self.entry_field = tk.Entry(self, state="disabled", textvariable=self.text)  # Initially disabled
                self.entry_field.grid(row=idx+1, column=1, padx=5, pady=5, sticky="w")
                if option == 'Separate File':
                    self.browse_button = tk.Button(self, text="Browse", command=self.select_folder, state='disabled')
                    self.browse_button.grid(row=idx+1, column=2, padx=5, pady=5)

    def update_entry_state(self):
        """Enable or disable the entry field based on the selected option."""
        if self.variable.get() in ["Pages", 'Separate File']:
            self.entry_field.config(state="normal")
            if self.browse_button:
                self.browse_button.config(state='normal')
        else:
            self.entry_field.delete(0, tk.END)  # Clear the entry field
            self.entry_field.config(state="disabled")
            if self.browse_button:
                self.browse_button.config(state='disabled')

    def get_selected(self):
        """Return the currently selected option."""
        if self.variable.get() in ['Pages', 'Separate File']:
            self.update_entry_state()
            return (self.variable.get(), self.entry_field.get())
        return self.variable.get()
    
    def select_folder(self):
        """Open a folder selection dialog and update the entry field."""
        folder = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], 
                                             initialfile='solutions',
                                             initialdir='..\\word searches',
                                             title='Save Solutions s PDF')
        if folder:  # If a folder was selected
            self.text.set(folder)

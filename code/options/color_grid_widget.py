import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from options.option_methods import center_popup
from options.options_globals import highlight_colors, default_highlight_colors

"""
TODO:
"""
class ColorGridWidget:
    def __init__(self, org_root, ws_manager):
        self.root = tk.Toplevel()
        self.org_root = org_root
        self.ws_manager = ws_manager
        self.root.title("Highlight Color Options")
        self.width, self.height = 600, 500

        self.colors = highlight_colors
    
        # Set the geometry of the popup to center it on the root window
        pos = center_popup(self.org_root, self.width, self.height)
        self.root.geometry(pos)
        # Frame for the color grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=20, padx=20)

        self.header()

        self.reset(highlight_colors)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        # Button to add a new row
        self.add_row_button = tk.Button(button_frame, text="Add Color", command=self.add_row)
        self.add_row_button.pack(side='left', padx=5)
        # Button to remove row
        self.add_row_button = tk.Button(button_frame, text="Remove Color", command=self.remove_row)
        self.add_row_button.pack(side='left', padx=5)
        # Reset Button
        self.reset_button = tk.Button(button_frame, text="Reset to Default", command=self.reset)
        self.reset_button.pack(side='left', padx=5)
       
        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', pady=10)

        # Bottom Button Frame
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill='x', pady=5, padx=20)

        # Help Button
        self.help_button = tk.Button(bottom_frame, text="Help", command=self.help)
        self.help_button.pack(side="left")   

        # Cancel Button
        self.cancel_button = tk.Button(bottom_frame, text="Cancel", command=self.cancel)
        self.cancel_button.pack(side="right", padx=5) 

         # OK Button
        self.ok_button = tk.Button(bottom_frame, text="OK", command=self.exit)
        self.ok_button.pack(side="right", padx=5)

        # Apply Button
        self.apply_button = tk.Button(bottom_frame, text="Apply", command=self.save_color_config)
        self.apply_button.pack(side="right", padx=5)


        
        self.root.grab_set()

    def add_row(self, bg='white', fg='black'):
        row_num = len(self.rows) + 1

        # Number label
        num_label = tk.Label(self.grid_frame, text=str(row_num))
        num_label.grid(row=row_num, column=0, padx=5, pady=5)

        # Foreground color label
        fg_color_label = tk.Label(self.grid_frame, text="    ", bg=fg, relief="solid")
        fg_color_label.grid(row=row_num, column=1, padx=5, pady=5)
        fg_color_label.bind("<Button-1>", lambda event: self.change_color(fg_color_label))

        # Background color label
        bg_color_label = tk.Label(self.grid_frame, text="    ", bg=bg, relief="solid")
        bg_color_label.grid(row=row_num, column=2, padx=5, pady=5)
        bg_color_label.bind("<Button-1>", lambda event: self.change_color(bg_color_label))

        # Example text label
        example_text_label = tk.Label(self.grid_frame, text="Example Text", fg=fg, bg=bg, width=20)
        example_text_label.grid(row=row_num, column=3, padx=5, pady=5)

        # Move up and down buttons
        action_frame = tk.Frame(self.grid_frame)
        action_frame.grid(row=row_num, column=4)

        up_button = tk.Button(action_frame, text="↑", command=lambda: self.move_row_up(row_num - 1))
        up_button.grid(row=row_num - 1, column=4)

        down_button = tk.Button(action_frame, text="↓", command=lambda: self.move_row_down(row_num - 1))
        down_button.grid(row=row_num - 1, column=4, padx=(35, 5))      
        # Store row components in a list for easy access
        self.rows.append((num_label, fg_color_label, bg_color_label, example_text_label, up_button, down_button))
        #self.root.geometry(f"{self.width}x{self.calc_height()}")

    def calc_height(self):
        # Not working correctly
        rows = len(self.rows)
        self.root.update_idletasks()
        row_h = self.rows[0][0].winfo_height()
        print(row_h)
        if rows == 10:
            return 500
        if rows > 10:
            return 500 + rows*row_h
        if rows < 10:
            return 500
        
    def remove_row(self):   
        self.rows.pop()
        for widget in self.grid_frame.winfo_children():
            widget.grid_forget()        
        temp = self.rows
        self.rows = []
        self.header()
        for color in temp:
            self.add_row(color[2].cget('bg'), color[1].cget('bg'))  # Add an initial row

    def move_row_up(self, index):
        if index > 0:
            # Swap rows in the list
            self.rows[index], self.rows[index - 1] = self.rows[index - 1], self.rows[index]
            self.update_grid()

    def move_row_down(self, index):
        if index < len(self.rows) - 1:
            # Swap rows in the list
            self.rows[index], self.rows[index + 1] = self.rows[index + 1], self.rows[index]
            self.update_grid()

    def update_grid(self):
        # Update grid display after reordering
        for i, row in enumerate(self.rows):
            num_label, fg_label, bg_label, example_label, up_button, down_button = row
            num_label.config(text=str(i + 1))
            num_label.grid(row=i + 1, column=0)
            fg_label.grid(row=i + 1, column=1)
            bg_label.grid(row=i + 1, column=2)
            example_label.grid(row=i + 1, column=3)
            up_button.grid(row=i + 1, column=4)
            down_button.grid(row=i + 1, column=4, padx=(30, 5))

    def change_color(self, label):
        # Open color chooser and apply selected color to label's background
        color_code = colorchooser.askcolor(title="Choose Color")[1]
        if color_code:
            label.config(bg=color_code)

            # Update example text colors based on the selected swatch
            for row in self.rows:
                fg_label, bg_label = row[1], row[2]
                example_text_label = row[3]

                example_text_label.config(fg=fg_label.cget("bg"), bg=bg_label.cget("bg"))

    def reset(self, colors=default_highlight_colors):
        # Initialize color rows
        self.rows = []
        for color in colors:
            self.add_row(color[0], color[1])  # Add an initial row
    
    def header(self):
        # Add header labels
        headers = ["#", "Foreground", "Background", "Example Text"]
        for col, text in enumerate(headers):
            header_label = tk.Label(self.grid_frame, text=text, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=5)

    def help(self):
        help_content = """Change the Highlight Color of the solution of the words displayed in the puzzle grid\n
\'Add Color\': add a new configuration to the list. If there are more words in the word list than color configurations, the colors are cycled\n
\'Remove Color\': remove the last color configuration in the table\n
Use the arrows to change the order\n
Change the Foreground and Background colors by clicking on the color patches"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_text = tk.Text(help_window, wrap="word", padx=10, pady=10)
        help_text.insert("1.0", help_content)
        help_text.config(state="disabled")  # Make text read-only
        help_text.pack(expand=True, fill="both")

    def save_color_config(self):
        global highlight_colors
        highlight_colors = []
        for color in self.rows:
            highlight_colors.append([color[2].cget('bg'), color[1].cget('bg')])

    def cancel(self):
        # revert changes before closing
        global highlight_colors
        highlight_colors = self.colors
        self.exit()

    def exit(self):
        global highlight_colors
        self.ws_manager.configure_highlights(highlight_colors)
        self.root.destroy()

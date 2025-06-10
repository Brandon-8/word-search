def center_popup(root, width, height):
    # Get the root window's position and dimensions
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # Calculate position for the popup to be centered on the root window
    center_x = root_x + (root_width - width) // 2
    center_y = root_y + (root_height - height) // 2
    return f"{width}x{height}+{center_x}+{center_y}"
         
    
import os
from PyPDF2 import PdfReader, PdfWriter

def find_repeat_words(filePath):
    """
    For large files with many puzzles, find which words appear the most frequently in the word
    lists
    """
    words = []
    counts = []
    with open(filePath, "r", encoding='utf-8') as f:
        for line in f:
            l = line.strip().lower()
            if l:
                if l[0].isdigit() or l[0] == '#' or l[:6] == 'theme:' or l[:6] == 'title:':
                    pass
                elif l[:9] == 'subtitle:':
                    pass
                elif l[:5] == 'mask:':
                    pass
                elif l[:5]== 'size:' and 'x' not in l:
                    pass
                elif l[:5] == 'size:' and 'x' in l:
                    pass
                elif 'puzzle grid' in l:
                    pass
                elif 'word list' in l:
                    pass
                elif 'solutions' in l:
                    pass
                else:
                    if l in words:
                        i = words.index(l)
                        counts[i] += 1
                    else:
                        words.append(l)
                        counts.append(1)
    # combine and reorder counts and words list
    combined = []
    for i in range(len(counts)):
        if counts[i] != 1:
            combined.append((counts[i], words[i]))
            
    return sorted(combined, key=lambda x: x[0], reverse=True), len(words)    

def check_valid_encoding(filePath, encoding='utf-8'):
    line_number = 0
    with open(filePath, 'rb', encoding=encoding) as f:
        for line in f:
            line_number += 1
            try:
                line.decode('utf-8')  # Attempt to decode each line
            except UnicodeDecodeError as e:
                print(f"Error in line {line_number}: {e}")
                print(f"Problematic byte sequence: {line[e.start:e.end]}")

def merge_pdfs(pdf1_path, pdf2_path, output_path):
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
    with open(output_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == '__main__':
    filePath = 'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\saved\\daily_2025.txt'
    repeats, num_unqiue = find_repeat_words(filePath)
    for r in repeats:
        print(r)
    print(num_unqiue)
    filePath1 = 'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\ws_about.pdf'
    filePath2 = 'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\pdfs\\daily_2025.pdf'
    outputPath = 'C:\\Users\\Brand\\Data\\kdp\\puzzles\\word searches\\daily_2025_final.pdf'
    merge_pdfs(filePath1, filePath2, outputPath)
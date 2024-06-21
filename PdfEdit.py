import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_headers_footers_watermarks(input_pdf_path, output_pdf_path):
    try:
        # Open the PDF
        document = fitz.open(input_pdf_path)
        
        # Define criteria for headers, footers, and watermarks
        # This can be customized as needed
        watermark_texts = ["Your Watermark Text", "Header Text", "Footer Text"]
        
        for page_number in range(len(document)):
            page = document[page_number]
            
            # Remove text-based watermarks, headers, and footers
            for text in watermark_texts:
                text_instances = page.search_for(text)
                for inst in text_instances:
                    page.add_redact_annotation(inst, fill=(1, 1, 1))
                page.apply_redactions()
        
        # Save the cleaned PDF
        document.save(output_pdf_path)
        document.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, file_path)

def process_file():
    input_pdf_path = entry_input.get()
    if not input_pdf_path:
        messagebox.showerror("Error", "Please select an input PDF file.")
        return

    output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_pdf_path:
        return

    success = remove_headers_footers_watermarks(input_pdf_path, output_pdf_path)
    if success:
        messagebox.showinfo("Success", f"Header, footer, and watermark removed. Saved as {output_pdf_path}")
    else:
        messagebox.showerror("Error", "Failed to process the PDF file.")

# Create the main window
root = tk.Tk()
root.title("PDF Header/Footer/Watermark Remover")

# Create and place widgets
label_input = tk.Label(root, text="Input PDF File:")
label_input.grid(row=0, column=0, padx=10, pady=10)

entry_input = tk.Entry(root, width=50)
entry_input.grid(row=0, column=1, padx=10, pady=10)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10)

button_process = tk.Button(root, text="Remove Header/Footer/Watermark", command=process_file)
button_process.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Start the main event loop
root.mainloop()

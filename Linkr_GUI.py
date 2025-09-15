import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
from global_var import VERSION

def compress():
    package_name = entry_package.get().strip()
    folder_path = entry_folder.get().strip()
    urls = entry_urls.get("1.0", tk.END).strip().splitlines()   

    if not package_name or not folder_path or not urls:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    try:
        cmd =  ['linkr', 'compress', package_name, folder_path] + [url.strip() for url in urls if url.strip()]
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Package '{package_name}.linkr' created successfully.")
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Compression failed: {e}")
        messagebox.showinfo("Info", "Ensure that linkr.exe is in your system PATH or in the same directory as this GUI.")


def extract():
    file_path_2 = entry_linkr.get().strip()
    folder_path_2 = entry_folder_2.get().strip()
    checksum_override = var_override.get()
    
    if not file_path_2 or not folder_path_2:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    try:
        cmd = ['linkr', 'extract', file_path_2, folder_path_2]
        if checksum_override:
            cmd.append('--override-checksum')
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Files extracted successfully to '{folder_path_2}'.")
    
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Extraction failed: {e}")
        messagebox.showinfo("Info", "Ensure that linkr.exe is in your system PATH or in the same directory as this GUI.")


root =  tk.Tk()
root.title(f"Linkr {VERSION}")
root.geometry("640x625")

style = ttk.Style()
style.configure("CustomStyle.TLabel", font=("Bookman Old Style", 11))

heading = ttk.Style()
heading.configure("Heading.TLabel", font=("Bookman Old Style", 16, "bold"))

h2 = ttk.Style()
h2.configure("SubHeading.TLabel", font=("Bookman Old Style", 14, "bold"))

button_style = ttk.Style()
button_style.configure("CustomStyle.TButton", font=("Bookman Old Style", 10))

main_btn_style = ttk.Style()
main_btn_style.configure("Main.TButton", font=("Bookman Old Style", 12, "bold"), padding=10)

chk_style = ttk.Style()
chk_style.configure("CustomStyle.TCheckbutton", font=("Bookman Old Style", 11))

ttk.Label(root, text="Linkr - Package and Extract Files", style="Heading.TLabel").grid(row=0, column=0, columnspan=3, pady=10)
tab_control = ttk.Notebook(root)
tab_compress = tk.Frame(tab_control)
tab_extract = tk.Frame(tab_control)
tab_control.add(tab_compress, text="Compress")
tab_control.add(tab_extract, text="Extract")
tab_control.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Compress Tab
ttk.Label(tab_compress, text="Compress Folder", style="SubHeading.TLabel").grid(row=0, column=0, columnspan=3, pady=10)
ttk.Label(tab_compress, text="Package Name:", style="CustomStyle.TLabel").grid(row=1, column=0, pady=5)
entry_package = tk.Entry(tab_compress, width=50)
entry_package.grid(row=1, column=1, pady=5)

ttk.Label(tab_compress, text="Package Location:", style="CustomStyle.TLabel").grid(row=2, column=0, pady=5)
entry_folder = tk.Entry(tab_compress, width=50)
entry_folder.grid(row=2, column=1, pady=5)

btn_browse_folder = ttk.Button(tab_compress, text="Browse", style="CustomStyle.TButton", command=lambda: entry_folder.insert(0, filedialog.askdirectory()))
btn_browse_folder.grid(row=2, column=2, padx=5, pady=5)

ttk.Label(tab_compress, text="Server URLs (one per line):", style="CustomStyle.TLabel").grid(row=3, column=0, pady=5)
entry_urls = tk.Text(tab_compress, width=50, height=10)
entry_urls.grid(row=4, column=0, columnspan=3, pady=5)

btn_compress = ttk.Button(tab_compress, style="Main.TButton", text="Compress", command=compress)
btn_compress.config(width=20)
btn_compress.grid(row=5, column=0, columnspan=3, pady=20)

# Extract Tab
ttk.Label(tab_extract, text="Extract Linkr File", style="SubHeading.TLabel").grid(row=0, column=0, columnspan=3, pady=10)
ttk.Label(tab_extract, text="Linkr File:", style="CustomStyle.TLabel").grid(row=1, column=0, pady=5)
entry_linkr = tk.Entry(tab_extract, width=50)
entry_linkr.grid(row=1, column=1, pady=5)
btn_browse_linkr = ttk.Button(tab_extract, style="CustomStyle.TButton", text="Browse", command=lambda: entry_linkr.insert(0, filedialog.askopenfilename(filetypes=[("Linkr files", "*.linkr")])))
btn_browse_linkr.grid(row=1, column=2, padx=5, pady=5)
ttk.Label(tab_extract, text="Destination:", style="CustomStyle.TLabel").grid(row=2, column=0, pady=5)
entry_folder_2 = tk.Entry(tab_extract, width=50)
entry_folder_2.grid(row=2, column=1, pady=5)
btn_browse_folder_2 = ttk.Button(tab_extract, style="CustomStyle.TButton", text="Browse", command=lambda: entry_folder_2.insert(0, filedialog.askdirectory()))
btn_browse_folder_2.grid(row=2, column=2, padx=5, pady=5)
var_override = tk.BooleanVar()
chk_override = ttk.Checkbutton(tab_extract, text="Override checksum errors", style="CustomStyle.TCheckbutton", variable=var_override)
chk_override.grid(row=3, column=0, columnspan=3, pady=5)
btn_extract = ttk.Button(tab_extract, style="Main.TButton", text="Extract", command=extract)
btn_extract.config(width=20)
btn_extract.grid(row=4, column=0, columnspan=3, pady=20)
copyright_label = ttk.Label(root, text="\u00A9 2025 Mohammad Zain", font=("Bookman Old Style", 10))
copyright_label.grid(row=5, column=0, columnspan=3, pady=5)


root.mainloop()

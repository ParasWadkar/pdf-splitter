#!/usr/bin/env python3
"""GUI for PDF Splitter - Select and process multiple PDFs."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
from src.splitter import split_pdf_into_quadrants
import threading


class PDFSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter - Batch Processor")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        self.selected_files = []
        self.processing = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI layout."""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="📄 PDF Splitter - Batch Processor",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Selection frame
        selection_frame = tk.LabelFrame(content_frame, text="Step 1: Select PDFs", font=("Helvetica", 10, "bold"))
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = tk.Frame(selection_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.browse_btn = tk.Button(
            button_frame,
            text="📁 Browse & Select PDFs",
            command=self.browse_files,
            bg="#3498db",
            fg="white",
            font=("Helvetica", 11, "bold"),
            padx=15,
            pady=10
        )
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_selection,
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 10),
            padx=15,
            pady=10
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # File list frame
        list_frame = tk.LabelFrame(content_frame, text="Step 2: Selected Files", font=("Helvetica", 10, "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 9),
            height=8
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Output directory frame
        output_frame = tk.LabelFrame(content_frame, text="Step 3: Output Directory (Optional)", font=("Helvetica", 10, "bold"))
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_button_frame = tk.Frame(output_frame)
        output_button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.output_btn = tk.Button(
            output_button_frame,
            text="📂 Choose Output Folder",
            command=self.choose_output_dir,
            bg="#9b59b6",
            fg="white",
            font=("Helvetica", 10),
            padx=15,
            pady=8
        )
        self.output_btn.pack(side=tk.LEFT)
        
        self.output_path_label = tk.Label(
            output_button_frame,
            text="(Same as input files)",
            font=("Helvetica", 9),
            fg="#7f8c8d"
        )
        self.output_path_label.pack(side=tk.LEFT, padx=10)
        
        self.output_dir = None
        
        # Progress frame
        progress_frame = tk.LabelFrame(content_frame, text="Progress", font=("Helvetica", 10, "bold"))
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_label = tk.Label(progress_frame, text="Ready", font=("Helvetica", 9), fg="#27ae60")
        self.progress_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # PROCESS BUTTON FRAME - LARGE AND PROMINENT
        button_action_frame = tk.Frame(content_frame, bg="#ecf0f1", relief=tk.SUNKEN, bd=2)
        button_action_frame.pack(fill=tk.X, pady=(0, 0))
        
        button_inner_frame = tk.Frame(button_action_frame, bg="#ecf0f1")
        button_inner_frame.pack(fill=tk.X, padx=10, pady=15)
        
        self.process_btn = tk.Button(
            button_inner_frame,
            text="▶ START PROCESSING",
            command=self.process_files,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 14, "bold"),
            padx=40,
            pady=15,
            relief=tk.RAISED,
            bd=3,
            activebackground="#229954",
            activeforeground="white"
        )
        self.process_btn.pack(side=tk.LEFT, expand=True)
        
        self.cancel_btn = tk.Button(
            button_inner_frame,
            text="⏹ CANCEL",
            command=self.cancel_processing,
            bg="#95a5a6",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED,
            activebackground="#7f8c8d",
            activeforeground="white"
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(10, 0))
    
    def browse_files(self):
        """Open file browser to select multiple PDFs."""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if files:
            self.selected_files.extend(files)
            self.update_file_list()
    
    def clear_selection(self):
        """Clear the selected files list."""
        self.selected_files.clear()
        self.update_file_list()
        self.progress_label.config(text="Ready", fg="#27ae60")
        self.progress_bar['value'] = 0
    
    def update_file_list(self):
        """Update the listbox with selected files."""
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            filename = Path(file).name
            self.file_listbox.insert(tk.END, filename)
    
    def choose_output_dir(self):
        """Choose output directory for processed PDFs."""
        dir_path = filedialog.askdirectory(title="Choose output directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_path_label.config(text=dir_path, fg="#2c3e50")
    
    def process_files(self):
        """Process all selected PDFs in a separate thread."""
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select at least one PDF file.")
            return
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_files_thread)
        thread.start()
    
    def _process_files_thread(self):
        """Worker thread for processing files."""
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.browse_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)
        
        total_files = len(self.selected_files)
        successful = 0
        failed = 0
        errors = []
        
        for index, input_file in enumerate(self.selected_files):
            if not self.processing:
                break
            
            try:
                # Determine output path
                input_path = Path(input_file)
                if self.output_dir:
                    output_path = Path(self.output_dir) / f"{input_path.stem}_split.pdf"
                else:
                    output_path = input_path.parent / f"{input_path.stem}_split.pdf"
                
                # Update status
                filename = input_path.name
                self.progress_label.config(text=f"Processing: {filename}...", fg="#f39c12")
                self.root.update()
                
                # Process the PDF
                split_pdf_into_quadrants(str(input_file), str(output_path))
                
                successful += 1
                
                # Update progress
                progress = ((index + 1) / total_files) * 100
                self.progress_bar['value'] = progress
                self.progress_label.config(
                    text=f"✅ Completed: {filename}",
                    fg="#27ae60"
                )
                self.root.update()
                
            except Exception as e:
                failed += 1
                errors.append(f"{Path(input_file).name}: {str(e)}")
                self.progress_label.config(
                    text=f"❌ Failed: {Path(input_file).name}",
                    fg="#e74c3c"
                )
                self.root.update()
        
        # Processing complete
        self.processing = False
        self.process_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.browse_btn.config(state=tk.NORMAL)
        self.clear_btn.config(state=tk.NORMAL)
        
        if self.processing or not self.selected_files:
            return
        
        # Show summary
        message = f"Processing Complete!\n\n✅ Successful: {successful}\n❌ Failed: {failed}"
        if errors:
            message += f"\n\nErrors:\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                message += f"\n... and {len(errors) - 5} more"
        
        self.progress_label.config(text="✅ All done!", fg="#27ae60")
        messagebox.showinfo("Processing Complete", message)
    
    def cancel_processing(self):
        """Cancel ongoing processing."""
        self.processing = False
        self.progress_label.config(text="Cancelled", fg="#e74c3c")
        self.cancel_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterGUI(root)
    root.mainloop()

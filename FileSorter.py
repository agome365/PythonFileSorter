import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Define categories for file types
FILE_CATEGORIES = {
    'Excel Files': ['xls', 'xlsx', 'csv'],
    'Video Files': ['mp4', 'avi', 'mkv', 'mov', 'flv'],
    'Image Files': ['jpg', 'jpeg', 'png', 'gif'],
    'Document Files': ['pdf', 'doc', 'docx', 'txt']
}

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")
        self.root.geometry("400x200")

        # Create a button to select files
        self.button = tk.Button(root, text="Select Files to Sort", width=30, height=2, command=self.open_file_dialog)
        self.button.pack(pady=20)

        # Initialize the list of files
        self.file_paths = []

    def open_file_dialog(self):
        # Open the file dialog to allow the user to select multiple files
        self.file_paths = filedialog.askopenfilenames(title="Select Files to Sort")

        if self.file_paths:
            # Ask the user for the output directory after files have been selected
            self.ask_output_folder()

    def ask_output_folder(self):
        # Ask user for the output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory for Sorted Files")

        if output_dir:
            # Sort the files into the selected output directory
            self.sort_files(output_dir)

    def sort_files(self, output_dir):
        files_sorted = 0
        folders_created = set()

        for file_path in self.file_paths:
            filename = os.path.basename(file_path)

            # Get the file extension
            _, ext = os.path.splitext(filename)
            ext = ext[1:].lower()  # Remove the leading dot and lowercase the extension

            # Skip files without an extension
            if ext == "":
                continue

            # Determine the folder name based on file category
            folder_name = None
            for category, extensions in FILE_CATEGORIES.items():
                if ext in extensions:
                    folder_name = category
                    break

            # If the file does not match any category, use the extension with " Files"
            if folder_name is None:
                folder_name = f"{ext.upper()} Files"

            # Set the folder path
            folder = os.path.join(output_dir, folder_name)

            # Create the folder if it doesn't exist and track folders created
            if not os.path.exists(folder):
                os.makedirs(folder)
                folders_created.add(folder_name)

            # Move the file to the new folder and count sorted files
            new_file_path = os.path.join(folder, filename)
            shutil.move(file_path, new_file_path)
            files_sorted += 1

        # Show a summary of the sorting process
        self.show_summary(files_sorted, folders_created)

    def show_summary(self, files_sorted, folders_created):
        # Display a message with the sorting summary
        message = f"Files sorted: {files_sorted}\n"
        if folders_created:
            message += f"Folders created: {', '.join(folders_created)}"
        else:
            message += "No new folders were created."

        messagebox.showinfo("Sorting Completed", message)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()
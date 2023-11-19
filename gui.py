import tkinter as tk
from tkinter import filedialog
import sqlite3

class ImageSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Selector App")

        # Variables to store text and file paths
        self.question_text = tk.StringVar()
        self.answer_text = tk.StringVar()
        self.question_image_path = tk.StringVar()
        self.answer_image_path = tk.StringVar()

        # Database initialization
        self.conn = sqlite3.connect('image_selector_db.db')
        self.create_table()
        self.update_entry_count()

        # Create widgets for question
        self.create_widgets("Question", self.question_text, self.question_image_path, 0)

        # Create widgets for answer
        self.create_widgets("Answer", self.answer_text, self.answer_image_path, 2)

    def create_widgets(self, label_text, text_var, file_path_var, row):
        # Label for text field
        label = tk.Label(self.root, text=f"{label_text} Text:")
        label.grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)

        # Text field
        text_entry = tk.Entry(self.root, textvariable=text_var, width=30)
        text_entry.grid(row=row, column=1, padx=10, pady=5, sticky=tk.W)

        # Button for file selection
        file_button = tk.Button(self.root, text=f"Select {label_text} Image", command=lambda: self.browse_file(file_path_var))
        file_button.grid(row=row, column=2, padx=10, pady=5, sticky=tk.W)

        # Print button
        print_button = tk.Button(self.root, text=f"Print {label_text}", command=lambda: self.save_to_database(text_var.get(), file_path_var.get()))
        print_button.grid(row=row, column=3, padx=10, pady=5, sticky=tk.W)

    def browse_file(self, file_path_var):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        file_path_var.set(file_path)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                answer_text TEXT,
                question_image_path TEXT,
                answer_image_path TEXT
            )
        ''')
        self.conn.commit()

    def save_to_database(self, question_text, question_image_path):
        # Check if the number of entries exceeds 10
        if self.get_entry_count() >= 10:
            self.disable_buttons()
            self.show_message("Maximum number of cards reached (10)")

        else:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO entries (question_text, question_image_path) VALUES (?, ?)
            ''', (question_text, question_image_path))
            self.conn.commit()

            # Update entry count and check if it exceeds 10
            self.update_entry_count()
            if self.get_entry_count() >= 10:
                self.disable_buttons()
                self.show_message("Maximum number of cards reached (10)")

    def update_entry_count(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM entries')
        count = cursor.fetchone()[0]
        self.entry_count = count

        # Update entry count on the GUI
        self.update_entry_count_label()

    def get_entry_count(self):
        return self.entry_count

    def update_entry_count_label(self):
        # Label to display the number of entries
        entry_count_label = tk.Label(self.root, text=f"Number of Entries: {self.get_entry_count()}")
        entry_count_label.grid(row=4, column=0, columnspan=4, pady=10, sticky=tk.W)

    def disable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)

    def show_message(self, message):
        message_label = tk.Label(self.root, text=message, fg='red')
        message_label.grid(row=5, column=0, columnspan=4, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSelectorApp(root)
    root.mainloop()

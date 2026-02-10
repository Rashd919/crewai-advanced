import tkinter as tk
from tkinter import ttk

class Raed(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("الرعد")
        self.geometry("800x600")
        self.sidebar = tk.Frame(self, bg="#2f4f4f")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.main_frame = tk.Frame(self, bg="#f0f0f0")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.sidebar_label = tk.Label(self.sidebar, text="الرعد", bg="#2f4f4f", fg="#ffffff", font=("Arial", 24))
        self.sidebar_label.pack(pady=20)
        
        self.message_count_label = tk.Label(self.sidebar, text="0", bg="#2f4f4f", fg="#ffffff", font=("Arial", 18))
        self.message_count_label.pack(pady=20)
        
        self.main_label = tk.Label(self.main_frame, text="الرعد", bg="#f0f0f0", fg="#808080", font=("Arial", 24))
        self.main_label.pack(pady=20)
        
        self.header_label = tk.Label(self.main_frame, text="الرعد", bg="#f0f0f0", fg="#ffd700", font=("Arial", 18))
        self.header_label.pack(pady=20)
        
        self.message_text = tk.Text(self.main_frame, bg="#f0f0f0", font=("Arial", 14))
        self.message_text.pack(fill=tk.BOTH, expand=True)
        
        self.update_message_count()
        
    def update_message_count(self):
        # تعديل لاحق
        self.message_count_label.config(text=str(0))
        self.after(1000, self.update_message_count)

if __name__ == "__main__":
    app = Raed()
    app.mainloop()
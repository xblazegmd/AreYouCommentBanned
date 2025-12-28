import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Are You Comment Banned?")
        self.geometry("500x400")
        self.resizable(False, False)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

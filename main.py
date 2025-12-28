import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Are You Comment Banned?")
        self.geometry("300x400")
        self.resizable(False, False)

        # User info
        self.username = tk.StringVar()

        ttk.Label(self, text="Username:").pack(pady=(10, 0))
        usernameEntry = ttk.Entry(self, textvariable=self.username)
        usernameEntry.pack(pady=(0, 10))

        self.password = tk.StringVar()

        ttk.Label(self, text="Password:").pack(pady=(10, 0))
        passwordEntry = ttk.Entry(self, textvariable=self.password, show="*")
        passwordEntry.pack(pady=(0, 10))

        # Disclaimer text
        # As someone who's been making GD mods for a while, why does this formatting
        # remind me of FLAlertLayer lol
        ttk.Label(
            self,
            text="Have in mind that to test if you're\ncomment banned, you will have to try\nand upload a comment",
            justify=tk.CENTER
        ).pack(pady=10) # Only thing it's missing is the -> operator

        # Level ID
        self.levelID = tk.StringVar()

        ttk.Label(self, text="Level ID").pack(pady=(10, 0))
        levelIDEntry = ttk.Entry(self, textvariable=self.levelID)
        levelIDEntry.pack(pady=(0, 10))

        # Test Comment
        self.comment = tk.StringVar()
        self.comment.trace_add("write", self.onCommentEntryWrite)

        ttk.Label(self, text="Comment (will be deleted if you want)").pack(pady=(10, 0))
        commentEntry = ttk.Entry(self, textvariable=self.comment)
        commentEntry.pack(pady=(0, 10))

        # The Moment of Truth
        ttk.Button(self, text="Am I Comment Banned?", command=self.onBtClick).pack(pady=10)
    
    def onCommentEntryWrite(self, *args):
        charLimit = 100
        txt = self.comment.get()
        if len(txt) > charLimit:
            self.comment.set(txt[:charLimit])
    
    def onBtClick(self):
        messagebox.showinfo("TODO", "TODO")

def main() -> None:
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

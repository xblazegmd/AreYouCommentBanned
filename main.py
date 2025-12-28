import tkinter as tk
from tkinter import ttk, messagebox

import requests

API = "http://www.boomlings.com/database/"
SECRET = "Wmfd2893gb7"
HEADERS = { "User-Agent": "" }

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
        levelIDEntry = ttk.Entry(
            self,
            textvariable=self.levelID,
            validate="key",
            validatecommand=(self.register(self.validateLevelIDEntry), "%P")
        )
        levelIDEntry.pack(pady=(0, 10))

        # Test Comment
        self.comment = tk.StringVar()
        self.comment.trace_add("write", self.onCommentEntryWrite)

        ttk.Label(self, text="Comment (will be deleted if you want)").pack(pady=(10, 0))
        commentEntry = ttk.Entry(self, textvariable=self.comment)
        commentEntry.pack(pady=(0, 10))

        # The Moment of Truth
        ttk.Button(self, text="Am I Comment Banned?", command=self.onBtClick).pack(pady=10)
    
    def validateLevelIDEntry(self, P: str) -> None:
        return P.isdigit() or P == ""
    
    def onCommentEntryWrite(self, *args) -> None:
        charLimit = 100
        txt = self.comment.get()
        if len(txt) > charLimit:
            self.comment.set(txt[:charLimit])
    
    def onBtClick(self) -> None:
        username = self.username.get()
        password = self.password.get()
        levelID = int(self.levelID.get())
        comment = self.comment.get()

        # Get accountID
        accIDReqParams = {
            "secret": SECRET,
            "str": username
        }

        accIDReq = requests.post(API + "getGJUsers20.php", data=accIDReqParams, headers=HEADERS)

        if not accIDReq.ok:
            messagebox.showerror(title="Error", message=f"Could not find user data: {accIDReq.text}")
            return
        
        if accIDReq.text == "-1":
            messagebox.showerror(title="Error", message=f"User '{username}' was not found")
            return
        
        res = accIDReq.text.split(":")
        accID = int(res[3])
        print(accID)

        # Try and upload comment
        uploadCommentReqParams = {
            "accountID": accID,
            "gjp": "",
            "comment": "",
            "levelID": levelID,
            "percent": 0,
            "chk": "",
            "secret": SECRET
        }

def main() -> None:
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

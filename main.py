import tkinter as tk
from tkinter import ttk, messagebox

from utils import *

import base64
import requests
from enum import Enum

API = "http://www.boomlings.com/database/"
SECRET = "Wmfd2893gb7"
HEADERS = { "User-Agent": "" }

class Status(Enum):
    NORMAL = "Not banned",
    BANNED = "Banned",
    PERMABANNED = "Banned"

class StatusPopup(tk.Toplevel):
    def __init__(self, master, status: Status, duration: int | None = None, reason: str = "N/A") -> None:
        super().__init__(master)

        if status == Status.BANNED and duration is None:
            raise ValueError("Expected value for 'duration'")

        self.title("Status")
        self.geometry("300x200")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onExit)

        # Info labels
        ttk.Label(self, text=f"Status: {status.value[0]}").pack(pady=10)

        if status != Status.NORMAL:
            ttk.Label(self, text=f"Duration: {'PERMANENT' if status == Status.PERMABANNED else duration}").pack(pady=10)
            ttk.Label(self, text=f"Reason: {reason}").pack(pady=10)

        ttk.Button(self, text="Ok", command=self.onExit).pack(pady=10)
    
    def onExit(self):
        self.master.deiconify()
        self.destroy()

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
        levelIDPre = self.levelID.get()
        comment = self.comment.get()

        if not username or not password or not levelIDPre or not comment:
            messagebox.showerror(title="Error", message="Missing options")
            return

        levelID = int(levelIDPre)

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
        
        accIDRes = parseKeyValStr(accIDReq.text)
        accID = int(accIDRes["16"]) # 16 = accountID

        # Try and upload comment
        commentEnc = base64.urlsafe_b64encode(comment.encode()).decode()
        percent = 0
        gjp = gjp2(password)
        chk = generateChk([username, commentEnc, levelID, percent], "29481", "0xPT6iUrtws0J")

        uploadCommentReqParams = {
            "accountID": accID,
            "gjp2": gjp,
            "userName": username,
            "comment": commentEnc,
            "levelID": levelID,
            "percent": percent,
            "chk": chk,
            "secret": SECRET
        }
        print(uploadCommentReqParams)

        uploadCommentReq = requests.post(API + "uploadGJComment21.php", data=uploadCommentReqParams, headers=HEADERS)

        if not uploadCommentReq.ok:
            messagebox.showerror(title="Error", message=f"An unexpected error occured: {uploadCommentReq}")
            return

        uploadCommentRes = uploadCommentReq.text
        
        if uploadCommentRes == "-1":
            messagebox.showerror(title="Error", message="Failed to upload comment (no you're not comment banned this is different)")
            return

        self.withdraw()

        # The moment of truth: are you comment banned?
        if uploadCommentRes == "-10":
            StatusPopup(self, Status.PERMABANNED)
        elif uploadCommentRes.startswith("temp_"):
            info = parseTempBan(uploadCommentRes)
            StatusPopup(self, Status.BANNED, info["duration"], info["reason"])
        else:
            StatusPopup(self, Status.NORMAL)
        
        # Reset all inputs
        self.username.set("")
        self.password.set("")
        self.levelID.set("")
        self.comment.set("")

def main() -> None:
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
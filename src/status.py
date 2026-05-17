import tkinter as tk
from tkinter import ttk, messagebox

from utils import *

import requests
from enum import Enum

class Status(Enum):
    NORMAL = "Not Banned",
    BANNED = "Banned",
    PERMABANNED = "Banned"

class StatusPopup(tk.Toplevel):
    def __init__(
        self,
        master,
        status: Status,
        duration: str | None = None,
        reason: str = "N/A",
        accID: int | None = None, 
        commentID: int | None = None,
        levelID: int | None = None,
        gjp2: str | None = None
    ) -> None:
        super().__init__(master)

        self.title("Status")
        self.geometry("300x200")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onExit)

        self.status = status

        if self.status == Status.BANNED and duration is None:
            raise ValueError("Expected value for 'duration'")

        required = {
            "accID": accID,
            "commentID": commentID,
            "levelID": levelID,
            "gjp2": gjp2
        }
        missing = [name for name, val in required.items() if val is None]

        if self.status == Status.NORMAL and missing:
            raise ValueError(f"Expected value for {', '.join(missing)}")

        self.accID = accID
        self.commentID = commentID
        self.levelID = levelID
        self.gjp2 = gjp2

        # Info labels
        ttk.Label(self, text=f"Status: {self.status.value}").pack(pady=10)

        if self.status != Status.NORMAL:
            ttk.Label(self, text=f"Duration: {'PERMANENT' if self.status == Status.PERMABANNED else f'{duration} days'}").pack(pady=10)
            ttk.Label(self, text=f"Reason: {reason}").pack(pady=10)

        ttk.Button(self, text="Ok", command=self.onOkButton).pack(pady=(10, 2))

        if status != Status.NORMAL:
            ttk.Button(self, text="What do I do now?", command=self.onHelp).pack()
    
    def onOkButton(self):
        if self.status == Status.NORMAL and messagebox.askyesno(title="Delete comment", message="Do you want to delete the comment?"):
            params = {
                "accountID": self.accID,
                "gjp2": self.gjp2,
                "commentID": self.commentID,
                "levelID": self.levelID,
                "secret": SECRET
            }

            req = requests.post(API + "deleteGJComment20.php", data=params, headers=HEADERS)

            if not req.ok or req.text == "-1":
                messagebox.showerror(title="Error", message="Failed to delete comment")
            else:
                messagebox.showinfo(title="Sucess", message="Sucessfully deleted comment")

        self.onExit()

    def onHelp(self):
        if self.status == Status.PERMABANNED:
            messagebox.showinfo("What do I do now?", "You rly can't do anything. You've been permanently banned/banned for an extremely long time. And you can't easily ban evade that. If you believe you've been falsely banned, contact an Elder Moderator")
        else:
            messagebox.showinfo("What do I do now?", "Wait until the ban is over. It'll range from either a couple of days to a couple of weeks. And please don't try to ban evade (ban evasion may result in a perma ban). If you believe you've been falsely banned, contact an Elder Moderator")

    def onExit(self):
        self.master.deiconify()
        self.destroy()
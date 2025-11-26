#!/usr/bin/env python3

#
# Copyright (C) 2025 Joelle Maslak
# All Rights Reserved - See License
#

import os
import pathlib
import re
import shutil
import subprocess
import time
from typing import List
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, ProgressBar


class PrintApp(App):
    """App to print output."""

    CSS_PATH = "print.css"

    BINDINGS = [
        ("p", "print", "Print File"),
        ("s", "skip", "Skip File"),
        ("D", "delete", "Delete File"),
        ("q", "quit", "Quit"),
    ]
    index = reactive(0)

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        self.theme = "textual-dark"

        self.files = get_files()
        self.index = 0
        self.len = len(self.files)

        self.label = Label(id="lbl1")
        self.label.border_title = "Next File"

        self.pb = ProgressBar(id="pb", total=self.len, show_eta=False)
        self.update_status()

        yield Header()
        yield Footer()
        yield self.pb
        yield Center(self.label)

    def action_skip(self) -> None:
        """Skip current file."""
        self.index += 1
        self.update_status()

    def action_delete(self) -> None:
        """Unlink document."""
        if self.index < self.len:
            os.unlink(self.files[self.index])

        self.index += 1
        self.update_status()

    def action_print(self) -> None:
        """Print document and move."""
        fn = self.files[self.index]
        if self.index < self.len:
            subprocess.call(["lpr", fn])

            with open("printed.lst", "a") as f:
                f.write(f"{os.path.getmtime(fn)}|{fn}\n")

            # Create if it doesn't exist, and then move files, so long as it
            # is a proper directory. Otherwise skip.
            if not os.path.exists("printed"):
                os.mkdir("printed")

            if os.path.isdir("printed"):
                newname = pathlib.Path("printed") / fn

                # Also don't want it to already exist
                if not os.path.exists(newname):
                    shutil.move(fn, newname)

        self.index += 1
        self.update_status()

    def update_status(self) -> None:
        """Update all status items."""
        if self.index < self.len:
            self.label.content = self.files[self.index]
            tm = time.localtime(os.path.getmtime(self.label.content))
            self.label.border_subtitle = time.strftime("%Y-%m-%d", tm)
            self.label.remove_class("done")
            self.label.add_class("working")
        else:
            self.label.content = "Done!"
            self.label.add_class("done")
            self.label.remove_class("working")
            self.label.border_subtitle = None

        self.pb.progress = self.index


def get_files() -> List[str]:
    """List files ending in .pdf in current directory."""
    files = os.listdir()
    files.sort(
        key=os.path.getmtime,
    )
    files = [x for x in files if os.path.isfile(x) and x.endswith("pdf")]

    if not os.path.exists("printed.lst"):
        open("printed.lst", "a").close()

    with open("printed.lst", "r") as f:
        printed = [re.sub(r"^\d+\.\d+\|", "", x).rstrip() for x in f.readlines()]

    return [x for x in files if x not in printed]


def main():
    """Main application function."""
    get_files()
    app = PrintApp()
    app.run()


if __name__ == "__main__":
    main()

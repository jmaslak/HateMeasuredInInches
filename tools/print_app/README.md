# Hate Measured in Inches Print Tool

This tool is designed to be installed inside a directory where the user
dumps PDF files to be later printed.  The `print.py` and `print.css` files
must both be included, and the Python textual module must be installed.

Once installed, the user will dump PDFs into that directory.  When
desired, the user can enter that directory, run `print.py`, and print
files one at a time in chronological (based on modification time of
directory entry pointing at the PDF file).

When a user prints a file, it is moved to a `printed/` subdirectory
under the current directory and it is added to the `printed.lst` file
along with the timestamp of the modification time of the file.  Files
will not be moved (but will still be printed/added to `printed.lst` if
they are not in `printed.lst`).

Any file in the `printed.lst` file will be skipped by this tool, and not
reprinted.

The tool uses the `lpr` command to print PDFs, which should have a
default printer defined. The `lpr` command must know what to do with
`.pdf` files (modern Linux and OS X does).

This was a quick-and-dirty script, and no tests exist yet.

## How I Use the Tool

I will print all files for my Hate Measured in Inches (an exploration of
trans embodiment in a media-rich social environment) to common
directory.  When I am ready to print these documents, I'll open a
terminal window, go to this directory, and run the tool.  Once finished,
I'll check the directory for any PDF files that remain, as this
indicates that they are likely accidental duplicates. However, if they
are not, I might rename the file and print it using the tool again.

## AI Coding Tools

See [CLAUDE.md](../../CLAUDE.md) in the root of this repo.

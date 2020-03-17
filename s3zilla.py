#! /usr/bin/python3
from s3zilla.s3zilla import S3Zilla, Thread
from tkinter import Tk


def run_gui_thread():
    root = Tk()
    S3Zilla(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        thread = Thread(target=run_gui_thread)
        thread.daemon = True
        thread.start()
        thread.join()
    except KeyboardInterrupt:
        pass
    print('\nExiting S3Zilla')

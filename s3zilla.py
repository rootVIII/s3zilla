#! /usr/bin/python3
from tkinter import Tk
from threading import Thread
from sys import platform


def run_gui_thread():
    root = Tk()
    if platform != 'win32':
        from s3zilla import S3Zilla
        S3Zilla(root)
    else:
        from s3zilla import S3ZillaWin10
        S3ZillaWin10(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        thread = Thread(target=run_gui_thread)
        thread.daemon = True
        thread.start()
        thread.join()
    except KeyboardInterrupt:
        print('\nExiting S3Zilla')

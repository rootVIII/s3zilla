from s3zilla.s3zilla import S3Zilla
from tkinter import Tk


def run_gui_thread():
    root = Tk()
    S3Zilla(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        run_gui_thread()
    except KeyboardInterrupt:
        pass

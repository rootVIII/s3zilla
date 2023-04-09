# MIT License Copyright (c) 2019-2023 rootVIII
from getpass import getuser
from html import unescape
from os import listdir, remove
from os.path import realpath, isdir, basename
from shutil import rmtree
from tkinter import Menu, StringVar, Label, OptionMenu
from tkinter import Button, Listbox, E, W, PhotoImage
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno


from src.s3_client import S3Client
from src.utils import folder_walk


class App(S3Client):
    def __init__(self, master):
        S3Client.__init__(self)
        light_gray = '#D9D9D9'
        blue = '#181B42'
        green = '#33CC00'
        red = '#FF0000'
        black = '#000000'
        cyan = '#80DFFF'
        bold = 'Helvetica 10 bold'
        normal = 'Helvetica 10'

        self.finish_thread = None
        self.greeting = f'Hello {getuser()}'
        self.master = master
        self.master.title('Amazon S3 File Transfer Client')
        self.master.configure(bg=black)

        self.src = realpath(__file__)[:-len(basename(__file__))]
        self.master.geometry('600x700')
        self.master.iconbitmap(f'{self.src}icon.ico')
        self.master.maxsize('600', '700')
        self.master.minsize('600', '700')

        menu = Menu(self.master)
        menu.config(background=black, fg=light_gray)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Exit', command=self.quit_app)
        menu.add_cascade(label='File', menu=file)
        refresh = Menu(menu)
        refresh.add_command(label='Local', command=self.refresh_local)
        refresh.add_command(label='S3', command=self.refresh_s3)
        menu.add_cascade(label='Refresh', menu=refresh)

        self.refresh_img = PhotoImage(master=master, file=f'{self.src}refresh.png')

        self.chosen_directory, self.chosen_bucket = '', ''

        self.folder_path = StringVar()
        self.dropdown = StringVar()

        try:
            self.available_buckets = self.list_avail_buckets()
        except Exception:
            self.available_buckets = ['none available']

        self.local_label = Label(master, fg=green, bg=black, font=bold,
                                 width=24, text='LOCAL')
        self.local_label.grid(row=0, column=0, sticky=E+W, padx=10, pady=20)

        self.s3_label = Label(master, fg=green, bg=black, font=bold,
                              width=24, text='AWS S3')
        self.s3_label.grid(row=0, column=1, sticky=E+W, padx=10, pady=20)

        self.browse_button = Button(master, fg=light_gray, bg=blue, text='Browse',
                                    width=34, highlightbackground=black,
                                    highlightthickness=2, command=self.load_dir)
        self.browse_button.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.refresh_btn_local = Button(master, fg=light_gray, bg=black,
                                        image=self.refresh_img, width=20,
                                        borderwidth=0, highlightcolor=black,
                                        highlightbackground=black,
                                        highlightthickness=0,
                                        command=self.refresh_local)
        self.refresh_btn_local.grid(row=1, sticky=E, column=0, padx=9)

        self.dropdown_box = OptionMenu(master, self.dropdown, *self.available_buckets,
                                       command=self.set_chosen_bucket)
        self.dropdown_box.configure(fg=light_gray, bg=blue, width=36,
                                    highlightbackground=black, highlightthickness=2)
        self.dropdown_box.grid(row=1, column=1, sticky=W, padx=10, pady=10)

        self.refresh_btn_s3 = Button(master, fg=light_gray, bg=black,
                                     image=self.refresh_img, width=20,
                                     borderwidth=0, highlightcolor=black,
                                     highlightbackground=black,
                                     highlightthickness=0,
                                     command=self.refresh_s3)
        self.refresh_btn_s3.grid(row=1, sticky=E, column=1, padx=10)

        self.browse_label = Label(master, fg=light_gray, bg=black, width=24,
                                  font=normal, text='No directory selected')
        self.browse_label.grid(row=3, column=0, sticky=E+W, padx=10, pady=10)

        self.bucket_label = Label(master, fg=light_gray, bg=black, width=24,
                                  font=normal, text='No bucket selected')
        self.bucket_label.grid(row=3, column=1, sticky=E+W, padx=10, pady=10)

        self.local_explorer = Listbox(master, fg=cyan, bg=black, width=36, height=24,
                                      highlightcolor=black, selectmode='multiple')
        self.local_explorer.grid(row=5, column=0, sticky=E+W, padx=10, pady=10)

        self.s3_explorer = Listbox(master, fg=cyan, bg=black, width=36, height=24,
                                   highlightcolor=black, selectmode='multiple')
        self.s3_explorer.grid(row=5, column=1, sticky=E+W, padx=10, pady=10)

        self.upload_button = Button(master, fg=cyan, bg=blue,
                                    text=unescape('&emsp; &thinsp;▶️'),
                                    width=3, highlightbackground=black,
                                    command=self.upload)
        self.upload_button.grid(row=6, column=0, sticky=E, padx=120, pady=10)
        self.delete_local = Button(master, fg=red, bg=blue, text=unescape('❌'),
                                   width=3, highlightbackground=red, activebackground=red,
                                   command=self.delete_local_records)
        self.delete_local.grid(row=6, column=0, sticky=W, padx=120)

        self.download_button = Button(master, fg=cyan, bg=blue,
                                      text=unescape('&emsp;&thinsp;◀️'),
                                      width=3,  highlightbackground=black,
                                      command=self.download)
        self.download_button.grid(row=6, column=1, sticky=W, padx=120, pady=10)
        self.delete_s3 = Button(master, fg=red, bg=blue, text=unescape('❌'),
                                width=3, highlightbackground=red, activebackground=red,
                                command=self.delete_s3_records)
        self.delete_s3.grid(row=6, column=1, sticky=E, padx=120, pady=10)

        self.found_label_local = Label(master, fg=light_gray, bg=black,
                                       text='found local', width=16)
        self.found_label_local.grid(row=7, column=0, sticky=E+W, padx=10, pady=10)

        self.found_label_s3 = Label(master, fg=light_gray, bg=black,
                                    text='found s3', width=16)
        self.found_label_s3.grid(row=7, column=1, sticky=E+W, padx=10, pady=10)

        self.status_label = Label(master, fg=light_gray, bg=black,
                                  text=self.greeting, width=8)
        self.status_label.grid(row=8, column=0, sticky=E + W, padx=10, pady=10)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(5, weight=1)

        self.set_found_local_label('%d files found' % self.local_explorer.size())
        self.set_found_s3_label('%d files found' % self.s3_explorer.size())

    @staticmethod
    def quit_app():
        exit()

    def set_status(self, text, clear=False):
        self.status_label.config(text=text)
        if clear:
            self.status_label.after(3000, self.clear_status)
        self.status_label.update_idletasks()

    def set_found_local_label(self, text):
        self.found_label_local.config(text=text)
        self.found_label_local.update_idletasks()

    def set_found_s3_label(self, text):
        self.found_label_s3.config(text=text)
        self.found_label_s3.update_idletasks()

    @staticmethod
    def check_file_path_len(text):
        if len(text) < 60:
            return text
        return f'.../{[item.strip() for item in text.split("/") if item.strip()][-1]}'[:60]

    def set_local_browse_label(self, text):
        self.browse_label.config(text=self.check_file_path_len(text))

    def set_s3_bucket_label(self, text):
        self.bucket_label.config(text=self.check_file_path_len(text))

    def clear_status(self):
        self.status_label.config(text='')

    def get_local_sel(self):
        return [self.local_explorer.get(item) for item in self.local_explorer.curselection()]

    def get_s3_sel(self):
        return [self.s3_explorer.get(item) for item in self.s3_explorer.curselection()]

    def set_chosen_bucket(self, selection):
        self.chosen_bucket = selection

    def refresh_local(self):
        if not self.chosen_directory:
            self.set_status('Please select a directory (browse button)', clear=True)
            self.chosen_directory = ''
        else:
            self.set_local_browse_label(self.chosen_directory)
            self.local_explorer.delete(0, 'end')
            current_dir = f'{self.chosen_directory}\\'
            files = [file_name if not isdir(f'{current_dir}{file_name}') else f'{file_name}/'
                     for file_name in sorted(listdir(current_dir))]
            self.local_explorer.insert('end', *files)
            files_found = f'{self.local_explorer.size()} files found'
            self.set_found_local_label(files_found)

    def local_delete(self, files: list):
        msg = 'Finished deleting'
        if files:
            for file_name in files:
                file_path = f'{self.chosen_directory}\\{file_name}'
                if not isdir(file_path):
                    try:
                        if not isdir(file_path):
                            remove(file_path)
                        else:
                            rmtree(file_path)
                    except Exception as err:
                        msg = f'Error occurred: {err}'
                        break

        self.refresh_local()
        self.set_status(msg, clear=True)

    def delete_local_records(self):
        files = self.get_local_sel()
        if not files:
            self.set_status('Please select a file(s) to delete', clear=True)
        else:
            title = 'Delete local files?'
            if askyesno(title, '\n'.join(files)):
                self.local_delete(files)

    def delete_s3_records(self):
        to_remove = []
        if not self.chosen_bucket:
            self.set_status('Please select a bucket...', clear=True)
        else:
            to_remove = self.get_s3_sel()
        if not to_remove:
            self.set_status('Please select at least 1 object to delete', clear=True)
        else:
            title = 'Delete S3 Objects?'
            if askyesno(title, '\n'.join(to_remove)):
                for obj_name in to_remove:
                    self.delete_obj(self.chosen_bucket, obj_name)

                self.refresh_s3()
                self.set_status('Finished deleting', clear=True)

    def load_dir(self):
        self.chosen_directory = askdirectory()
        if not self.chosen_directory or not isdir(self.chosen_directory):
            self.set_status('Ensure a directory is selected', clear=True)
            self.chosen_directory = ''
        else:
            self.set_local_browse_label(self.chosen_directory)

    def refresh_s3(self):
        if 'none available' in self.available_buckets:
            self.set_status('Please create at least one S3 bucket', clear=True)
        elif not self.chosen_bucket:
            self.set_status('Please select a bucket from the drop-down list', clear=True)
        else:
            self.s3_explorer.delete(0, 'end')
            try:
                self.s3_explorer.insert('end', *self.get_bucket_contents())
            except Exception:
                self.set_status('Unable to find bucket', clear=True)
            else:
                self.set_s3_bucket_label(self.chosen_bucket)
                file_count = self.s3_explorer.size()
                files_found = f'{file_count} file-object{"s" if file_count != 1 else ""} found'
                self.set_found_s3_label(files_found)

    def upload(self):
        if not self.chosen_bucket or not self.chosen_directory:
            self.set_status('Ensure a path & S3 bucket are selected', clear=True)
        elif not self.get_local_sel():
            self.set_status('Ensure files are selected to upload', clear=True)
        else:
            self.set_status('Uploading...')
            for selection in self.get_local_sel():
                file_path = f'{self.chosen_directory}/{selection}'
                if not isdir(file_path):
                    self.upload_s3(file_path, self.chosen_bucket, basename(file_path))
                    continue
                for file_name in folder_walk(file_path, []):
                    if not isdir(file_name):
                        self.upload_s3(file_name, self.chosen_bucket,
                                       file_name[len(self.chosen_directory) + 1:])

            self.refresh_s3()
            self.set_status('Finished uploading...', clear=True)

    def download(self):
        if not self.chosen_bucket or not self.chosen_directory:
            self.set_status('Ensure a file & bucket are selected', clear=True)
        elif not self.get_s3_sel():
            self.set_status('Ensure files are selected to download', clear=True)
        else:
            for selection in self.get_s3_sel():
                file_name = f'{self.chosen_directory}/{selection}'
                print(file_name)
                # self.download_s3(self.chosen_bucket, selection, file_name)
            self.refresh_local()
            self.set_status('Downloaded...', clear=True)

    def get_bucket_contents(self):
        return self.list_bucket_contents(self.chosen_bucket)

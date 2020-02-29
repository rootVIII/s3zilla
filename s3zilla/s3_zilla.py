from tkinter import Menu, StringVar, Label, OptionMenu
from tkinter import Button, Listbox, Text, E, W, END, PhotoImage
from tkinter.filedialog import askdirectory
from os import listdir, remove, execl
from os.path import realpath
from shutil import rmtree, make_archive
from getpass import getuser
from os.path import isdir, basename
from sys import executable, argv, platform
from time import sleep
from threading import Thread

try:
    import boto3
    from botocore.exceptions import ClientError
except Exception as err:
    print('%s: %s' % (type(err).__name__, str(err)))
    exit(1)

# rootVIII
# pycodestyle validated
# last update: 27FEB2020


class S3Zilla:
    def __init__(self, master):
        try:
            self.s3 = boto3.resource('s3')
            self.s3c = boto3.client('s3')
        except Exception as err:
            print('%s: %s' % (type(err).__name__, str(err)))
            exit(1)

        light_gray = '#D9D9D9',
        blue = '#181B42',
        red = '#FF0000',
        black = '#000000',
        cyan = '#80DFFF'
        bold = 'Helvetica 10 bold underline'
        normal = 'Helvetica 10'
        rpath = realpath(__file__)[:-len(basename(__file__))]

        self.finish_thread = None
        self.greeting = 'Hello %s' % getuser()
        self.master = master
        self.master.title('Amazon S3 File Transfer Client')
        self.master.configure(bg=black)
        if platform != 'win32':
            self.master.geometry('695x700')
            self.icon = PhotoImage(file=rpath + 'icon.png')
            master.iconphoto(False, self.icon)
        else:
            self.master.geometry('485x700')
            self.master.iconbitmap(rpath + 'icon.ico')
        menu = Menu(self.master)
        menu.config(
            background=black,
            fg=light_gray
        )
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(
            label='Exit',
            command=self.quit
        )
        menu.add_cascade(
            label='File',
            menu=file
        )
        refresh = Menu(menu)
        refresh.add_command(
            label='Local',
            command=self.refresh_local
        )
        refresh.add_command(
            label='S3',
            command=self.refresh_s3
        )
        menu.add_cascade(label='Refresh', menu=refresh)
        self.dir, self.drp_sel, self.bucket_name = ['' for _ in range(3)]
        self.folder_path = StringVar()
        self.dropdown = StringVar()
        self.dropdown_data = self.populate_dropdown()
        if not self.dropdown_data:
            self.dropdown_data = ['none available']
        self.deleted = False
        self.local_sel, self.s3_sel = ([] for _ in range(2))

        self.local_label = Label(
            master,
            fg=light_gray,
            bg=black,
            text='LOCAL FILE SYSTEM',
            font=bold,
            width=24
        )
        self.local_label.grid(
            row=0,
            column=0,
            sticky=E+W,
            padx=10,
            pady=20
        )
        self.s3_label = Label(
            master,
            fg=light_gray,
            bg=black,
            text='AMAZON  S3',
            font=bold,
            underline=True,
            width=24
        )
        self.s3_label.grid(
            row=0,
            column=1,
            sticky=E+W,
            padx=10,
            pady=20
        )
        self.dropdown_box = OptionMenu(
            master,
            self.dropdown,
            *self.dropdown_data,
            command=self.set_drop_val
        )
        self.dropdown_box.configure(
            fg=light_gray,
            bg=blue,
            width=16,
            highlightbackground=black,
            highlightthickness=2
        )
        self.dropdown_box.grid(
            row=1,
            column=1,
            sticky=E+W,
            padx=52,
            pady=10
        )
        self.browse_button = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='Browse',
            width=16,
            highlightbackground=black,
            highlightthickness=2,
            command=self.load_dir
        )
        self.browse_button.grid(
            row=1,
            column=0,
            sticky=E+W,
            padx=52,
            pady=10
        )
        self.browse_label = Label(
            master,
            fg=light_gray,
            bg=black,
            text='No directory selected',
            width=24,
            font=normal
        )
        self.browse_label.grid(
            row=2,
            column=0,
            sticky=E+W,
            padx=10,
            pady=10
        )
        self.bucket_label = Label(
            master,
            fg=light_gray,
            bg=black,
            text='No bucket selected',
            width=24,
            font=normal
        )
        self.bucket_label.grid(
            row=2,
            column=1,
            sticky=E+W,
            padx=10,
            pady=10
        )
        self.refresh_btn_local = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='REFRESH',
            width=10,
            highlightbackground=black,
            highlightthickness=2,
            command=self.refresh_local
        )
        self.refresh_btn_local.grid(
            row=3,
            column=0,
            sticky=E+W,
            padx=50,
            pady=10
        )
        self.refresh_btn_s3 = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='REFRESH',
            width=10,
            highlightbackground=black,
            highlightthickness=2,
            command=self.refresh_s3
        )
        self.refresh_btn_s3.grid(
            row=3,
            column=1,
            sticky=E+W,
            padx=50,
            pady=10
        )

        self.ex_loc = Listbox(
            master,
            fg=cyan,
            bg=black,
            width=36,
            height=18,
            highlightcolor=black,
            selectmode='multiple'
        )
        self.ex_loc.grid(
            row=5,
            column=0,
            sticky=E+W,
            padx=10,
            pady=10
        )
        self.ex_s3 = Listbox(
            master,
            fg=cyan,
            bg=black,
            width=36,
            height=18,
            highlightcolor=black,
            selectmode='multiple'
        )
        self.ex_s3.grid(
            row=5,
            column=1,
            sticky=E+W,
            padx=10,
            pady=10
        )
        self.upload_button = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='Upload ->',
            width=14,
            highlightbackground=black,
            highlightthickness=2,
            command=self.upload
        )
        self.upload_button.grid(
            row=6,
            column=0,
            sticky=E,
            padx=10,
            pady=10
        )
        self.download_button = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='<- Download',
            width=14,
            highlightbackground=black,
            highlightthickness=2,
            command=self.download
        )
        self.download_button.grid(
            row=6,
            column=1,
            sticky=W,
            padx=10,
            pady=10
        )
        self.delete_local = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='DELETE',
            width=14,
            highlightbackground=red,
            activebackground=red,
            command=self.delete_local_records
        )
        self.delete_local.grid(
            row=6,
            column=0,
            sticky=W,
            padx=10,
            pady=10
        )
        self.delete_s3 = Button(
            master,
            fg=light_gray,
            bg=blue,
            text='DELETE',
            width=14,
            highlightbackground=red,
            activebackground=red,
            command=self.delete_s3_records
        )
        self.delete_s3.grid(
            row=6,
            column=1,
            sticky=E,
            padx=10,
            pady=10
        )
        self.found_label_local = Label(
            master,
            fg=light_gray,
            bg=black,
            text='found local',
            width=16
        )
        self.found_label_local.grid(
            row=7,
            column=0,
            sticky=E+W,
            padx=10,
            pady=10
        )
        self.found_label_s3 = Label(
            master,
            fg=light_gray,
            bg=black,
            text='found s3',
            width=16
        )
        self.found_label_s3.grid(
            row=7,
            column=1,
            sticky=E+W,
            padx=10,
            pady=10
        )
        self.status_label = Label(
            master,
            fg=light_gray,
            bg=black,
            text=self.greeting,
            width=8
        )
        self.status_label.grid(
            row=8,
            column=0,
            sticky=E + W,
            padx=10,
            pady=10
        )
        self.create_bucket_label = Label(
            master,
            fg=light_gray,
            bg=black,
            text='New Bucket:',
            width=10
        )
        self.create_bucket_label.grid(
            row=8,
            column=1,
            sticky=W,
            padx=1,
            pady=1
        )
        if platform != 'win32':
            self.create_bucket_name = Text(
                master,
                fg=cyan,
                bg=black,
                width=18,
                height=1
            )
            self.create_bucket_button = Button(
                master,
                fg=light_gray,
                bg=blue,
                text='Create',
                width=5,
                highlightbackground=black,
                highlightthickness=2,
                command=self.create_bucket
            )
        else:
            self.create_bucket_name = Text(
                master,
                fg=cyan,
                bg=black,
                width=11,
                height=1
            )
            self.create_bucket_button = Button(
                master,
                fg=light_gray,
                bg=blue,
                text='Create',
                width=7,
                highlightbackground=black,
                highlightthickness=2,
                command=self.create_bucket
            )
        self.create_bucket_name.grid(
            row=8,
            column=1,
            padx=1,
            pady=10
        )
        self.create_bucket_button.grid(
            row=8,
            column=1,
            sticky=E,
            padx=10,
            pady=10
        )

        n1 = '%s files found' % str(self.ex_loc.size())
        self.set_found_local_label(n1)
        n2 = '%s files found' % str(self.ex_s3.size())
        self.set_found_s3_label(n2)

    @staticmethod
    def quit():
        exit()

    def get_local_sel(self):
        return [self.ex_loc.get(i) for i in self.ex_loc.curselection()]

    def get_s3_sel(self):
        return [self.ex_s3.get(i) for i in self.ex_s3.curselection()]

    def set_drop_val(self, selection):
        self.drp_sel = selection

    def delete_local_records(self):
        files = self.get_local_sel()
        if not files:
            message = 'Please select a file(s) to delete'
            self.set_status_label(message)
        else:
            self.del_local(files)

    def del_local(self, files_remaining):
        if len(files_remaining) > 0:
            f = files_remaining.pop(0)
            if not isdir(self.dir + '/' + f):
                try:
                    remove('%s/%s' % (self.dir, f))
                except Exception as err:
                    self.set_status_label('%s' % err)
                self.del_local(files_remaining)
            else:
                try:
                    rmtree('%s/%s' % (self.dir, f))
                except Exception as err:
                    self.set_status_label('%s' % err)
                self.del_local(files_remaining)
        self.deleted = True
        self.refresh_local()

    def delete_s3_records(self):
        removal = ''
        if not self.drp_sel:
            m = 'Please select a bucket...'
            self.set_status_label(m)
        else:
            removal = self.get_s3_sel()
        if not removal:
            m = 'Please select at least 1 object to delete'
            self.set_status_label(m)
        else:
            bucket = self.s3.Bucket(self.drp_sel)
            for rm in removal:
                for k in bucket.objects.all():
                    if k.key != rm:
                        continue
                    k.delete()
                    break
            self.deleted = True
            self.refresh_s3()

    def load_dir(self):
        self.dir = askdirectory()
        if not isdir(self.dir):
            self.set_status_label('Ensure a directory is selected')
            self.dir = ''
        else:
            self.set_local_browse_label(self.dir)

    def refresh_local(self):
        if not self.dir:
            m = 'Use the browse button to select a directory'
            self.set_status_label(m)
        else:
            self.set_local_browse_label(self.dir)
            self.ex_loc.delete(0, 'end')
            x = self.dir + '/'
            d = [f if not isdir(x+f) else f + '/' for f in sorted(listdir(x))]
            self.ex_loc.insert('end', *d)
            if not self.deleted:
                m = self.greeting
            else:
                m = 'FINISHED DELETING'
                self.deleted = False
            self.set_status_label(m)
            n = '%s files found' % str(self.ex_loc.size())
            self.set_found_local_label(n)

    def refresh_s3(self):
        if 'none available' in self.dropdown_data:
            m = 'Please create at least one S3 bucket'
            self.set_status_label(m)
        elif not self.drp_sel:
            m = 'Please select a bucket from the drop-down list'
            self.set_status_label(m)
        else:
            self.ex_s3.delete(0, 'end')
            try:
                self.ex_s3.insert('end', *self.get_bucket_contents())
            except Exception:
                m = 'Unable to find bucket'
                self.set_status_label(m)
            else:
                self.set_status_label(self.greeting)
                self.set_s3_bucket_label(self.drp_sel)
                n = '%s files found' % str(self.ex_s3.size())
                self.set_found_s3_label(n)
                if not self.deleted:
                    m = self.greeting
                else:
                    m = 'FINISHED DELETING'
                    self.deleted = False
                self.set_status_label(m)

    def finish(self, incoming_message):
        d = 'FINISHED %s' % incoming_message
        for letter in enumerate(d):
            self.set_status_label(d[0:letter[0] + 1])
            sleep(.04)

    def upload(self):
        if not self.drp_sel or not self.dir:
            m = 'Ensure a local path and S3 bucket are selected'
            self.set_status_label(m)
        elif not self.get_local_sel():
            m = 'Ensure files are selected to upload'
            self.set_status_label(m)
        else:
            for selection in self.get_local_sel():
                file_ = '%s/%s' % (self.dir, selection)
                if not isdir(file_):
                    self.s3c.upload_file(file_, self.drp_sel, basename(file_))
                else:
                    zipd = make_archive(file_, 'zip', self.dir, selection)
                    self.s3c.upload_file(zipd, self.drp_sel, basename(zipd))
                    remove(zipd)
                m = 'Uploaded: %s' % selection
                self.set_status_label(m)
            self.refresh_s3()
            self.finish_thread = Thread(target=self.finish, args=['UPLOAD'])
            self.finish_thread.start()

    def download(self):
        if not self.drp_sel or not self.dir:
            m = 'Ensure a file and bucket have been selected'
            self.set_status_label(m)
        elif not self.get_s3_sel():
            m = 'Ensure files are selected to download'
            self.set_status_label(m)
        else:
            for selection in self.get_s3_sel():
                file_ = '%s/%s' % (self.dir, selection)
                self.s3c.download_file(self.drp_sel, selection, file_)
            self.refresh_local()
            self.finish_thread = Thread(target=self.finish, args=['DOWNLOAD'])
            self.finish_thread.start()

    def get_bucket_contents(self):
        bucket = self.s3.Bucket(self.drp_sel)
        return [s3_file.key for s3_file in bucket.objects.all()]

    def populate_dropdown(self):
        return [bucket.name for bucket in self.s3.buckets.all()]

    def set_local_browse_label(self, incoming):
        if len(incoming) > 35:
            self.browse_label.config(text=basename(incoming) + '/')
        else:
            self.browse_label.config(text=incoming)

    def set_s3_bucket_label(self, incoming):
        self.bucket_label.config(text=incoming)

    def set_status_label(self, incoming):
        self.status_label.config(text=incoming)
        self.status_label.update_idletasks()

    def set_found_local_label(self, incoming):
        self.found_label_local.config(text=incoming)
        self.found_label_local.update_idletasks()

    def set_found_s3_label(self, incoming):
        self.found_label_s3.config(text=incoming)
        self.found_label_s3.update_idletasks()

    def create_bucket(self):
        self.bucket_name = self.create_bucket_name.get('1.0', END).strip()
        if not self.bucket_name:
            m = 'Please enter a new bucket name'
            self.set_status_label(m)
        else:
            pre_exists = False
            try:
                self.s3.create_bucket(Bucket=self.bucket_name)
            except ClientError:
                pre_exists = True
                m = 'Bucket name is already in use. '
                m += 'Choose a different name.'
                self.set_status_label(m)
            if not pre_exists:
                m = '%s created: restarting...' % self.bucket_name
                self.set_status_label(m)
                self.status_label.update_idletasks()
                res = executable
                execl(res, res, *argv)

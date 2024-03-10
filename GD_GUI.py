import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image
import os
from GDriveUtils import GDriveUtils as gutils

class GUploadGUI:
    def __init__(self):

        self.root = tk.Tk()
        self.root.configure(background='#303030')
        self.root.configure(borderwidth=2, relief="ridge")
        self.root.title('GDrive Utility Tool')
        self.__token = 'D:/github/__Secrets/token.json'
        self.__client_secret_path = 'D:/github/__Secrets'
        self.root.geometry("480x450")  # Set initial window size

        # Import image
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, "Images/Logo.png").replace("\\", "/")
        orig_image = Image.open(image_path)
        scale=4
        scaled_image = orig_image.resize((orig_image.width//scale,orig_image.height//scale))
        scaled_image_path = 'scaled_image_path.png'
        scaled_image.save(scaled_image_path)

        self.photoImage = PhotoImage(file=scaled_image_path)

        # Create menu bar
        self.menubar = tk.Menu(self.root, bg='#000000')

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=self.on_closing)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label='Close Without Question', command=exit)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label='Copy ID', command=self.copy_to_clipboard)

        self.menubar.add_cascade(menu=self.filemenu, label='File')
        self.menubar.add_cascade(menu=self.actionmenu, label='Action')

        self.root.config(menu=self.menubar)

        self.image_label = tk.Label(self.root, image=self.photoImage,bg='#303030')
        self.image_label.grid(row=0, column=0,columnspan=1, padx=0, pady=0,sticky=tk.W)

        # Create radio buttons
        self.radio_var = tk.StringVar()
        self.radio_var.set("Upload")
        self.upload_radio = tk.Radiobutton(self.root, text="Upload", variable=self.radio_var, value="Upload",
                                           font=('Arial', 12), bg='#303030', fg='white', selectcolor='#303030',
                                           command=self.toggle_mode)
        self.upload_radio.grid(row=0, column=0,columnspan=2, padx=150, pady=10,sticky=tk.W)

        self.download_radio = tk.Radiobutton(self.root, text="Download", variable=self.radio_var, value="Download",
                                             font=('Arial', 12), bg='#303030', fg='white', selectcolor='#303030',
                                             command=self.toggle_mode)
        self.download_radio.grid(row=0, column=1, padx=0, pady=10, sticky=tk.W)

        # Create File Dialog
        self.file_dialog_entry = tk.Entry(self.root, width=35, font=('Arial', 12))
        self.file_dialog_entry.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.file_button = tk.Button(self.root, width=12, text='File To Upload', font=('Georgia', 10), fg='white',
                                     bg='#4c9c5c', command=self.open_file_dialog)
        self.file_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Create Folder in GDrive textbox
        self.fold_textbox = tk.Text(self.root, width=35, height=1.0, font=('Arial', 12, 'bold'), bg='white', fg='black',
                               state='normal')
        self.fold_textbox.grid(row=2, column=0, columnspan=1, padx=10, pady=0, sticky=tk.W)
        self.fold_textbox.bind("<Return>", self.prevent_clear)

        self.label = tk.Label(self.root, text=": Gdrive Folder", font=('Arial', 12, 'bold'), bg='#303030', fg='#ffff9f')
        self.label.grid(row=2, column=1, padx=0, pady=0, sticky=tk.W)

        # Create check button
        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, bg='#303030',font=('Ariel',16), variable=self.check_state)
        self.check.grid(row=3, column=0, columnspan=1, padx=0, pady=10, sticky=tk.E)

        self.check_label = tk.Label(self.root, text="  Publish as Local Path : ", font=('Arial', 12, 'bold'),
                                    bg='#303030', fg='#ffff9f')
        self.check_label.grid(row=3, column=0, padx=0, pady=10, sticky=tk.W)

        # Create textbox
        # self.canvas = tk.Canvas(self.root,width=10, bg='#000000')
        # self.canvas.grid(row=4, column=0, columnspan=2, padx=30, pady=10,sticky=tk.W)
        self.out_textbox = tk.Text(self.root, width=65, height=5, font=('Arial', 10), bg='black', fg='white',
                               state='disabled')
        self.out_textbox.grid(row=4, column=0, columnspan=2, padx=10, pady=2)



        # Create button
        self.button = tk.Button(self.root, text='Upload', width=10,height=1, font=('Helvetica', 12), fg='white', bg='#5c5c5c', highlightthickness=2, relief='raised', command=self.asset_upload)
        self.button.grid(row=5, column=0, columnspan=2, padx=50, pady=15,sticky=tk.W+tk.E)

        self.root.protocol('WM_DELETE_WINDOW', exit)

        self.root.mainloop()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_dialog_entry.config(state='normal')
            self.file_dialog_entry.delete(0, tk.END)
            self.file_dialog_entry.insert(0, file_path)
            self.file_dialog_entry.config(state='readonly')

    def prevent_clear(self, event):
        # Prevent clearing the textbox by returning 'break'
        return 'break'

    def copy_to_clipboard(self):
        text = self.out_textbox.get('1.0',tk.END)
        self.root.clipboard_clear()  # Clear the clipboard
        self.root.clipboard_append(text)  # Append the text to the clipboard
        messagebox.showinfo("Clipboard", "Text copied to clipboard")

    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message='Do you really want to quit?'):
            self.root.destroy()

    def toggle_mode(self):
        # Add logic here to adjust the interface based on selected mode
        pass

    def asset_upload(self):
        asset_path = self.file_dialog_entry.get()
        gd_folder = self.fold_textbox.get('1.0',tk.END)
        val = int(self.check_state.get())

        data_val = gutils(self.__client_secret_path,self.__token,asset_path,gd_folder)
        output=data_val.upload_file(val)

        # Clear the current content of the out_textbox
        self.out_textbox.config(state='normal')
        self.out_textbox.delete('1.0', tk.END)
        # Insert the output into the out_textbox
        self.out_textbox.insert('1.0', output)

        # Disable the out_textbox to prevent editing
        self.out_textbox.config(state='disabled')
g = GUploadGUI()



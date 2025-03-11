import validators
import os
import royalroad
import email_function
import threading

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno

main_url = 'https://www.royalroad.com'

class Novel2EPUB:
    def __init__(self, root):
        self.root = root
        self.root.title("Novel2EPUB")
        self.root.resizable(False, False)

        window_width = 400
        window_height = 200

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.label = ttk.Label(self.root, text="Please enter a novel title or url.")
        self.label.pack(ipadx=10, ipady=10)

        self.entry = ttk.Entry(self.root, width=50)
        self.entry.pack(padx=20, pady=10)
        self.root.iconbitmap('./assets/icon.ico')
        self.kindle_checkbox = tk.BooleanVar(value=False) 
        self.phone_checkbox = tk.BooleanVar(value=False)

        ttk.Checkbutton(root,  
                text="Send to Kindle", 
                variable=self.kindle_checkbox,
                onvalue=True,
                offvalue=False).pack()
        
        ttk.Checkbutton(root,
                text="Send to Phone",
                variable=self.phone_checkbox,
                onvalue=True,
                offvalue=False).pack()

        self.button = ttk.Button(self.root, text="Download", command=self.on_click)
        self.button.pack(padx=20, pady=10)

        self.progress_bar = ttk.Progressbar(root,
                                orient = "horizontal",
                                mode="indeterminate",
                                length=280)

        self.book_title = None

        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    def create_thread(self, target_function, arguments):
        thread = threading.Thread(target=target_function, args=arguments)
        thread.start()
    
    def kindle_box_ticked(self):
        if not os.path.exists("config.txt"):
            showinfo(title="Error", message="Config file not found. Please run setup batch file.")
            return
        
        with open("config.txt", "r") as f:
            kindle_email = f.readline()
            phone_address = f.readline()
            if(kindle_email == "N/A"):
                showinfo(title="Error", message="Kindle email not found in config file. Please run the setup batch file again.")
                os.remove("config.txt")
                return
            else:
                email_function.send_email(kindle_email, f'{self.book_title}.epub')
                self.on_success()
    
    def phone_box_ticked(self):
        if not os.path.exists("config.txt"):
            showinfo(title="Error", message="Config file not found. Please run setup batch file.")
            return
        
        with open("config.txt", "r") as f:
            kindle_email = f.readline()
            phone_address = f.readline()
        
        if(phone_address == "N/A"):
                showinfo(title="Error", message="Phone number not found in config file. Please run the setup batch file again.")
                os.remove("config.txt")
                return
        else:
            email_function.send_email(phone_address, f'{self.book_title}.epub')
            self.on_success()
    
    def start_download(self, user_input):
        if validators.url(user_input):
            self.progress_bar.pack()
            self.progress_bar.start()
            book_title = royalroad.fetch_title(royalroad.make_request(user_input))
            self.book_title = book_title
            self.checkbox_check()

        else:
            book_title, book_url = royalroad.search(royalroad.make_request(f'{main_url}/fictions/search?globalFilters=false&title={user_input}&orderBy=popularity'))
            self.book_title = book_title
            answer = askyesno(title='Confirmation',
                            message=f'Is {book_title} ({book_url}) the novel you are looking for?'
                            )

            if(answer):
                self.progress_bar.pack() 
                self.progress_bar.start()
                royalroad.pack_epub(book_url)
                self.checkbox_check()

            else:
                showinfo(title="Notice", message="Try re-entering the title in a more complete manner. (ex. mother -> mother of learning) or entering the url directly.")
                return 
            
    def on_click(self):
        user_input = self.entry.get()
        self.create_thread(self.start_download, (user_input,)) 
    
    def checkbox_check(self):
        if self.kindle_checkbox.get(): 
            self.create_thread(self.kindle_box_ticked, ())

        if self.phone_checkbox.get():
            self.create_thread(self.phone_box_ticked, ())

    def on_success(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        showinfo(title="Success!", message=f"{self.book_title} successfully downloaded.")
        return

def main():
    root = tk.Tk()
    app = Novel2EPUB(root)
    root.mainloop()

if __name__ == "__main__":
    main()
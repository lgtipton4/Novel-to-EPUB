# OVERALL TODO
# Implement automated updates
# Implement tray with pstray
# Implement history section in window and "resend" button.
# Add automated sending to iPhone via vtext. User can setup with phone number 

import validators
import os
import royalroad
import email_function

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

        window_width = 346
        window_height = 146

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.label = ttk.Label(self.root, text="Please enter a novel title or url.")
        self.label.pack(ipadx=10, ipady=10)

        self.entry = ttk.Entry(self.root, width=50)
        self.entry.pack(padx=20, pady=10)
        self.root.iconbitmap('./assets/icon.ico')
        self.checkbox = tk.BooleanVar(value=False) 

        ttk.Checkbutton(root,  
                text="Send to Kindle", 
                variable=self.checkbox,
                onvalue=True,
                offvalue=False).pack()

        self.button = ttk.Button(self.root, text="Submit", command=self.on_click)
        self.button.pack(padx=20, pady=10)

        self.book_title = None

        self.root.geometry(f"346x146+{center_x}+{center_y}")

    def box_ticked(self):
        if not os.path.exists("config.txt"):
            showinfo(title="Error", message="Config file not found. Please run setup batch file.")
            return
        
        with open("config.txt", "r") as f:
            kindle_email = f.readline()
            if(kindle_email == "N/A"):
                showinfo(title="Error", message="Kindle email not found in config file. Please run the setup batch file again.")
                os.remove("config.txt")
                return
            else:
                print(kindle_email)
                email_function.send_email(kindle_email, f'{self.book_title}.epub')

    def on_click(self):
        user_input = self.entry.get()
        if validators.url(user_input):
            book_title = royalroad.fetch_title(royalroad.make_request(user_input))
            self.book_title = book_title
            royalroad.pack_epub(user_input)

        else:
            book_title, book_url = royalroad.search(royalroad.make_request(f'{main_url}/fictions/search?globalFilters=false&title={user_input}&orderBy=popularity'))
            self.book_title = book_title
             #print(self.book_title)
            answer = askyesno(title='Confirmation',
                            message=f'Is {book_title} ({book_url} the novel you are looking for?)'
                            )

            if(answer):
                royalroad.pack_epub(book_url)

            else:
                showinfo(title="Notice", message="Try re-entering the title in a more complete manner. (ex. mother -> mother of learning) or entering the url directly.")

        if self.checkbox.get(): 
            self.box_ticked()
        
        showinfo(title="Success!", message=f"{book_title} successfully downloaded.")

def main():
    root = tk.Tk()
    app = Novel2EPUB(root)
    root.mainloop()

if __name__ == "__main__":
    main()
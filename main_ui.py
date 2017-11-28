import xliff_tool
# Python 3
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, askopenfilenames

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.clean_label = tk.Label(self, 
        text = 'Select one or more files to clean translation')
        self.clean_label.pack(side='top')

        self.browse = tk.Button(self)
        self.browse["text"] = "Clean xliff file.."
        self.browse["command"] = self.clean_xliff
        self.browse.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def clean_xliff(self):
        names = askopenfilenames(filetypes=[('xliff files', '.xliff')])
        for name in names:
            editor = xliff_tool.XliffEditor(name)
            editor.better_clean()
        self.clean_label['text'] = 'Clean completed'

 
root = tk.Tk()
root.title("nstring tools")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%sx%s' % (width//3, height//3))

app = Application(master=root)
app.mainloop()

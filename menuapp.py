from tkinter import Menu
from tkinter import messagebox

#ws =Tk()
#ws.title("Python Guides")
#ws.geometry("300x250")

def about():
    messagebox.showinfo('Ecompanions', 'Your guide to companion plants')

def setMenus(ws1):
    menubar = Menu(ws1, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
    file = Menu(menubar, tearoff=0, background='#ffcc99', foreground='black')
    file.add_command(label="New")
    file.add_command(label="Open")
    file.add_command(label="Save")
    file.add_command(label="Save as")
    file.add_separator()
    file.add_command(label="Exit", command=ws1.quit)
    menubar.add_cascade(label="File", menu=file)

    edit = Menu(menubar, tearoff=0)
    edit.add_command(label="Undo")
    edit.add_separator()
    edit.add_command(label="Cut")
    edit.add_command(label="Copy")
    edit.add_command(label="Paste")
    menubar.add_cascade(label="Edit", menu=edit)

    node = Menu(menubar, tearoff=0)
    node.add_command(label="New")
    node.add_command(label="Edit")
    node.add_command(label="Remove")
    node.add_command(label="Show list")
    menubar.add_cascade(label="Node", menu=node)

    link = Menu(menubar, tearoff=0)
    link.add_command(label="New")
    link.add_command(label="Edit")
    link.add_command(label="Remove")
    link.add_command(label="Show list")
    menubar.add_cascade(label="Link", menu=link)

    network = Menu(menubar, tearoff=0)
    network.add_command(label="New")
    network.add_command(label="Edit")
    network.add_command(label="Remove")
    network.add_command(label="Show catalog")
    menubar.add_cascade(label="Network", menu=network)

    help = Menu(menubar, tearoff=0)
    help.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=help)
    return menubar

#ws.config(menu=setMenus(ws))
#ws.mainloop()
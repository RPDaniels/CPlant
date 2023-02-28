#import tkinter as tk
from tkinter import messagebox, ttk, Label, Entry, Button, Toplevel
import sqlcplants
import canvasutils

data = []

def on_submit():
    nombre = nombre_entry.get()
    nombre_latin = nombre_latin_entry.get()
    nombre_español = nombre_español_entry.get()
    padre = padre_entry.get()
    tipo = tipo_entry.get()

    data = [padre, tipo, nombre, nombre_latin, nombre_español]
    if all(data):
        sqlcplants.savenode(data)
        messagebox.showinfo(l.get("Data introduced"),
            f"{l.get('Name')}: {nombre}\n"
            f"{l.get('Latin name')}: {nombre_latin}\n"
            f"{l.get('Spanish name')}: {nombre_español}\n"
            f"{l.get('Parent')}: {padre}\n"
            f"{l.get('Type')}: {tipo}")
        dialog.destroy()
        # Actualizar combo1 y refrescar
    else:
        messagebox.showinfo(l.get("Error introducing data"),l.get("Please fill in all data"))

def on_delete():
    name = nombre_entry.get()
    isDeleted = False
    confirmation = messagebox.askyesno(l.get("Delete plant?"), l.get("You are going to delete plant")+" " + name)
    if confirmation:
        sqlcplants.deletenode(name)
        isDeleted = True
        messagebox.showinfo(l.get("Deleting plant"),l.get("Plant deleted")+": "+ name)
    dialog.destroy()
    return isDeleted


def getPlantDataByName(name):
    nodeObject = sqlcplants.getNodeByName(name)
    latin = nodeObject.name_lat
    esp = nodeObject.name_es
    parent = nodeObject.parent
    type = nodeObject.type
    return latin, esp, parent, type

def open_edit_dialog(lang,name):
    global l
    l = lang
    if len(name)>0:
        latin, esp, parent, type = getPlantDataByName(name)
        data = nodeDialog(name, latin, esp, parent, type)
    else:
        data = open_dialog()
    return data

def open_dialog(lang):
    global l
    l = lang
    data = nodeDialog("","","","","")
    return data



def nodeDialog(name, latin, esp, parent, type):
    global dialog
    dialog = Toplevel()
    dialog.title(l.get("Plant"))

    dialog.update()
    x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2
    y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2
    dialog.geometry("+%d+%d" % (x, y))

    # -------------
    image = canvasutils.getImage(name)

    # Create a label to display the image
    labelImage = Label(dialog, image=image)
    labelImage.image = image  # keep a reference!

    # Center the label in the window
    labelImage.grid(row=0, column=0, sticky="w")
        #.place(relx=0.5, rely=0.5, anchor="center")

    #----------------
    nombre_label = Label(dialog, text=l.get("Name")+":")
    nombre_label.grid(row=1, column=0, sticky="w")

    global nombre_entry
    nombre_entry = Entry(dialog)
    nombre_entry.insert(0, name)
    nombre_entry.grid(row=1, column=1, sticky="w")

    # -------------
    nombre_latin_label = Label(dialog, text=l.get("Latin name")+":")
    nombre_latin_label.grid(row=2, column=0, sticky="w")

    global nombre_latin_entry
    nombre_latin_entry = Entry(dialog)
    nombre_latin_entry.insert(0, latin)
    nombre_latin_entry.grid(row=2, column=1, sticky="w")


    # -------------
    nombre_español_label = Label(dialog, text=l.get("Spanish name")+":")
    nombre_español_label.grid(row=3, column=0, sticky="w")

    global nombre_español_entry
    nombre_español_entry = Entry(dialog)
    nombre_español_entry.insert(0, esp)
    nombre_español_entry.grid(row=3, column=1, sticky="w")

    # -------------
    padre_label = Label(dialog, text=l.get("Parent")+":")
    padre_label.grid(row=4, column=0, sticky="w")

    global padre_entry
    padre_entry = ttk.Combobox(dialog, values=["Alliacaea", "Brassicacaea", "Cucurbitacaea", "Leguminosae",
                                               "Solanacaea","Vegetables","Herbs","Grains","Flowers","Fruit",
                                               "Wild plants"])
    padre_entry.set(parent)
    padre_entry.grid(row=4, column=1, sticky="w")

    # -------------
    tipo_label = Label(dialog, text="Type:")
    tipo_label.grid(row=5, column=0, sticky="w")

    global tipo_entry
    tipo_entry = ttk.Combobox(dialog, values=["Species"])
    tipo_entry.set(type)
    tipo_entry.grid(row=5, column=1, sticky="w")

    # -------------

    submit_button = Button(dialog, text=l.get("Save"), command=on_submit)
    submit_button.grid(row=6, column=0, pady=10)
    submit_button = Button(dialog, text=l.get("Delete"), command=on_delete)
    submit_button.grid(row=6, column=1, pady=10)
    cancel_button = Button(dialog, text=l.get("Cancel"), command=dialog.destroy)
    cancel_button.grid(row=6, column=2, pady=10)


    return data


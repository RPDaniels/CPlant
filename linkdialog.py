import tkinter as tk
from tkinter import ttk, messagebox
import sqlcplants
import canvasutils

def dialog(lang):
    global l
    l=lang
    #global labelImagePrimary
    def update_popup(primary_name, companion_name):
        if l.lang!="en":
            primary_name = l.rget(primary_name)
            companion_name = l.rget(companion_name)
        node_primary = sqlcplants.getNodeByName(primary_name)
        node_companion = sqlcplants.getNodeByName(companion_name)
        linkId = sqlcplants.getLink(node_primary, node_companion)
        if linkId.id > 0:
            strength_entry.set(linkId.strength)
            description_entry.set(linkId.description)
        else:
            strength_entry.set("")
            description_entry.set("")

    def select_primary_combo(event):
        primary_name = primary_combo.get()
        companion_name = companion_combo.get()
        if l.lang!="en":
            imagename = l.rget(primary_name)
        else:
            imagename = primary_name
        image_primary = canvasutils.getImage(imagename)
        labelImagePrimary.config(image=image_primary)
        labelImagePrimary.image = image_primary

        update_popup(primary_name, companion_name)

    def select_companion_combo(event):
        primary_name = primary_combo.get()
        companion_name = companion_combo.get()
        if l.lang!="en":
            imagename = l.rget(companion_name)
        else:
            imagename = companion_name
        image_companion = canvasutils.getImage(imagename)
        labelImageCompanion.config(image=image_companion)
        labelImageCompanion.image = image_companion

        update_popup(primary_name, companion_name)

    def on_accept():
        primary = primary_combo.get()
        companion = companion_combo.get()
        strength = strength_entry.get()
        description = description_entry.get()
        data = [primary, companion, strength, description]
        if all(data):
            sqlcplants.savelink(data)
            messagebox.showinfo(l.get("Datos introducidos",
                                f"{l.get('Primary')}: {primary}\n"\
                                f"{l.get('Companion')}: {companion}\n"\
                                f"{l.get('Strength')}: {strength}\n"\
                                f"{l.get('Description')}: {description}"))
            dialog.destroy()

    def on_cancel():
        dialog.destroy()

    def on_delete():
        primary = primary_combo.get()
        companion = companion_combo.get()
        confirmation = messagebox.askyesno(l.get("Delete link?"), l.get("You are going to delete the link between primary:") +
                                           " " + primary + " "+l.get("and companion:")+" " + companion)
        if confirmation:
            sqlcplants.deleteLinkByNodeNames(primary,companion)
            messagebox.showinfo(l.get("Link deleted"), f"{l.get('Link deleted between:')}\n" \
                                                f"{l.get('Primary')}: {primary}\n" \
                                                f"{l.get('Companion')}: {companion}\n")
            dialog.destroy()

    #root = tk.Tk()
    #root.title("Pop-up")
    dialog = tk.Toplevel()
    dialog.title(l.get("Edit Link"))

    dialog.update()
    x = (dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2
    y = (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2
    dialog.geometry("+%d+%d" % (x, y))


    speciesList = sqlcplants.getSpeciesList(l)
    speciesList.insert(0,l.get("(Select)"))
    #primary_combo['values'] = tuple(speciesList)

    # Create primary combo box
    nombre_label = tk.Label(dialog, text=l.get("Primary")+":")
    nombre_label.grid(row=0, column=0, sticky="w")

    primary_combo = ttk.Combobox(dialog, values=tuple(speciesList))
    primary_combo.current(0)  # set the selected item
    primary_combo.grid(row=0, column=1, sticky="w")

    # Create companion combo box
    nombre_label2 = tk.Label(dialog, text=l.get("Companion")+":")
    nombre_label2.grid(row=1, column=0, sticky="w")

    companion_combo = ttk.Combobox(dialog, values=tuple(speciesList))
    companion_combo.current(0)
    companion_combo.grid(row=1, column=1, sticky="w")

    # Create strength entry field
    nombre_label3 = tk.Label(dialog, text=l.get("Strength")+":")
    nombre_label3.grid(row=2, column=0, sticky="w")

    strength_entry = ttk.Combobox(dialog, values=["-4","-3","-2","-1","","1","2","3","4"])
    strength_entry.current(4)
    strength_entry.grid(row=2, column=1, sticky="w")

    #Create icons ###################################
    image = canvasutils.getImage("default")
    global labelImagePrimary
    labelImagePrimary = tk.Label(dialog, image=image)
    labelImagePrimary.image = image  # keep a reference!
    labelImagePrimary.grid(row=0, column=3, rowspan=3, sticky="w")

    arrow = canvasutils.getImage("left_arrow")
    labelArrow = tk.Label(dialog, image=arrow) #, image=image
    labelArrow.image = arrow  # keep a reference!
    labelArrow.grid(row=0, column=4, rowspan=3, sticky="w")

    labelImageCompanion = tk.Label(dialog, image=image) #, image=image
    labelImageCompanion.image = image  # keep a reference!
    labelImageCompanion.grid(row=0, column=5, rowspan=3, sticky="w")
    ##################################################

    # Create description entry field
    linktypeslist = sqlcplants.getLinkTypesDescriptions()
    linktypeslist.insert(0, l.get("(Select)"))

    nombre_label4 = tk.Label(dialog, text=l.get("Description")+":")
    nombre_label4.grid(row=3, column=0, sticky="w")

    description_entry = ttk.Combobox(dialog, width=60, values=tuple(linktypeslist))
    description_entry.current(0)
    description_entry.grid(row=3, column=1, sticky="w", columnspan=5)

    # Create accept and cancel buttons
    accept_button = tk.Button(dialog, text=l.get("Accept"), command=on_accept)
    accept_button.grid(row=4, column=1, sticky="e")

    cancel_button = tk.Button(dialog, text=l.get("Cancel"), command=on_cancel)
    cancel_button.grid(row=4, column=2, sticky="w")

    delete_button = tk.Button(dialog, text=l.get("Delete link"), command=on_delete)
    delete_button.grid(row=4, column=3, sticky="w")

    primary_combo.bind("<<ComboboxSelected>>", select_primary_combo)
    companion_combo.bind("<<ComboboxSelected>>", select_companion_combo)

#import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import ttk, Tk, Button, Frame, Canvas, Scrollbar
import sqlcplants
import compcanvas
import ecocanvas
import canvasutils
import dialogonode
import linkdialog
import menuapp
import recommendations

ecosystem = []
ecosystemLinks = []
item = 0
moved = bool(False)

def framewin():

    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    compwidth = 100 * 10 #comp.squareside * comp.maxcolumns
    #canvasWidth = screen_width

    ############# Window Layout: Top frame + bottom left frame + canvas + bottom right frame + canvas2:
    root.title("CPlants creación de ecosistema")
    root.state('zoomed')
    root.config(menu=menuapp.setMenus(root))

    # Frame for comboboxes
    top_frame = Frame(root)
    top_frame.pack(side="top", fill="both", expand=True)

    # Frame for displaying plants
    left_frame = Frame(root)
    canvas = Canvas(left_frame, bg="white", width=compwidth, height=screen_height)
    scrollbar = Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="left", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set) #, scrollregion=(0, 0, 0, 3300))
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    left_frame.pack(side="left", fill="both", expand=True)

    # Frame for displaying ecosystems -------------------------
    right_frame = Frame(root)
    canvas2 = Canvas(right_frame, bg="white", width=int(screen_width/2), height=screen_height*2)
    scrollbar_right = ttk.Scrollbar(right_frame, orient="vertical", command=canvas2.yview)
    scrollbar_right.pack(side="right", fill="both")
    canvas2.config(yscrollcommand=scrollbar_right.set)
    canvas2.pack(fill="both", expand=True)
    right_frame.pack(side="right", fill="both", expand=True)

    comp = compcanvas.Compcanvas(canvas)
    eco = ecocanvas.Ecocanvas(canvas2)
    eco.set([],[])

    currentcanvas = canvas

    ############# Binding functions for top frame: #################################3

    def addCurrentCompanionToEcosystem():
        global ecosystem
        global ecosystemLinks
        companion = combo1.get()
        if companion != "All":
            ecosystem, ecosystemLinks = eco.addCompanionToEcosystem(companion)
            refreshCanvas2()
        #refreshCanvas()

    def removeCurrentCompanionFromEcosystem():
        global ecosystem
        global ecosystemLinks
        ecosystem, ecosystemLinks = eco.removeCompanionFromEcosystem(combo1.get())
        refreshCanvas2()
        #refreshCanvas()

    def saveEcosystem():
        ecoName = eco.saveEcosystem(combo2.get())
        list = eco.getecosystemcombolist()
        combo2['values'] = list
        if ecoName != None:
            combo2.current(combo2['values'].index(ecoName))
        #refreshCanvas2()

    def deleteEcosystem():
        eco.deleteEcosystem(combo2.get())
        list = eco.getecosystemcombolist()
        combo2['values'] = list
        combo2.current(0)
        refreshCanvas2()
        # refresh combo2


    def refreshCanvas(): # Reload all or species companions into canvas
        canvas.delete("all")
        #canvas.yview_moveto(0)
        global ecosystem
        nodeIdsList = []
        for node in ecosystem:
            nodeIdsList.append(node.id)
        #print("nodeIdsList:", nodeIdsList)
        if len(nodeIdsList) > 0:
            relations = recommendations.getEcosystemCompanionsHash(nodeIdsList)
        else: relations = {}
            #print("relations:",relations)
        numspecies = comp.refreshSpecies(combo1.get(),relations)
        #print("Num. especies:",numspecies)
        canvas.configure(scrollregion=canvas.bbox("all"))

    def refreshCanvas2(): #Reload ecosystem into canvas2
        canvas2.delete("all")
        canvas2.yview_moveto(0)
        eco.drawEcosystemCircle() # ecosystem under construction
        canvas2.configure(scrollregion=canvas2.bbox("all"))

    def select_combo1(choice): # Reload all or species companions into canvas
        refreshCanvas()

    def select_combo2(choice): # Load ecosystem into screen
        global ecosystem, ecosystemLinks
        ecosystem, ecosystemLinks = eco.loadEcosystemByName(combo2.get())
        refreshCanvas2()
        refreshCanvas()

    def addSpeciesToCatalog():
        dialogonode.open_dialog()
        root.wait_window(dialogonode.dialog)
        speciesList = sqlcplants.getSpeciesList()
        speciesList.insert(0, "All")
        #print(speciesList)
        combo1['values'] = tuple(speciesList)
        #combo1.current(0)  # set All
        refreshCanvas()

    def editNode():
        companion = combo1.get()
        dialogonode.open_edit_dialog(companion)
        root.wait_window(dialogonode.dialog)
        speciesList = sqlcplants.getSpeciesList()
        speciesList.insert(0, "All")
        combo1['values'] = tuple(speciesList)
        refreshCanvas()

    def showAllCatalog():
        #sqlcplants.getLinkMatrix()
        combo1.current(0)  # set All
        refreshCanvas()

    def showRecommendations():
        nodeIdsList = []
        for node in ecosystem:
            nodeIdsList.append(node.id)
        if len(nodeIdsList)>0:
            recommendations_list = recommendations.getRecommendationsList(nodeIdsList)
            canvas.delete("all")
            comp.loadNodeNamesList(recommendations_list)
            canvas.configure(scrollregion=canvas.bbox("all"))

    def showThreats():
        nodeIdsList = []
        for node in ecosystem:
            nodeIdsList.append(node.id)
        if len(nodeIdsList)>0:
            threats_list = recommendations.getRecommendationsList(nodeIdsList, type="negative")
            canvas.delete("all")
            comp.loadNodeNamesList(threats_list, color="indianred")
            canvas.configure(scrollregion=canvas.bbox("all"))

    def moveIcons():
        global moving
        moving = True
        for i in range(10):
            eco.drawMovingEcosystem()
        #balance.moveIcons(ecosystemLinks, canvas2)

    def linkPopUp():
        linkdialog.dialog()

    ########### Top frame layout: ###########################################################

    # Combo with list of plants
    combo1 = Combobox(top_frame)
    speciesList = sqlcplants.getSpeciesList()
    speciesList.insert(0,"All")
    combo1['values'] = tuple(speciesList)
    combo1.current(0)  # set the selected item
    combo1.grid(column=0, row=0)

    # Combo with list of ecosystems
    combo2 = Combobox(top_frame)
    ecosystemList = sqlcplants.getEcosystemsList()
    ecosystemList.insert(0,"(Select a ecosystem)")
    combo2['values'] = tuple(ecosystemList)
    combo2.current(0)  # set the selected item
    combo2.grid(column=3, row=0)

    combo1.bind("<<ComboboxSelected>>", select_combo1)
    combo2.bind("<<ComboboxSelected>>", select_combo2)

    # Button "Add->"
    btn1 = Button(top_frame, text='Add to Eco->', width=12, height=1, bd='2', command=addCurrentCompanionToEcosystem)
    btn1.grid(column=1, row=0)

    # Button "<-Remove"
    btn2 = Button(top_frame, text='<-Remove from Eco', width=16, height=1, bd='2', command=removeCurrentCompanionFromEcosystem)
    btn2.grid(column=2, row=0)

    # Button "Save"
    btn3 = Button(top_frame, text='Save Eco', width=10, height=1, bd='2', command=saveEcosystem)
    btn3.grid(column=4, row=0)

    # Button "Delete"
    btn4 = Button(top_frame, text='Delete Eco', width=10, height=1, bd='2', command=deleteEcosystem)
    btn4.grid(column=5, row=0)

    # Button "New Plant"
    button_newnode = Button(top_frame, text="New plant", width=10, height=1, bd='2', command= addSpeciesToCatalog)
    button_newnode.grid(column=6, row=0)

    # Button "Edit plant"
    button_move = Button(top_frame, text="Edit plant", width=12, height=1, bd='2', command= editNode)
    button_move.grid(column=7, row=0)

    # Button "Show catalog"
    button_allnodes = Button(top_frame, text="Show catalog", width=13, height=1, bd='2', command= showAllCatalog)
    button_allnodes.grid(column=8, row=0)

    # Button "Show recommendations"
    button_recommend = Button(top_frame, text="Show recommendations", width=20, height=1, bd='2', command= showRecommendations)
    button_recommend.grid(column=9, row=0)

    # Button "Show Threats"
    button_threat = Button(top_frame, text="Show threats", width=15, height=1, bd='2', command= showThreats)
    button_threat.grid(column=10, row=0)

    # Button "Move"
    button_move = Button(top_frame, text="Move Eco", width=12, height=1, bd='2', command= moveIcons)
    button_move.grid(column=11, row=0)

    # Button "Edit link"
    button_move = Button(top_frame, text="Link", width=12, height=1, bd='2', command= linkPopUp)
    button_move.grid(column=12, row=0)
    linkPopUp

    ########### Binding functions for canvases #################################:

    def on_enter_canvas2(choice):
        global currentcanvas
        currentcanvas = canvas2

    def on_enter_canvas(choice):
        global currentcanvas
        currentcanvas = canvas

    def select_item(event): # Select icon in catalog
        global currentcanvas
        item = pick_image(event, currentcanvas)
        companionName = canvasutils.getImageLabel(currentcanvas, item)
        if companionName in combo1['values']:
            combo1.set(companionName)  # Actualizar el combo para cargar la especie clicada
            refreshCanvas()
        return item

    def pick_image(event, mycanvas): # returns and item from a picked icon
        global moved
        moved = bool(False)
        global item
        item = 0
        halo = 20
        xcanvas = mycanvas.canvasx(event.x)
        ycanvas = mycanvas.canvasy(event.y)
        objectlist = mycanvas.find_overlapping(xcanvas-halo, ycanvas-halo, xcanvas+halo, ycanvas+halo)
        for i in objectlist:
            if contains(mycanvas.gettags(i), 'icon'):
                #print("Icono encontrado:",mycanvas.gettags(i))
                item = i
                mycanvas.tag_raise(i)
                break
        return item

    def contains(tuple, given_char):
        for ch in tuple:
            if ch == given_char:
                return True
        return False

    def click_canvas2(event): # Click on icon from ecosystem
        global moved
        moved = bool(False)
        global item
        if event.y < eco.getEcoDrawingHeight():
            item =  canvas2.find_closest(event.x, event.y)[0]
                #pick_image(event, canvas2)
            canvas2.tag_raise(item)
        else: item = 0


    def move_image(event): # Drag icon in ecosystem
        global moved
        global item
        moved = bool(True)
        if item>0:
            #print("item in move_image:",item)
            #item = canvas2.find_closest(event.x, event.y)[0] #OJO
            #pick_image(event, canvas2)
            x, y = canvas2.coords(item)
            x1, y1 = canvasutils.limitCoordinates(event.x, event.y, canvas2)
            name = canvasutils.getImageLabel(canvas2, item)
            canvasutils.moveImage(name, x1-x, y1-y, canvas2)
            eco.refreshLinks(eco.getIconHash())

    def on_release_button(event): # Release icon in ecosystem
        global item
        global moved
        if moved:
            pass
        else:
            #item = pick_image(event, currentcanvas)
            companionName = canvasutils.getImageLabel(canvas2,item)
            if companionName in combo1['values']:
                combo1.set(companionName) # Actualizar el combo para cargar la especie clicada
            refreshCanvas()

    def right_click(event): # Add icon from catalog to ecosystem
        global currentcanvas
        item = pick_image(event,currentcanvas)
        companionName = canvasutils.getImageLabel(currentcanvas,item)
        if companionName != '':
           global ecosystem
           global ecosystemLinks
           ecosystem, ecosystemLinks = eco.addCompanionToEcosystem(companionName)
        refreshCanvas2()
        refreshCanvas()

    def right_click_canvas2(event): # Remove from ecosystem
        global item
        global ecosystem
        global ecosystemLinks
        item = pick_image(event,canvas2)
        companionName = canvasutils.getImageLabel(canvas2, item)
        if companionName != '':
            #print("vamos a borrar el elemento:",companionName)
            companionName = canvasutils.getImageLabel(canvas2,item)
            ecosystem, ecosystemLinks = eco.removeCompanionFromEcosystem(companionName)
        refreshCanvas2()
        refreshCanvas()

    def scrollCanvas(event):
        global currentcanvas
        currentcanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Canvas events: ####################################################################

    # This bind window to keys so that move is called when you press a key
    canvas.bind("<ButtonPress-1>", select_item) # Select icon in catalog
    canvas.bind("<Button-3>", right_click) # Add icon from catalog to ecosystem
    canvas.bind("<Enter>", on_enter_canvas) # Enter canvas

    canvas2.bind("<ButtonPress-1>", click_canvas2) # Click on icon from ecosystem
    canvas2.bind("<B1-Motion>", move_image) # Drag icon in ecosystem
    canvas2.bind("<ButtonRelease-1>", on_release_button) # Release icon in ecosystem
    canvas2.bind("<Button-3>", right_click_canvas2) # Remove from ecosystem
    canvas2.bind("<Enter>", on_enter_canvas2) # Enter canvas

    left_frame.bind_all("<MouseWheel>", scrollCanvas)
    right_frame.bind_all("<MouseWheel>",scrollCanvas)

    comp.showAll()

    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas2.configure(scrollregion=canvas2.bbox("all"))

    root.mainloop()

framewin()
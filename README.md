# CPlant
<i>(Para versión en español haz clic <a href="LEEME.md">aquí</a>)</i><br>
A visualizer of companion plants relationships made with Python and SQLite

![cplants1](https://user-images.githubusercontent.com/49267590/219956809-1fc463ea-96c7-4a7e-834d-488de6ff08bc.png)

This software shows graphically the relationships between plants, in order to design visually ecosystems that are sustainable and symbiotic. This software is still under development and is aimed to be a part of an #opensource #permaculture software.

The program contains two frames:
<ul>
  <li><b>Left frame:</b> Allows you to choose a plant from the plant catalog and add it to an ecosystem. Left click over any plant "X" will show the plant companions (beneficial or detrimental) and also the plants for which plant "X" is a companion. Right click will add the plant to the ecosystem. This way we can form a set of plants (ecosystem) and see the relationships they contain</li>
  
  <li><b>Right frame:</b> Shows the beneficial or harmful relationships between plants of the ecosystem. A green line indicates a beneficial relationship, while a red line indicates a detrimental relationship for the plant. A description of the relationships (couples of plants) of the formed ecosystem will display.
Right click over a plant in the ecosystem will remove it. Left click will display the plants companions.
</li>
</ul>
The program also allows to show recommended plants for any formed ecosystem or plants that could harm the ecosystem.

![CPlants creación de ecosistema](https://user-images.githubusercontent.com/49267590/217051260-1c25f10c-9b2a-4b14-a579-c42bfcae5dea.png)

The plant catalog and relationships are stored in a SQLite database. The program allows to create, modify or delete plants and ecosystems.
The ecosystem network images can be moved with the mouse, so the network image can be customized by the user.

The main file is cplants.py

If you want to use it as a Windows executable file, you can download it from <a href="https://drive.google.com/drive/folders/1F1bidC26IPDtMy7XihU498Eys028yHLF?usp=sharing">here</a>


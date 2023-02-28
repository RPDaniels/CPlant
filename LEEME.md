# CPlant
<i>(For english version click <a href="README.md">here</a>)</i><br>
Un visualizador de relaciones entre plantas compañeras hecho con Python y SQLite

![cplants1](https://user-images.githubusercontent.com/49267590/219956809-1fc463ea-96c7-4a7e-834d-488de6ff08bc.png)

Este software muestra gráficamente las relaciones entre plantas, con el objetivo de diseñar ecosistemas visualmente sostenibles y simbióticos. Este software aún está en desarrollo y tiene como objetivo formar parte de un software de #permacultura #opensource.

El programa contiene dos marcos:
<ul>
  <li><b>Marco izquierdo:</b> Permite elegir una planta del catálogo de plantas y agregarla a un ecosistema. Al hacer clic izquierdo sobre cualquier planta "X", se mostrarán las plantas compañeras (beneficiosas o perjudiciales) y también las plantas para las que la planta "X" es compañera. Haciendo clic derecho se agregará la planta al ecosistema. De esta manera podemos formar un conjunto de plantas (ecosistema) y ver las relaciones que contienen</li>
  <li><b>Marco derecho:</b> Muestra las relaciones beneficiosas o perjudiciales entre las plantas del ecosistema. Una línea verde indica una relación beneficiosa, mientras que una línea roja indica una relación perjudicial para la planta. Se mostrará una descripción de las relaciones (parejas de plantas) del ecosistema formado. Haciendo clic derecho sobre una planta en el ecosistema la eliminará. Haciendo clic izquierdo se mostrarán las plantas compañeras.
</li>
</ul>
El programa también permite mostrar las plantas recomendadas para cualquier ecosistema formado o las plantas que podrían perjudicar al ecosistema.

![CPlants creación de ecosistema](https://user-images.githubusercontent.com/49267590/217051260-1c25f10c-9b2a-4b14-a579-c42bfcae5dea.png)

El catálogo de plantas y las relaciones se almacenan en una base de datos SQLite. El programa permite crear, modificar o eliminar plantas y ecosistemas.
Las imágenes del ecosistema se pueden mover con el ratón, por lo que la imagen de la red se puede personalizar por el usuario.

El archivo principal es cplants.py

Si desea utilizarlo como archivo ejecutable de Windows, puede descargarlo desde <a href="https://drive.google.com/drive/folders/1F1bidC26IPDtMy7XihU498Eys028yHLF?usp=sharing">aquí</a>


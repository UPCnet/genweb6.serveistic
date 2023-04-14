====================
genweb6.serveistic
====================

Serveis TIC de la UPC és un portal que proporciona una visió integrada i
unificada dels Serveis TIC que s'ofereixen a la universitat.

How it works
============

Quan s'instal·la el paquet a un lloc Genweb, una sèrie de components com ara
tipus de dades, vistes, *portlets*, etc. es fan automàticament disponibles.

Tipus de dades
##############

* **serveitic**: servei oferit per la UPC.
* **problema**: problema associat a un servei.
* **notificaciotic**: notificació referent a un servei o al lloc web en general.

Vistes
######

* **homepage**: cercador *facetat* de serveis.
* **serveistic-controlpanel**: paràmetres de configuració del paquet.
* **serveistic-facetes-controlpanel**: paràmetres de configuració de les facetes.
* **update_indicadors**: actualitza els indicadors relacionats amb el nombre
  de visites.

Portlets
########

* **banners**: mostra banners associats a un servei o al portal en general.
* **indicadors**: mostra propietats registrades com a indicadors d'un servei TIC.
* **notificacios**: mostra les notificacions associades a un servei TIC.
* **problemes**: mostra els problemes associats a un servei TIC.

Per a recollir la informació sobre els indicadors i problemes associats als
serveis, el paquet disposa de dos clients web configurables mitjançant la vista
*serveistic-controlpanel*.

Subscriptors
############

* **IServeiTIC on IObjectRemovedEvent**: Actualitza els indicadors.
* **IServeiTIC on IActionSucceededEvent**: Actualitza els indicadors.

Camps de registre
#################

Afegeix al registre els camps definits en 
``genweb6.serveistic.controlpanels.serveistic.IServeisTICControlPanelSettings`` i 
``genweb6.serveistic.controlpanels.facetes.IServeisTICFacetesControlPanelSettings``.

Installation
============

To install `genweb6.serveistic` you simply add ``genweb6.serveistic``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `genweb6.serveistic` using the Add-ons control panel.

Configuration
=============

To import the faceted search settings browse the "Faceted criteria" tab
in the faceted search view and import the file
``genweb6/serveistic/data/faceted_settings.xml``.

# Dubbio: è possibile passare alla funzione di callback dei parametri
# aggiuntivi?
#
# Risposta: si, quanti ne vuoi. 

#!/usr/bin/python
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked,
                            "nicomede", "fasiello")
        self.add(self.button)

    def on_button_clicked(self, widget, nome, cognome):
        print("Hello World, ", nome, " ", cognome, ".")

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Handler:
    # qui vanno i gestori degli eventi

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        
builder = Gtk.Builder()
builder.add_from_file("modelCreator.ui")
builder.connect_signals(Handler() )

window = builder.get_object("mainWindow")
window.show_all()

Gtk.main()



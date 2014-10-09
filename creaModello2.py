#TODO:  - gestione validazione email da perfezionare

from gi.repository import Gtk, Gdk
import re

class Handler:
    # qui vanno i gestori degli eventi

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onEntryChanged(self, entry):
        ctx = entry.get_style_context()
        if not EMAIL_REGEX.match(entry.get_text() ):
            ctx.add_class('invalid')
        else:
            ctx.remove_class('invalid')

    def addField(self, widget):
        # mostra dialogo per impostare formattazione
        dialog = builder.get_object("newFieldDialog")
        dialog.run()
        dialog.destroy()
        pass
        # aggiungi campo a text field
        pass
        # mostra il widget nascosto con campi oppoortunamente modficati
        fieldTemplate = builder.get_object("fieldTemplate")
        fieldTemplate.set_visible(True)
        
# Builder per GUI e segnali
builder = Gtk.Builder()
builder.add_from_file("modelCreator.ui")
builder.connect_signals(Handler() )


# Gestione CSS per tema widget
cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)

# Espressione Regolare per validazione mail
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Applicazione
window = builder.get_object("mainWindow")
window.show()
Gtk.main()



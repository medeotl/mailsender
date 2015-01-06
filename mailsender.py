# -*- coding: utf-8 -*-

# Espressione regolare per validare date inserite
# ^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$

from gi.repository import Gtk, Gdk, Pango
import TOOLS.dateValidator as dateValidator

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Mail Sender", border_width=12)

        self.set_default_size(555, 450)
        #~ self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.box = Gtk.Box(orientation=1, spacing=6)
        self.add(self.box)

        self.create_send_bbox()
        self.create_textview()
        self.create_entry()
        

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.box.pack_end(scrolledwindow, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(2) # 2=WORD
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("In allegato alla presente domanda di "
            + "Mini ASpI di  . "
            + "Si prega cortesemente di inviarla subito")
        
        scrolledwindow.add(self.textview)

    def create_entry(self):
        
        grid = Gtk.Grid(column_spacing=12)
        self.box.pack_start(grid, False, False, 0)
        
        self.lblNome = Gtk.Label("Assistito", xalign=1)
        self.entryNome = Gtk.Entry()
        self.entryNome.set_placeholder_text("Assistito")
        self.entryNome.set_hexpand(True)
        
        self.lblPrimoLavoro = Gtk.Label("Primo rapporto di lavoro",
                                        xalign=1)
        self.entryPrimoLavoro = Gtk.Entry()
        
        grid.attach(self.lblNome, 0, 0, 1, 1)
        grid.attach(self.entryNome, 1, 0, 1, 1)
        grid.attach(self.lblPrimoLavoro, 0, 1, 1, 1)
        grid.attach(self.entryPrimoLavoro, 1, 1, 1, 1)

        # GESTIONE EVENTI
        self.markNome = self.textbuffer.create_mark(
            "markNome", self.iter_at(50), False)
        self.entryNome.connect("changed", self.on_nome_changed, 50)

        self.entryPrimoLavoro.connect("focus-out-event",
                                      self.on_focus_out)

    def create_send_bbox(self):
        self.bb = Gtk.ButtonBox()
        self.bSend = Gtk.Button("Invia")
        self.bb.add(self.bSend)

        self.box.pack_end(self.bb, False, False, 0)

######----------             GESTORI EVENTI             ----------######
               
    def on_nome_changed(self, nome, posizione):
        # cancello quanto precedentemente scritto
        self.textbuffer.delete(
            self.iter_at(posizione),                        # inizio
            self.textbuffer.get_iter_at_mark(self.markNome) # fine
        )
        
        # scrivo il nuovo valore di Entry
        self.textbuffer.insert(self.iter_at(posizione), nome.get_text() )

    def on_focus_out(self, entry, data):
        ctx = entry.get_style_context()
        valida, testo = dateValidator.data_valida( entry.get_text() )
        if valida:
            # la data è valida
            entry.set_text(testo)
            entry.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY, None)
            ctx.remove_class('invalid')
        else:
            entry.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY, 'dialog-warning')
            entry.set_icon_tooltip_text(
                Gtk.EntryIconPosition.SECONDARY, testo)
            ctx.add_class('invalid')

    def iter_at(self, offset):
        # ritorna il textIter corrispondete all'offset
        #~ print(offset)
        return self.textbuffer.get_iter_at_offset(offset)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = TextViewWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()


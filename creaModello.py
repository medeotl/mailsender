# -*- coding: utf-8 -*-

# da aggiustare: funzionamento BOLD, ITALIC, UNDERLINE

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Crea Modello 1")

        self.set_default_size(555, 450)
        self.set_border_width(18)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.box = Gtk.Box(orientation=1, spacing=6)
        self.add(self.box)

        self.create_from()
        self.create_textview()
        self.create_toolbar()

    def create_from(self):
        """ Crea i campi A:, CC: e CCN: """

        grid = Gtk.Grid(column_spacing=12, row_spacing=6)
        self.box.pack_start(grid, False, False, 0)

        self.entryA = Gtk.Entry()
        self.entryA.set_hexpand(True)
        self.entryCc = Gtk.Entry()
        self.entryCcn = Gtk.Entry()


        grid.attach( Gtk.Label(label="A:"), 0, 0, 1, 1 )
        grid.attach( self.entryA, 1, 0, 1, 1 )
        grid.attach( Gtk.Label(label="Cc:"), 0, 1, 1, 1 )
        grid.attach( self.entryCc, 1, 1, 1, 1 )
        grid.attach( Gtk.Label(label="Ccn:"), 0, 2, 1, 1 )
        grid.attach( self.entryCcn, 1, 2, 1, 1 )

    def create_toolbar(self):
        """ Crea la toolbar """
        
        toolbar = Gtk.Toolbar()
        self.box.pack_end(toolbar, False, True, 0)

        # bold, italic, underline
        self.button_bold = Gtk.ToggleToolButton.new()
        self.button_bold.set_icon_name("format-text-bold-symbolic")
        toolbar.insert(self.button_bold, 0)
        self.button_italic = Gtk.ToggleToolButton.new()
        self.button_italic.set_icon_name("format-text-italic-symbolic")
        toolbar.insert(self.button_italic, 1)
        self.button_underline = Gtk.ToggleToolButton.new()
        self.button_underline.set_icon_name("format-text-underline-symbolic")
        toolbar.insert(self.button_underline, 2)

        self.button_bold.connect("clicked",
            self.on_style_button_clicked, self.tag_bold)
        self.button_italic.connect("clicked",
            self.on_style_button_clicked, self.tag_italic)
        self.button_underline.connect("clicked",
            self.on_style_button_clicked, self.tag_underline)

        self.style_dict = {
            "bold":self.button_bold,
            "italic":self.button_italic,
            "underline":self.button_underline}

        # Get Info
        button_get_tag = Gtk.ToolButton.new(None, "TAG - Get Info")
        # rendo visibile la label del pulsante
        toolbar.insert(button_get_tag, 3)

        button_get_tag.connect("clicked", self.on_button_tag_clicked)

        toolbar.insert(Gtk.SeparatorToolItem(), 4)

        # Justify LEFT, CENTER, RIGHT, FILL
        radio_justifyleft = Gtk.RadioToolButton()
        radio_justifyleft.set_icon_name("format-justify-left-symbolic")
        toolbar.insert(radio_justifyleft, 5)

        radio_justifycenter = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifycenter.set_icon_name("format-justify-center-symbolic")
        toolbar.insert(radio_justifycenter, 6)

        radio_justifyright = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifyright.set_icon_name("format-justify-right-symbolic")
        toolbar.insert(radio_justifyright, 7)

        radio_justifyfill = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifyfill.set_icon_name("format-justify-fill-symbolic")
        toolbar.insert(radio_justifyfill, 8)

        radio_justifyleft.connect("toggled", self.on_justify_toggled,
            Gtk.Justification.LEFT)
        radio_justifycenter.connect("toggled", self.on_justify_toggled,
            Gtk.Justification.CENTER)
        radio_justifyright.connect("toggled", self.on_justify_toggled,
            Gtk.Justification.RIGHT)
        radio_justifyfill.connect("toggled", self.on_justify_toggled,
            Gtk.Justification.FILL)

    def create_textview(self):
        """ Crea l'area di testo """
        
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
        self.textbuffer.connect("notify::cursor-position",
            self.on_cursor_position_changed)

        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold",
            weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic",
            style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline",
            underline=Pango.Underline.SINGLE)

    def on_style_button_clicked(self, button, tag):
        """ gestione dei pulsanti BOLD, ITALIC, UNDERLINE """
        
        print (button.get_active() )
        if self.textbuffer.props.has_selection:
            # ho testo selezionato a cui applicare la formattazione
            bounds = self.textbuffer.get_selection_bounds()
            start, end = bounds
            if button.get_active():
                self.textbuffer.apply_tag(tag, start, end)
            else:
                self.textbuffer.remove_tag(tag, start, end)
        else:
            cursore = self.textbuffer.get_iter_at_offset(
                self.textbuffer.props.cursor_position)
            self.textbuffer.apply_tag(tag, cursore, cursore)

    def on_button_tag_clicked(self, widget):
            
        mark_cursore = self.textbuffer.get_insert()
        iter_cursore = self.textbuffer.get_iter_at_mark(mark_cursore)
        print(iter_cursore.get_tags() )
        print("posizione cursore: ",
            self.textbuffer.props.cursor_position)
        print("dimensione finestra: ",self.get_size() )

    def on_justify_toggled(self, widget, justification):
        """ imposta la giustificazione selezionata """
        
        self.textview.set_justification(justification)

    def on_cursor_position_changed(self, buffer, data=None):
            
        ti = self.textbuffer.get_iter_at_offset(
            self.textbuffer.props.cursor_position-1)
        self.button_bold.set_active(False)
        self.button_italic.set_active(False)
        self.button_underline.set_active(False)
        for tag in ti.get_tags():
            self.style_dict[tag.props.name].set_active(True)

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

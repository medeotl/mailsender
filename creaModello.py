# da aggiustare: funzionamento BOLD, ITALIC, UNDERLINE

from gi.repository import Gtk, Gdk, Pango

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Crea Modello")

        self.set_default_size(555, 450)
        self.set_border_width(6)
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.box = Gtk.Box(orientation=1, spacing=6)
        self.add(self.box)

        self.create_from()
        self.create_textview()
        self.create_toolbar()
        
    def create_from(self):
        """ Crea i campi A:, CC: e CCN: """

        grid = Gtk.Grid(column_spacing=12)
        self.box.pack_start(grid, False, False, 0)
        
        self.entryA = Gtk.Entry()
        self.entryA.set_hexpand(True)
        self.entryCc = Gtk.Entry()
        self.entryCcn = Gtk.Entry()
        
        
        grid.attach( Gtk.Label("A:"), 0, 0, 1, 1 )
        grid.attach( self.entryA, 1, 0, 1, 1 )
        grid.attach( Gtk.Label("Cc:"), 0, 1, 1, 1 )
        grid.attach( self.entryCc, 1, 1, 1, 1 )
        grid.attach( Gtk.Label("Ccn:"), 0, 2, 1, 1 )
        grid.attach( self.entryCcn, 1, 2, 1, 1 )

    def create_toolbar(self):
        """ Crea la toolbar """
        toolbar = Gtk.Toolbar()
        self.box.pack_end(toolbar, False, True, 0)

        # bold, italic, underline
        button_bold = Gtk.ToggleToolButton.new_from_stock(Gtk.STOCK_BOLD)
        toolbar.insert(button_bold, 0)
        button_italic = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ITALIC)
        toolbar.insert(button_italic, 1)
        button_underline = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDERLINE)
        toolbar.insert(button_underline, 2)

        button_bold.connect("clicked", self.on_style_button_clicked,
            self.tag_bold)
        button_italic.connect("clicked", self.on_style_button_clicked,
            self.tag_italic)
        button_underline.connect("clicked", self.on_style_button_clicked,
            self.tag_underline)
        
        # Get Info
        button_get_tag = Gtk.ToolButton.new(None, "TAG - Get Info")
        # rendo visibile la label del pulsante
        button_get_tag.set_is_important(True) 
        toolbar.insert(button_get_tag, 3)

        button_get_tag.connect("clicked", self.on_button_tag_clicked)

        toolbar.insert(Gtk.SeparatorToolItem(), 4)

        # Justify LEFT, CENTER, RIGHT, FILL
        radio_justifyleft = Gtk.RadioToolButton()
        radio_justifyleft.set_stock_id(Gtk.STOCK_JUSTIFY_LEFT)
        toolbar.insert(radio_justifyleft, 5)

        radio_justifycenter = Gtk.RadioToolButton.new_with_stock_from_widget(
            radio_justifyleft, Gtk.STOCK_JUSTIFY_CENTER)
        toolbar.insert(radio_justifycenter, 6)

        radio_justifyright = Gtk.RadioToolButton.new_with_stock_from_widget(
            radio_justifyleft, Gtk.STOCK_JUSTIFY_RIGHT)
        toolbar.insert(radio_justifyright, 7)

        radio_justifyfill = Gtk.RadioToolButton.new_with_stock_from_widget(
            radio_justifyleft, Gtk.STOCK_JUSTIFY_FILL)
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
        
        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold",
            weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic",
            style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline",
            underline=Pango.Underline.SINGLE)

    def on_style_button_clicked(self, widget, tag):
        """ gestione dei pulsanti BOLD, ITALIC, UNDERLINE """
        if self.textbuffer.props.has_selection:
            bounds = self.textbuffer.get_selection_bounds()
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)
            # disattivo il pulsante
            # FIXME: la disattivazione non funziona così
            widget.set_active(False)
        else:
            cursore = self.textbuffer.props.cursor_position
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


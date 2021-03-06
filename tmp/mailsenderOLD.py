# Espressione regolare per validare date inserite
# ^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$

from gi.repository import Gtk, Gdk, Pango

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Mail Sender", border_width=12)

        self.set_default_size(555, 450)
        #~ self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.box = Gtk.Box(orientation=1, spacing=6)
        self.add(self.box)

        self.create_send_toolbar()
        self.create_textview()
        #~ self.create_toolbar() # non serve (ma funziona)
        self.create_entry()
        

    def create_toolbar(self): # per ora inutile
        toolbar = Gtk.Toolbar()
        self.box.pack_end(toolbar, False, True, 0)

        button_bold = Gtk.ToggleToolButton.new_from_stock(Gtk.STOCK_BOLD)
        toolbar.insert(button_bold, 0)

        button_italic = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ITALIC)
        toolbar.insert(button_italic, 1)

        button_underline = Gtk.ToolButton.new_from_stock(Gtk.STOCK_UNDERLINE)
        toolbar.insert(button_underline, 2)
        
        button_get_tag = Gtk.ToolButton.new(None, "Get Info")
        # rendo visibile la label del pulsante
        button_get_tag.set_is_important(True) 
        toolbar.insert(button_get_tag, 3)

        button_bold.connect("clicked", self.on_button_clicked, self.tag_bold)
        button_italic.connect("clicked", self.on_button_clicked,
            self.tag_italic)
        button_underline.connect("clicked", self.on_button_clicked,
            self.tag_underline)
        button_get_tag.connect("clicked", self.on_button_tag_clicked)

        toolbar.insert(Gtk.SeparatorToolItem(), 4)

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

        toolbar.insert(Gtk.SeparatorToolItem(), 9)

        button_clear = Gtk.ToolButton.new_from_stock(Gtk.STOCK_CLEAR)
        button_clear.connect("clicked", self.on_clear_clicked)
        toolbar.insert(button_clear, 10)

        toolbar.insert(Gtk.SeparatorToolItem(), 11)

        button_search = Gtk.ToolButton.new_from_stock(Gtk.STOCK_FIND)
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.insert(button_search, 12)
    
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

        # DA USARE PER TEMPLATE CREATOR
        #
        #~ self.tag_bold = self.textbuffer.create_tag("bold",
            #~ weight=Pango.Weight.BOLD)
        #~ self.tag_italic = self.textbuffer.create_tag("italic",
            #~ style=Pango.Style.ITALIC)
        #~ self.tag_underline = self.textbuffer.create_tag("underline",
            #~ underline=Pango.Underline.DOUBLE)

    def create_entry(self):
        
        grid = Gtk.Grid(column_spacing=12)
        self.box.pack_start(grid, False, False, 0)
        
        self.lblNome = Gtk.Label("Assistito", xalign=1)
        self.entryNome = Gtk.Entry()
        self.entryNome.set_placeholder_text("Assistito")
        self.entryNome.set_hexpand(True)
        
        self.lblPrimoLavoro = Gtk.Label("Primo rapporto di lavoro", xalign=1)
        self.entryPrimoLavoro = Gtk.Entry()
        
        grid.attach(self.lblNome, 0, 0, 1, 1)
        grid.attach(self.entryNome, 1, 0, 1, 1)
        grid.attach(self.lblPrimoLavoro, 0, 1, 1, 1)
        grid.attach(self.entryPrimoLavoro, 1, 1, 1, 1)

        
        self.markNome = self.textbuffer.create_mark(
            "markNome", self.iter_at(50), False)
        self.entryNome.connect("changed", self.on_nome_changed, 50)

    def create_send_toolbar(self):
        self.bb = Gtk.ButtonBox()
        self.bSend = Gtk.Button("Invia")
        self.bb.add(self.bSend)

        self.box.pack_end(self.bb, False, False, 0)
            
    def on_button_clicked(self, widget, tag):
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
               
    def on_nome_changed(self, nome, posizione):
        # cancello quanto precedentemente scritto
        self.textbuffer.delete(
            self.iter_at(posizione),                        # inizio
            self.textbuffer.get_iter_at_mark(self.markNome) # fine
        )
        
        # scrivo il nuovo valore di Entry
        self.textbuffer.insert(self.iter_at(posizione), nome.get_text() )

    def on_clear_clicked(self, widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)

    def on_justify_toggled(self, widget, justification):
        self.textview.set_justification(justification)

    def on_search_clicked(self, widget):
        dialog = SearchDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()

            self.search_and_mark(dialog.entry.get_text(), start)

        dialog.destroy()

    def search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match != None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)
            
    def iter_at(self, offset):
        # ritorna il textIter corrispondete all'offset
        print(offset)
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


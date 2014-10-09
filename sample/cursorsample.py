from gi.repository import Gtk

class CursorSample(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="org.app.CursorSample")

        self.buffer = Gtk.TextBuffer()
        self.buffer.connect("notify::cursor-position",
                            self.on_cursor_position_changed)

        self.tw = Gtk.TextView()
        self.tw.set_buffer(self.buffer)
        self.tw.props.wrap_mode = Gtk.WrapMode.CHAR

    def do_activate(self):
        main_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        main_window.add(self.tw)
        self.add_window(main_window)
        main_window.set_position(Gtk.WindowPosition.CENTER)
        main_window.show_all()

    def on_cursor_position_changed(self, buffer, data=None):
        print(buffer.props.cursor_position)

if __name__ == "__main__":
    cursorsample = CursorSample()
    cursorsample.run(None)

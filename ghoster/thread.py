import threading
from threading import Thread
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject


class MainWindow(Gtk.Window):

    a = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.default_height = 50
        self.props.default_width = 300

        self.connect("destroy", Gtk.main_quit)

        self.progress = Gtk.ProgressBar(show_text=True)

        self.add(self.progress)

        self.show_all()

        print(self.props.window)
        gdk_window = self.props.window
        gdk_window.set_opacity(0.9)

        self.run_thread(target=self.example_target, callback=(self.update_progess, self.cmdline_logging))

    def cmdline_logging(self):
        print("test")

    def update_progess(self, i):
        self.progress.pulse()
        self.progress.set_text(str(i))
        return False

    def example_target(self, callback_list):
        i = 0
        while self.a is True:
            i += 1
            GLib.idle_add(callback_list[0], i)
            GLib.idle_add(callback_list[1])
            time.sleep(15)

    def run_thread(self, target, callback):
        thread = threading.Thread(target=target, args=(callback,))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    app = MainWindow()
    Gtk.main()
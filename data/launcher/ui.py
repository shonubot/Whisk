import gi
import subprocess
import os
from launcher.search import get_applications, fuzzy_search

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, Gdk

class QuickLaunchWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Whisk")
        self.set_default_size(600, 100)

        # Load CSS
        provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
        provider.load_from_path(css_path)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Search apps...")
        self.entry.connect("changed", self.on_search)
        self.entry.connect("activate", self.on_launch_selected)

        self.listbox = Gtk.ListBox()
        self.listbox.connect("row-activated", self.on_row_activated)

        self.scroller = Gtk.ScrolledWindow()
        self.scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroller.set_min_content_height(200)
        self.scroller.set_child(self.listbox)

        self.results = []

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.append(self.entry)
        box.append(self.scroller)

        self.set_child(box)
        self.applications = get_applications()

    def on_search(self, entry):
        query = entry.get_text()

        # GTK4-compatible method to clear ListBox
        child = self.listbox.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.listbox.remove(child)
            child = next_child

        self.results = fuzzy_search(self.applications, query)

        for name, path, icon in self.results:
            row = Gtk.ListBoxRow()
            row.set_child(Gtk.Label(label=name))
            self.listbox.append(row)

    def on_launch_selected(self, entry):
        if self.results:
            name, path, _ = self.results[0]
            subprocess.Popen(["gtk-launch", path])

    def on_row_activated(self, listbox, row):
        index = row.get_index()
        if 0 <= index < len(self.results):
            name, path, _ = self.results[index]
            subprocess.Popen(["gtk-launch", path])

class QuickLaunchApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.shonubot.whisk")

    def do_activate(self):
        win = QuickLaunchWindow(self)
        win.present()

def launch_ui():
    app = QuickLaunchApp()
    app.run()

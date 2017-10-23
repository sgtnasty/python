#!/usr/bin/env python


import uuid
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


ICON_NAME_ONE = "system-run"
OO = "mail-send-receive-symbolic"


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Destiny Manager")
        self.set_border_width(0)
        self.set_default_size(800, 400)

        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "Destiny"
        self.set_titlebar(self.headerbar)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name=ICON_NAME_ONE)
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.headerbar.pack_end(button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(button)

        self.headerbar.pack_start(box)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.destiny_treeview = self.create_treeview()
        self.destiny_treeview.expand_row(Gtk.TreePath('0'), False)
        select = self.destiny_treeview.get_selection()
        select.connect("changed", self.on_tree_selection_changed)
        self.scrolledwindow.add(self.destiny_treeview)
        self.paned.add1(self.scrolledwindow)
        self.paned.add2(self.create_textview())
        self.paned.set_wide_handle(True)
        self.paned.set_position(192)
        self.vbox.pack_start(self.paned, True, True, 0)
        self.status_bar = Gtk.Statusbar()
        self.status_bar.push(1, 'Ready')
        self.vbox.pack_end(self.status_bar, False, True, 0)
        self.add(self.vbox)

    def on_button_clicked(self, widget):
        print("Hello World")

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.append_text('{}: {}'.format(model[treeiter][0], model[treeiter][1]))
            print("You selected", model[treeiter][0])

    def create_treeview(self):
        tv = Gtk.TreeView(self.create_store())
        tv.append_column(Gtk.TreeViewColumn('Entity', Gtk.CellRendererText(), text=0))
        tv.append_column(Gtk.TreeViewColumn('Count', Gtk.CellRendererText(), text=1))
        return tv

    def create_store(self):
        store = Gtk.TreeStore(str, str)
        self.weapons_iter = store.append(None, ['Weapons', '40'])
        self.gen_entries(store, self.weapons_iter, 10, 'weapon ')
        self.armor_iter = store.append(None, ['Armor', '40'])
        self.gen_entries(store, self.armor_iter, 100, 'armor ')
        self.items_iter = store.append(None, ['Items', '100'])
        self.gen_entries(store, self.items_iter, 100, 'item ')
        return store

    def gen_entries(self, store, iter, count, title):
        for i in range(count):
            store.append(iter, ['{}{}'.format(title, i+1), str(uuid.uuid1())])

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        scrolledwindow.add(self.textview)
        return scrolledwindow

    def append_text(self, text):
        v = '{}\n'.format(text)
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, v)
        self.textview.scroll_to_mark(self.textbuffer.get_insert(), 0.0, True, 0.5, 0.5)


def main():
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
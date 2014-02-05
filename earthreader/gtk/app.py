import os
import os.path
import sys
import uuid

from gi.repository.GdkPixbuf import Pixbuf
from gi.repository.Gtk import (Application, ApplicationWindow, Box,
                               CellRendererText, ListStore, TreeStore,
                               TreeView, TreeViewColumn)
from gi.repository.WebKit2 import WebView
from libearth.repository import FileSystemRepository
from libearth.session import Session
from libearth.stage import Stage
from libearth.subscribe import Category

from .subscribe import SubscriptionTreeModel


APP_ID = 'org.earthreader.gtk'
ICON_LIST = [
    Pixbuf.new_from_file(os.path.join(os.path.dirname(__file__), 'icons', n))
    for n in os.listdir(os.path.join(os.path.dirname(__file__), 'icons'))
]


class EarthReaderApp(Application):

    __gtype_name__ = 'EarthReaderApp'
    __slots__ = 'session', 'repository', 'stage'

    def __init__(self):
        super(EarthReaderApp, self).__init__(application_id=APP_ID)
        self.session = Session('er-gtk-{0:x}'.format(uuid.getnode()))
        self.repository = FileSystemRepository(
            '/home/dahlia/Dropbox/Earth Reader')  # FIXME
        self.stage = Stage(self.session, self.repository)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.window = ReaderWindow(
            application=self,
            hide_titlebar_when_maximized=True,
        )
        self.window.set_default_size(600, 400)
        self.window.maximize()
        self.window.show_all()
        self.window.content_view.load_uri('http://earthreader.org/')


class ReaderWindow(ApplicationWindow):

    __gtype_name__ = 'ReaderWindow'

    def __init__(self, **kwargs):
        super(ReaderWindow, self).__init__(
            title='Eearth Reader',
            **kwargs
        )
        app = self.get_application()
        assert isinstance(app, EarthReaderApp)
        self.set_wmclass('Earth Reader', 'Earth Reader')
        self.set_icon_list(ICON_LIST)
        self.box = Box(spacing=0)
        self.add(self.box)
        subscriptions = SubscriptionTreeModel(app.stage)
        self.subscriptions_sidebar = TreeView(subscriptions)
        cell_renderer = CellRendererText()
        subscription_column = TreeViewColumn('Title', cell_renderer, text=0)
        def cell_data_func(tree_view_column, renderer, model, tree_iter, *args):
            if isinstance(model[tree_iter], Category):
                renderer.set_property('cell-background', 'silver')
            else:
                renderer.set_property('cell-background', None)
        subscription_column.set_cell_data_func(cell_renderer, cell_data_func)
        self.subscriptions_sidebar.append_column(subscription_column)
        self.box.pack_start(self.subscriptions_sidebar,
                            expand=True, fill=True, padding=0)
        entries_store = dummy_entries()
        entry_column = TreeViewColumn('Title', CellRendererText(), text=0)
        self.entry_list_view = TreeView(entries_store)
        self.entry_list_view.append_column(entry_column)
        self.box.pack_start(self.entry_list_view,
                            expand=True, fill=True, padding=0)
        self.content_view = WebView()
        self.box.pack_start(self.content_view,
                            expand=True, fill=True, padding=0)


def dummy_feeds():
    store = TreeStore(str, str)
    mine = store.append(None, ('Mine', 'category'))
    store.append(mine, ('Romantic Binaries', 'feed'))
    store.append(mine, ('Referentially transparent', 'feed'))
    friends = store.append(None, ('Friends', 'category'))
    store.append(friends, ('Null Model', 'feed'))
    store.append(friends, ('Mearie Journal', 'feed'))
    return store


def dummy_entries():
    store = ListStore(str)
    store.append(('First entry',))
    store.append(('Second entry',))
    store.append(('Third entry',))
    return store


if __name__ == '__main__':
    app = EarthReaderApp()
    app.run(sys.argv)

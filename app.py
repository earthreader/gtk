import sys

from gi.repository.Gtk import Application, ApplicationWindow


APP_ID = 'io.github.earthreader.gtk'


class EarthReaderApp(Application):

    __gtype_name__ = 'EarthReaderApp'

    def __init__(self):
        super(EarthReaderApp, self).__init__(application_id=APP_ID)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.window = ApplicationWindow.new(self)
        self.window.set_title('Earth Reader')
        self.window.set_default_size(600, 400)
        self.window.maximize()
        self.window.show_all()


if __name__ == '__main__':
    app = EarthReaderApp()
    app.run(sys.argv)
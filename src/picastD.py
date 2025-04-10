#!/usr/bin/env python3

"""
picast - a simple wireless display receiver for Raspberry Pi

    Copyright (C) 2019 Hiroshi Miura
    Copyright (C) 2018 Hsun-Wei Cho

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from logging import DEBUG, StreamHandler, getLogger


def setup_logger():
    logger = getLogger("PiCast")
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = True

def app_main():
    setup_logger()
    WifiP2PServer().start()
    window = Gtk.Window()
    window.set_name('PiCast')
    window.connect('destroy', Gtk.main_quit)

    def picast_target():
        picast = PiCast(window)
        picast.run()
        Gtk.main_quit()

    window.show_all()

    thread = threading.Thread(target=picast_target)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    Gst.init(None)
    app_main()
    Gtk.main()

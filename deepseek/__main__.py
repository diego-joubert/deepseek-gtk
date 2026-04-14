import logging
from gi.repository import Gtk, GLib
from deepseek_gtk import DeepSeekClient
from constants import APP_NAME


def main():
    GLib.set_prgname(APP_NAME)

    try:
        app = DeepSeekClient()
        app.connect("destroy", Gtk.main_quit)
        app.show_all()
        Gtk.main()
    except KeyboardInterrupt:
        logging.info("Aplicacion interrumpida por el usuario.")
    except Exception as error:
        logging.critical(f"La aplicacion callo inesperadamente: {error}", exc_info=True)


if __name__ == "__main__":
    main()

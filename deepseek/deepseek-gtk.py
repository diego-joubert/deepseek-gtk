"""Logica de la aplicacion principal"""

import logging
from utils import get_app_data_path, setup_logging
from constants import (
    WINDOW_TITLE,
    DEFAULT_WIDTH,
    DEFAULT_HEIGHT,
    DEEPSEEK_URL,
    DEFAULT_USER_AGENT,
)

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import Gtk, WebKit2, GLib  # noqa: E402


class DeepSeekClient(Gtk.Window):
    def __init__(self):
        super().__init__(title=WINDOW_TITLE)

        self.set_default_size(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.base_path = get_app_data_path()
        self.icon_path = self.base_path / "deepseek-icon.png"

        # Configurar logging
        setup_logging(self.base_path)

        # Icono de la ventana
        try:
            if self.icon_path.exists():
                self.set_icon_from_file(str(self.icon_path))
            else:
                self.set_icon_name("deepseek")
        except Exception as e:
            logging.warning(f"Error al definir el icono de la ventana: {e}")

        # Inicializar componentes
        self._init_webview()
        self.webview.load_uri(DEEPSEEK_URL)
        self.add(self.webview)
        self.show_all()

    def _init_webview(self):
        data_manager = WebKit2.WebsiteDataManager(
            base_data_directory=str(self.base_path),
            base_cache_directory=str(self.base_path),
        )

        context = WebKit2.WebContext.new_with_website_data_manager(data_manager)
        self.webview = WebKit2.WebView.new_with_context(context)

        # Configurar ajustes

        settings = self.webview.get_settings()
        settings.set_enable_page_cache(True)
        settings.set_enable_html5_local_storage(True)
        settings.set_user_agent(DEFAULT_USER_AGENT)

        logging.info(f"User-Agent definido: {DEFAULT_USER_AGENT}")

        self.webview.connect("load-failed", self._on_load_failed)

        context.connect("download-started", self._on_download_started)

    def _on_download_started(
        self, context: WebKit2.WebContext, download: WebKit2.Download
    ):
        logging.info("Iniciando descarga...")
        download.connect("decide-destination", self._on_download_decide_destination)
        download.connect("finished", self._on_download_finished)
        download.connect("failed", self._on_download_failed)

    def _on_download_decide_destination(
        self, download: WebKit2.Download, suggested_filename: str
    ) -> bool:
        logging.info(f"Solicitado destino para archivo: {suggested_filename}")
        dialog = Gtk.FileChooserDialog(
            title="Guardar archivo", parent=self, action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.ACCEPT,
        )
        if suggested_filename:
            dialog.set_current_name(suggested_filename)
        else:
            dialog.set_current_name("deepseek_download")
        downloads_dir = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)
        if downloads_dir:
            dialog.set_current_folder(downloads_dir)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            uri = dialog.get_uri()
            logging.info(f"Destino definido: {uri}")
            download.set_destination(uri)
            dialog.destroy()
            return True
        dialog.destroy()
        return False

    def _on_download_finished(self, download: WebKit2.Download):
        logging.info("Descarga concluida con exito.")

    def _on_download_failed(self, download: WebKit2.Download, error: GLib.Error):
        logging.warning(f"Descarga fallida: {error}")

    def _on_load_failed(
        self,
        webview: WebKit2.WebView,
        load_event: WebKit2.LoadEvent,
        failing_uri: str,
        error: GLib.Error,
    ) -> bool:
        logging.error(f"Fallo al cargar {failing_uri}: {error.message}")

        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            message_format="Falla de Conexion",
        )

        dialog.format_secondary_text(
            f"No fue posibe cargar DeepSeek.\n\nVerifique su conexion a Internet.\nDetalles: {error.message}\n\nIntentando reconectar en 10 segundos..."
        )
        dialog.run()
        dialog.destroy()
        GLib.timeout_add_seconds(10, self.webview.reload)
        return True


def main():
    DeepSeekClient()
    Gtk.main()


if __name__ == "__main__":
    main()

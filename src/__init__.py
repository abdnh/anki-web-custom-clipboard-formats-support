from __future__ import annotations

import json
import mimetypes
from typing import Any

from anki.hooks import wrap
from aqt import mw
from aqt.editor import EditorWebView, pics
from aqt.qt import *
from .server import CorsServer


def process_mime(
    self: EditorWebView,
    mime: QMimeData,
    *args: Any,
    **kwargs: Any,
) -> tuple[str, bool]:
    _old = kwargs.pop("_old")
    ret = _old(self, mime, *args, **kwargs)
    if ret[0]:
        return ret
    custom_formats: dict[str, str] = {}
    for fmt in mime.formats():
        if fmt.startswith("application/x-qt"):
            prefix = 'value="'
            custom_formats[fmt[fmt.index(prefix) + len(prefix) : -1]] = fmt
    if "Web Custom Format Map" not in custom_formats:
        return "", False
    format_map: dict[str, str] = json.loads(
        mime.data(custom_formats["Web Custom Format Map"]).data()
    )
    html = ""
    for type, custom_format in format_map.items():
        data = mime.data(custom_formats[custom_format]).data()
        filename = "paste"
        ext = mimetypes.guess_extension(type)
        if ext:
            filename += ext
        filename = mw.col.media.write_data(filename, data)
        if ext in pics:
            html += f'<img src="{filename}">'
        else:
            html += f"[sound:{filename}]"

    return html, False


# TODO: use the editor_will_process_mime hook for newer versions
EditorWebView._processMime = wrap(EditorWebView._processMime, process_mime, "around")
config = mw.addonManager.getConfig(__name__)
if config["run_server"]:
    server = CorsServer(config)
    server.start()

#!/usr/bin/env python3
"""Tes cepat mdv: render, ekspor HTML, dan fitur GUI (menu, dirty, simpan, tema).

Jalankan: python3 test_mdv.py    (butuh sesi grafis untuk bagian GUI)
"""
import importlib.machinery
import importlib.util
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_loader(
    "mdvmod", importlib.machinery.SourceFileLoader("mdvmod", str(HERE / "mdv"))
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

tmp = Path(tempfile.mkdtemp())
src = tmp / "in.md"
src.write_text("# Judul\n\n- [x] satu\n- [ ] dua\n\n```py\nx = 1\n```\n")

# --- render / tema ---
assert "github-markdown-dark.css" in m.page(src.read_text(), True)
assert "github-markdown-light.css" in m.page(src.read_text(), False)
body = m.render_body("- [x] a\n- [ ] b\n", True)
assert "checked" in body and "task-list-item" in body

# --- ekspor HTML: satu file, CSS inline ---
out = tmp / "out.html"
m.export_html(src, out, True)
html = out.read_text()
assert "<style>" in html and 'rel="stylesheet"' not in html, "CSS belum inline"
assert 'class="markdown-body"' in html

# --- GUI ---
app = m.App(str(src))
Gtk = app.Gtk

menus = []


def walk(widget):
    if isinstance(widget, Gtk.Menu):
        for it in widget.get_children():
            walk(it)
    elif isinstance(widget, Gtk.MenuItem):
        menus.append(widget.get_label())
        if widget.get_submenu():
            walk(widget.get_submenu())
    elif isinstance(widget, Gtk.Container):
        for child in widget.get_children():
            walk(child)


walk(app.win)
assert "File" in menus and "Tampilan" in menus, menus
assert "Buka…" in menus and "Simpan" in menus and "Ekspor" in menus, menus
assert "Mode gelap" in menus, menus

# edit -> dirty + judul bertanda bintang
app.buffer.set_text("")
assert app.dirty is True, "buffer berubah tapi dirty tidak ter-set"
assert app.win.get_title().startswith("*"), app.win.get_title()

# simpan
app.path = tmp / "simpan.md"
assert app.save() is True
assert (tmp / "simpan.md").read_text() == ""
assert app.dirty is False

app.buffer.set_text("halo dunia")
assert app.save() is True
assert (tmp / "simpan.md").read_text() == "halo dunia"

# toggle tema
before = app.dark
app.theme_item.set_active(not before)
assert app.dark is (not before), "toggle tema tidak mengubah state"

app.dirty = False
assert app.confirm_discard() is True

# mode tampilan: default pratinjau saja
assert app.mode == "preview", app.mode
app.show()
assert app.view.get_visible() is True and app.editor.get_visible() is False
assert app.mode_items["preview"].get_active() is True

for mode, editor_shown, preview_shown in (("preview", False, True), ("editor", True, False), ("both", True, True)):
    app.set_view_mode(mode)
    assert app.editor.get_visible() is editor_shown, mode
    assert app.view.get_visible() is preview_shown, mode

# tema berlaku ke chrome GTK, bukan cuma pratinjau
settings = Gtk.Settings.get_default()
app.set_dark(False, refresh=False)
light_theme = settings.get_property("gtk-theme-name")
assert not light_theme.endswith("-dark"), light_theme
app.set_dark(True, refresh=False)
dark_theme = settings.get_property("gtk-theme-name")
assert dark_theme.endswith("-dark"), dark_theme

app.win.destroy()
print("SEMUA TES LULUS")

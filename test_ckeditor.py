"""Tes integrasi CKEditor: data dua arah + tema. Butuh sesi grafis."""
import importlib.machinery
import importlib.util
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_loader(
    "m", importlib.machinery.SourceFileLoader("m", str(HERE / "mdv"))
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SRC = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "README.md")
app = m.App(SRC)
Gtk = app.Gtk
app.set_view_mode("wysiwyg")
app.show()


def pump(sec):
    end = time.time() + sec
    while time.time() < end:
        while Gtk.events_pending():
            Gtk.main_iteration()
        time.sleep(0.02)


def js(script, wait=2.0):
    box = {}
    app.ckview.run_javascript(
        script, None,
        lambda v, res, data=None: box.update(v=v.run_javascript_finish(res).get_js_value().to_string()),
        None,
    )
    pump(wait)
    return box.get("v")


ok = None
for _ in range(25):
    ok = js("document.querySelector('.ck-editor') ? 'yes' : 'no'", 0.4)
    if ok == "yes":
        break
assert ok == "yes", "CKEditor tidak muncul di DOM"
print("CKEditor tampil:", ok)

# isi file masuk ke CKEditor (setData CKEditor asinkron, jadi tunggu sampai terisi)
in_editor = ""
for _ in range(25):
    in_editor = js("(document.querySelector('.ck-editor__editable') || {}).innerText || ''", 0.4)
    if in_editor.strip():
        break
assert in_editor.strip(), "CKEditor kosong, push markdown gagal"
print("isi terkirim ke CKEditor:", repr(in_editor[:40]))

# editan di CKEditor masuk ke buffer Python
js("window.mdv.simulateEdit('# Hasil Suntingan\\n\\nteks **tebal**\\n')")
pump(1.5)
buf = app.buffer.get_text(*app.buffer.get_bounds())
assert buf.startswith("# Hasil Suntingan"), repr(buf[:50])
print("CKEditor -> buffer:", repr(buf[:40]))

# tema
app.set_dark(False, refresh=False)
pump(0.5)
assert js("document.body.classList.contains('dark') ? 'dark' : 'light'", 0.4) == "light"
app.set_dark(True, refresh=False)
pump(0.5)
assert js("document.body.classList.contains('dark') ? 'dark' : 'light'", 0.4) == "dark"
print("tema CKEditor: OK")

app.win.destroy()
print("TES CKEDITOR LULUS")

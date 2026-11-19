# mdv

Markdown viewer **dan** editor di window GTK biasa — tanpa tab browser — dengan
tampilan seperti GitHub: tabel, task list, blok kode berwarna, mode gelap/terang.

Dibuat untuk Omarchy/Hyprland, tapi jalan di desktop Linux apa pun yang punya GTK3.

## Fitur

- **Empat mode tampilan**: pratinjau saja (`Ctrl+1`, **default**),
  **editor Markdown** (`Ctrl+2`) — teks `.md` asli dengan pewarnaan sintaks —
  editor + pratinjau (`Ctrl+3`), dan editor WYSIWYG (`Ctrl+4`), hanya muncul kalau
  aset CKEditor terpasang.
- **Editor teks** memakai GtkSourceView (bahasa Markdown) dengan toolbar formater:
  tebal (`Ctrl+B`), miring (`Ctrl+I`), coret, judul, daftar, task list, kutipan,
  blok kode, tautan.
- **Editor WYSIWYG CKEditor 5** (opsional) membaca/menulis **Markdown GFM** langsung
  lewat plugin `Markdown`, jadi file `.md` tetap Markdown, bukan HTML.
- **Menu File**: Baru (`Ctrl+N`), Buka… (`Ctrl+O`), Simpan (`Ctrl+S`),
  Simpan Sebagai… (`Ctrl+Shift+S`), Ekspor ▸ HTML/PDF, Keluar (`Ctrl+Q`).
- **Menu Tampilan**: centang "Mode gelap" + pilihan mode tampilan + muat ulang (`Ctrl+R`).
  Tema berlaku untuk **seluruh window** — menu bar, editor, dan dialog ikut berganti.
- **Ekspor**: HTML satu file (CSS di-inline) dan PDF (selalu versi terang agar terbaca).
- **Anti kehilangan data**: peringatan Simpan/Buang/Batal saat menutup window atau
  membuka dokumen lain dengan perubahan belum tersimpan; judul diberi `*` saat kotor.
- `Esc` menutup window; link eksternal dibuka lewat `xdg-open`.

## Arsitektur singkat

Buffer Markdown di Python adalah sumber kebenaran:

- Editor teks (GtkSourceView) mengedit buffer itu langsung.
- CKEditor (di WebView, JS aktif) ⇄ `window.webkit.messageHandlers.mdv` ⇄ buffer Python;
  hanya perubahan dari interaksi manusia yang dikirim balik, jadi `setData()` programatik
  tidak menandai dokumen "kotor".
- Pratinjau (WebView, JS mati) merender ulang buffer ↔ CSS GitHub.
- Seluruh teks dokumen tidak pernah dibaca dari CKEditor saat menyimpan: simpan selalu
  memakai buffer, jadi format Markdown tidak bisa "hilang" karena perilaku editor.

## Build

**Aplikasinya sendiri tidak punya langkah build.** `mdv` adalah satu skrip Python
(+ CSS + aset CKEditor). Yang "dibangun" hanya CKEditor-nya, dan itu pun **tidak wajib**:
`assets/ckeditor/ckeditor5.umd.js` + `ckeditor5.css` yang ada di repo ini adalah
**build UMD siap pakai** dari paket npm resmi, tanpa bundler, tanpa webpack/vite.

Pasang / perbarui aset CKEditor:

```sh
cd assets/ckeditor
npm install ckeditor5@latest            # hanya untuk mengambil dist-nya
cp node_modules/ckeditor5/dist/ckeditor5.umd.js .
cp node_modules/ckeditor5/dist/ckeditor5.css .
rm -rf node_modules package-lock.json package.json
```

Build UMD itu mengekspos global `CKEDITOR`, dan `assets/ckeditor/editor.js` memakai
`CKEDITOR.ClassicEditor` beserta plugin `Markdown` (GFM) — jadi tidak ada tahap kompilasi.

Kalau butuh **set plugin khusus** (plugin premium/ tambahan), buat build sendiri lalu
letakkan hasilnya dengan nama yang sama:

```sh
npm create ckeditor5@latest        # atau: npm i ckeditor5 vite && ikuti dokumentasi
# hasil build harus mengekspor global CKEDITOR (UMD) atau ubah editor.html/editor.js
# agar memuat ESM, lalu salin ke assets/ckeditor/
```

Setelah aset berubah, jalankan `./install.sh` supaya `~/.local/share/mdv/assets/ckeditor/`
ikut terbarui. Saat `mdv` dijalankan langsung dari checkout repo, aplikasi memakai
`assets/` milik repo (lihat `assets_dir()`), jadi tidak perlu install ulang untuk mencoba.

## Pasang

```sh
git clone git@github.com:dulumina/mdv.git
cd mdv
./install.sh
```

`install.sh` memasang:

| Tujuan | Isi |
|---|---|
| `~/.local/bin/mdv` | executable |
| `~/.local/share/mdv/assets/` | CSS GitHub + `ckeditor/` |
| `~/.local/share/applications/mdv.desktop` | entri menu "Open With" (Exec absolut) |

Dependensi (Arch):

```sh
sudo pacman -S --needed python-markdown-it-py python-pygments python-gobject gtk3 webkit2gtk-4.1
```

## Pakai

```sh
mdv                      # window kosong, siap menulis
mdv README.md            # buka file
mdv -                    # baca dari stdin
mdv --dump README.md     # cetak HTML ke stdout, tanpa GUI
mdv --export html out.html README.md
mdv --export pdf out.pdf README.md
```

`--export pdf` butuh WebView sungguhan, jadi window muncul sekilas lalu menutup sendiri.

## Tes

```sh
python3 test_mdv.py        # render, ekspor HTML, menu, dirty flag, simpan, mode, tema
python3 test_ckeditor.py   # integrasi CKEditor: data dua arah + tema (butuh sesi grafis)
```

## Batas yang diketahui

- CKEditor menormalkan Markdown saat bolak-balik (mis. penanda daftar jadi `-`, spasi
  antar-blok). Teks tetap utuh, tapi file bisa "dirapikan" saat disimpan.
- Tanpa `assets/ckeditor/`, panel editor hanya menampilkan pesan; pratinjau tetap jalan.
- Tema gelap/terang mengganti `gtk-theme-name` ke varian `-dark`/tanpa `-dark`
  (mis. `Adwaita-dark` ⇄ `Adwaita`).
- HTML mentah di file **tidak** disanitasi. Aman untuk dokumen sendiri, jangan dipakai
  membuka `.md` dari sumber tak dikenal.
- Tidak ada live-reload dari perubahan file di disk, emoji shortcode, anchor-link ikon
  pada heading, atau render matematika.
- Ekspor hanya HTML dan PDF. DOCX/ODT butuh `pandoc`.

## Lisensi

Kode: milik penulis repo ini, tanpa lisensi eksplisit.

`assets/*.css` dari [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css), MIT.
`assets/ckeditor/` dari [CKEditor 5](https://ckeditor.com/ckeditor-5/) (GPL-2.0-or-later
atau komersial; `licenseKey: 'GPL'` sudah diset di `editor.js`).

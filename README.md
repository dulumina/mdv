# mdv

Markdown viewer **dan** editor di window GTK biasa — tanpa tab browser — dengan
tampilan seperti GitHub: tabel, task list, blok kode berwarna, mode gelap/terang.

Dibuat untuk Omarchy/Hyprland, tapi jalan di desktop Linux apa pun yang punya GTK3.

## Fitur

- **Pratinjau + editor berdampingan** (split view), pratinjau ikut berubah saat mengetik
  (debounce 300 ms).
- **Menu File**: Baru (`Ctrl+N`), Buka… (`Ctrl+O`), Simpan (`Ctrl+S`),
  Simpan Sebagai… (`Ctrl+Shift+S`), Ekspor ▸ HTML/PDF, Keluar (`Ctrl+Q`).
- **Menu Tampilan**: centang "Mode gelap" (langsung ganti CSS tanpa restart),
  Muat ulang pratinjau (`Ctrl+R`).
- **Ekspor**: HTML satu file (CSS di-inline) dan PDF (selalu versi terang agar terbaca).
- **Anti kehilangan data**: peringatan Simpan/Buang/Batal saat menutup window atau
  membuka dokumen lain dengan perubahan belum tersimpan. Judul window diberi `*` saat kotor.
- `Esc` menutup window; link eksternal dibuka lewat `xdg-open`, bukan di dalam window.

## Alur render

1. `markdown-it-py` preset `commonmark` + ekstensi `table` dan `strikethrough`
2. blok kode diwarnai `pygments` (style `github-dark` / `default`, warna inline)
3. `- [x]` diubah jadi checkbox asli
4. dibungkus CSS resmi [`github-markdown-css`](https://github.com/sindresorhus/github-markdown-css);
   varian gelap/terang awal diambil dari `gsettings get org.gnome.desktop.interface color-scheme`

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
| `~/.local/share/mdv/assets/*.css` | CSS GitHub |
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
python3 test_mdv.py      # render, ekspor HTML, menu, dirty flag, simpan, toggle tema
```

## Batas yang diketahui

- HTML mentah di file **tidak** disanitasi. Aman untuk dokumen sendiri, jangan dipakai
  membuka `.md` dari sumber tak dikenal.
- Tidak ada live-reload dari perubahan file di disk (yang live hanya dari editor),
  emoji shortcode (`:rocket:`), anchor-link ikon pada heading, atau render matematika.
- Ekspor hanya HTML dan PDF. DOCX/ODT butuh `pandoc` yang belum jadi dependensi.
- CSS dan entri desktop menunjuk ke `$HOME` tetap (tidak membaca `XDG_DATA_HOME`).
- Gambar relatif di HTML hasil ekspor tetap menunjuk path relatif; file HTML harus
  disimpan di folder yang sama dengan gambarnya.

## Lisensi

Kode: milik penulis repo ini, tanpa lisensi eksplisit.

`assets/*.css` berasal dari [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css),
MIT — teks lisensi ada di `assets/license-github-markdown-css.txt`.

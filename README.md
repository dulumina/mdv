# mdv

Lihat file Markdown di window GTK biasa — tanpa tab browser — dengan tampilan seperti
GitHub: tabel, task list, blok kode berwarna, dark/light mengikuti tema sistem.

Dibuat untuk Omarchy/Hyprland, tapi jalan di desktop Linux apa pun yang punya GTK3.

## Kenapa bukan browser

Markdown dirender di server-lokal (Python), lalu HTML-nya ditampilkan di
`WebKit2.WebView` tanpa address bar, tanpa JavaScript, tanpa riwayat. Window-nya
dikelola window manager seperti aplikasi lain.

## Alur render

1. `markdown-it-py` preset `commonmark` + ekstensi `table` dan `strikethrough`
2. blok kode diwarnai `pygments` (style `github-dark` / `default`, warna inline)
3. `- [x]` diubah jadi checkbox asli
4. dibungkus CSS resmi [`github-markdown-css`](https://github.com/sindresorhus/github-markdown-css)
   (varian gelap/terang dipilih dari `gsettings get org.gnome.desktop.interface color-scheme`)

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
mdv README.md        # buka window
mdv -                # baca dari stdin
mdv --dump README.md # cetak HTML ke stdout, tanpa GUI
```

- `Esc` menutup window.
- Link eksternal dibuka lewat `xdg-open` (window tetap menampilkan dokumen).
- Gambar relatif (`![](gambar.png)`) ikut termuat karena base URI di-set ke folder file.
- File `.md` bisa diklik-kanan → Open With → mdv.

## Batas yang diketahui

- HTML mentah di file **tidak** disanitasi. Aman untuk dokumen sendiri, jangan dipakai
  membuka `.md` dari sumber tak dikenal.
- Tidak ada live-reload, emoji shortcode (`:rocket:`), anchor-link ikon pada heading,
  atau render matematika.
- CSS dan entry desktop menunjuk ke `$HOME` tetap (tidak membaca `XDG_DATA_HOME`).

## Lisensi

Kode: milik penulis repo ini, tanpa lisensi eksplisit.

`assets/*.css` berasal dari [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css),
MIT — teks lisensi ada di `assets/license-github-markdown-css.txt`.

#!/bin/sh
# Pasang mdv untuk user saat ini.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
bin_dir="$HOME/.local/bin"
data_dir="$HOME/.local/share/mdv"
app_dir="$HOME/.local/share/applications"

if [ ! -f "$here/assets/github-markdown-dark.css" ] || [ ! -f "$here/mdv" ]; then
  echo "gagal: jalankan dari checkout repo mdv (aset CSS atau skrip mdv tidak ada)" >&2
  exit 1
fi

mkdir -p "$bin_dir" "$data_dir/assets" "$app_dir"
install -m 755 "$here/mdv" "$bin_dir/mdv"
install -m 644 "$here"/assets/*.css "$data_dir/assets/"
if [ -d "$here/assets/ckeditor" ]; then
  rm -rf "$data_dir/assets/ckeditor"
  cp -r "$here/assets/ckeditor" "$data_dir/assets/ckeditor"
else
  echo "peringatan: assets/ckeditor tidak ada, mode editor hanya menampilkan pesan" >&2
fi
sed "s|@BIN@|$bin_dir/mdv|" "$here/mdv.desktop" > "$app_dir/mdv.desktop"
update-desktop-database "$app_dir" 2>/dev/null || true

echo "terpasang: $bin_dir/mdv"
echo "hapus dengan: sh $here/uninstall.sh"

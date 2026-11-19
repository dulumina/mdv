#!/bin/sh
# Hapus mdv yang dipasang install.sh untuk user saat ini.
# File Markdown milik pengguna tidak disentuh.
set -eu

bin_dir="$HOME/.local/bin"
data_dir="$HOME/.local/share/mdv"
app_dir="$HOME/.local/share/applications"

rm -f "$bin_dir/mdv" "$app_dir/mdv.desktop"
rm -rf "$data_dir"
update-desktop-database "$app_dir" 2>/dev/null || true

echo "terhapus: $bin_dir/mdv"
echo "terhapus: $app_dir/mdv.desktop"
echo "terhapus: $data_dir"

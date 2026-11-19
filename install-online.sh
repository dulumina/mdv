#!/bin/sh
# Pasang mdv tanpa clone repo:
#   curl -fsSL https://raw.githubusercontent.com/dulumina/mdv/main/install-online.sh | sh
# Pakai versi lain: MDV_REF=v1.0.1 curl ... | sh
set -eu

repo="${MDV_REPO:-https://github.com/dulumina/mdv}"
ref="${MDV_REF:-main}"

command -v curl >/dev/null 2>&1 || { echo "gagal: curl tidak ada" >&2; exit 1; }
command -v tar >/dev/null 2>&1 || { echo "gagal: tar tidak ada" >&2; exit 1; }

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM

url="$repo/archive/refs/heads/$ref.tar.gz"
case "$ref" in
  v*) url="$repo/archive/refs/tags/$ref.tar.gz" ;;
esac

echo "mengunduh $url"
curl -fsSL "$url" | tar -xz -C "$tmp" --strip-components=1
sh "$tmp/install.sh"

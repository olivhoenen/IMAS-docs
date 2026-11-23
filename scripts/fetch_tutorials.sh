#!/usr/bin/env bash
# Copy the hands-on notebooks from the IMAS-tutorial repository into
# docs/tutorials/notebooks/ so that Sphinx renders them as part of the site.
# Usage: scripts/fetch_tutorials.sh [git-ref]   (default: main)
set -euo pipefail

ref="${1:-main}"
repo="${IMAS_TUTORIAL_REPO:-https://github.com/iterorganization/IMAS-tutorial.git}"
root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$root/docs/tutorials/notebooks"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

git clone --quiet --depth 1 --branch "$ref" "$repo" "$tmp/IMAS-tutorial"
rm -rf "$dest"
mkdir -p "$dest"
cp "$tmp"/IMAS-tutorial/notebooks/*.ipynb "$dest"/
# keep images referenced by the notebooks
find "$tmp/IMAS-tutorial/notebooks" -maxdepth 1 -type f \( -name '*.svg' -o -name '*.png' \) \
    -exec cp {} "$dest"/ \;
echo "Copied $(ls "$dest"/*.ipynb | wc -l) notebooks from $repo@$ref into $dest"

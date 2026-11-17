#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SC="$HOME/Documents/automations/sellerchamp"

if [[ ! -d "$SC" ]]; then
  echo "Missing SellerChamp automations folder: $SC" >&2
  exit 1
fi

mkdir -p "$ROOT/.cursor/skills" "$ROOT/.agents"

ln -sfn "$SC/head of growth" "$ROOT/.cursor/skills/head-of-growth"
ln -sfn "$SC/executive assistant" "$ROOT/.cursor/skills/executive-assistant"
ln -sfn "$SC/.agents/product-marketing.md" "$ROOT/.agents/product-marketing.md"

echo "Linked head-of-growth, executive-assistant, and .agents/product-marketing.md"
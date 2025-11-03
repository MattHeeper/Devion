#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI_SRC="${PROJECT_ROOT}/cli/devion.js"
DEST="/usr/local/bin/devion"

echo "Devion installer"
echo "Project root: ${PROJECT_ROOT}"

if [ ! -f "${CLI_SRC}" ]; then
  echo "Error: CLI source not found at ${CLI_SRC}"
  exit 1
fi

detect_pm() {
  if command -v apt-get >/dev/null 2>&1; then echo "apt"; return; fi
  if command -v pacman >/dev/null 2>&1; then echo "pacman"; return; fi
  if command -v dnf >/dev/null 2>&1; then echo "dnf"; return; fi
  if command -v brew >/dev/null 2>&1; then echo "brew"; return; fi
  echo "none"
}

PM=$(detect_pm)
echo "Detected package manager: ${PM}"

# create user config
USER_CONFIG="${HOME}/.devion/config.json"
mkdir -p "$(dirname "${USER_CONFIG}")"
if [ ! -f "${USER_CONFIG}" ]; then
  cat > "${USER_CONFIG}" <<EOF
{
  "created_at": "$(date --iso-8601=seconds || date -Iseconds)",
  "version": "1.0.0",
  "settings": {
    "auto_update": true,
    "language": "en",
    "color_output": true
  }
}
EOF
  echo "Created ${USER_CONFIG}"
else
  echo "${USER_CONFIG} already exists"
fi

# install CLI binary (symlink)
if [ -f "${DEST}" ]; then
  echo "${DEST} exists — backing up to ${DEST}.bak"
  sudo mv "${DEST}" "${DEST}.bak"
fi

echo "Linking ${CLI_SRC} -> ${DEST}"
sudo ln -sfn "${CLI_SRC}" "${DEST}"
sudo chmod +x "${CLI_SRC}"

echo "Install complete. Run 'devion help' to start."

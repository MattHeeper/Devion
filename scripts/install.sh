#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Devion Installer Script
# -----------------------------------------------------------------------------
# This script sets up the Devion environment by:
# 1. Checking for required system dependencies (Node.js, Python).
# 2. Installing project dependencies via npm.
# 3. Creating the default user configuration.
# 4. Symlinking the CLI entry point to /usr/local/bin for global access.
# -----------------------------------------------------------------------------

set -e  # Exit immediately if a command exits with a non-zero status

# --- Visual Configuration ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Project Paths ---
# Resolve the project root relative to this script location
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI_SRC="${PROJECT_ROOT}/cli/index.js"
LINK_DEST="/usr/local/bin/devion"
CONFIG_DIR="${HOME}/.devion"
CONFIG_FILE="${CONFIG_DIR}/config.json"

# --- Helper Functions ---

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is required but not installed. Aborting."
        exit 1
    fi
}

# --- Main Execution Flow ---

echo -e "${CYAN}"
echo "  ____            _             "
echo " |  _ \  ___ __ _(_) ___  _ __  "
echo " | | | |/ _ \  / / |/ _ \| '_ \ "
echo " | |_| |  __/\ V /| | (_) | | | |"
echo " |____/ \___| \_/ |_|\___/|_| |_|"
echo "                                 "
echo -e "${NC}"
log_info "Starting Devion Installation..."
log_info "Project Root: ${PROJECT_ROOT}"

# 1. Prerequisite Check
log_info "Checking system prerequisites..."
check_dependency node
check_dependency npm
check_dependency python3
log_success "System prerequisites found."

# 2. Install NPM Dependencies
if [ -f "${PROJECT_ROOT}/package.json" ]; then
    log_info "Installing Node.js dependencies..."
    cd "${PROJECT_ROOT}"
    # Run install silently to keep output clean
    npm install --silent --no-audit --no-fund
    log_success "Dependencies installed."
else
    log_warn "package.json not found. Skipping npm install."
fi

# 3. Setup User Configuration
log_info "Setting up user configuration..."
mkdir -p "${CONFIG_DIR}"

if [ ! -f "${CONFIG_FILE}" ]; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    cat > "${CONFIG_FILE}" <<EOF
{
  "created_at": "${TIMESTAMP}",
  "version": "1.0.0",
  "settings": {
    "auto_update": true,
    "language": "en",
    "color_output": true
  }
}
EOF
    log_success "Created default config at ${CONFIG_FILE}"
else
    log_warn "Configuration already exists at ${CONFIG_FILE}. Skipping."
fi

# 4. Create Symlink (Global Access)
log_info "Creating global symlink..."

if [ ! -f "${CLI_SRC}" ]; then
    log_error "CLI source file not found at ${CLI_SRC}"
    exit 1
fi

# Ensure the entry point is executable
chmod +x "${CLI_SRC}"

# Check if destination exists and backup if necessary
if [ -f "${LINK_DEST}" ]; then
    log_warn "Existing binary found. Backing up to ${LINK_DEST}.bak"
    sudo mv "${LINK_DEST}" "${LINK_DEST}.bak"
fi

# Create the symbolic link
# We use sudo because /usr/local/bin usually requires root permissions
if sudo ln -sfn "${CLI_SRC}" "${LINK_DEST}"; then
    log_success "Symlink created: ${CLI_SRC} -> ${LINK_DEST}"
else
    log_error "Failed to create symlink. Please check your permissions."
    exit 1
fi

# --- Completion ---
echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo -e "Try running: ${CYAN}devion help${NC}"
echo ""

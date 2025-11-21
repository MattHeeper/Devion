
# Devion 🚀

> **The Next-Generation Hybrid Development Environment Manager.**
> *Seamlessly bridging Node.js UI with Python Core logic.*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.11%2B-yellow.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-lightgrey.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 📖 Overview

**Devion** is not just a CLI tool; it's a hybrid architecture experiment designed to standardize development environments. It solves the "it works on my machine" problem by enforcing tool versions and configurations across your team.

### 🏗️ The Hybrid Architecture

Devion leverages the best of two worlds using an advanced IPC (Inter-Process Communication) bridge:

```mermaid
graph LR
    A[User Terminal] -- Commands --> B(Node.js CLI Frontend)
    B -- JSON Args --> C{IPC Bridge}
    C -- Spawns --> D[Python Core Backend]
    D -- System Ops --> E[OS / File System]
    D -- JSON Result --> B
    B -- Beautiful UI --> A
````

1.  **Node.js (Frontend):** Handles the CLI experience, spinners, colors, and user interaction using `Commander` and `Ora`.
2.  **Python (Backend):** Executes heavy system operations, environment analysis, and logic using `subprocess` and standard libraries.

-----

## ✨ Key Features

  * **🩺 Deep Health Check:** Instantly verifies Python, Node, NPM, Git, and Docker installations.
  * **🧠 Smart Analysis:** Scans project directories to generate statistical reports on file types and structure.
  * **🛠️ Auto-Fix:** Detects missing configurations or tools and attempts to repair them automatically.
  * **🚀 One-Command Deploy:** Packages your project into a distribution-ready `dist/` folder.
  * **⚙️ Global Config:** Centralized configuration via `~/.devion/config.json`.
  * **🔌 Modular Design:** Easily extensible architecture.

-----

## 📦 Installation

### Prerequisites

  * **Python:** 3.11 or higher
  * **Node.js:** v18 or higher
  * **OS:** Linux or macOS (Windows support coming soon)

### ⚡ Method 1: The Quick Installer (Recommended)

We provide an automated script that handles dependencies, permissions, and symlinking.

```bash
# 1. Clone the repository
git clone https://github.com/MattHeeper/Devion.git

# 2. Enter the directory
cd Devion

# 3. Run the installer
./scripts/install.sh
```

### 🛠️ Method 2: Manual Installation

If you prefer to install it step-by-step:

```bash
# 1. Clone repo
git clone https://github.com/MattHeeper/Devion.git
cd Devion

# 2. Install Python Core dependencies
pip install .

# 3. Install Node.js CLI dependencies
npm install

# 4. Link the binary globally
npm link
```

-----

## 🚀 Usage

Once installed, `devion` is available globally in your terminal.

### Common Commands

| Command | Alias | Description |
| :--- | :--- | :--- |
| `devion status` | - | **Health Check:** Checks installed tools and versions. |
| `devion scan` | - | **System Info:** Detailed scan of OS and environment. |
| `devion analyze` | - | **Project Stats:** Analyzes files in the current directory. |
| `devion fix` | - | **Repair:** Fixes missing configs and checks paths. |
| `devion init` | - | **Setup:** Re-initializes the `~/.devion` config. |
| `devion deploy` | - | **Build:** Packages the project to `dist/`. |
| `devion config` | - | **Settings:** View or update global settings. |
| `devion help` | `-h` | **Help:** Shows this list. |

### Examples

**Check System Status:**

```bash
$ devion status

🔧 Development Environment Status
  ✅ python: 3.11.4
  ✅ node: 20.5.0
  ✅ git: 2.40.1
  ❌ docker: Not installed

📊 Summary: 3/4 tools installed
```

**Update Configuration:**

```bash
$ devion config --key language --value fa
✅ Setting 'language' updated to 'fa'.
```

-----

## ⚙️ Configuration

Devion stores its global configuration in `~/.devion/config.json`. You can edit this file manually or use the `devion config` command.

**Default Structure:**

```json
{
  "version": "1.0.0",
  "settings": {
    "auto_update": true,
    "language": "en",
    "color_output": true
  }
}
```

-----

## 🤝 Contributing

We welcome contributions from the community\!

1.  **Fork** the repository.
2.  Create a new **Branch** (`git checkout -b feature/SuperCoolFeature`).
3.  **Commit** your changes (`git commit -m 'Add SuperCoolFeature'`).
4.  **Push** to the branch (`git push origin feature/SuperCoolFeature`).
5.  Open a **Pull Request**.

### Development Setup

To run the project in development mode without installing it globally:

```bash
# Run via npm script
npm run devion -- status
```

-----

## 📜 License

This project is licensed under the **Apache 2.0 License** - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

-----

\<p align="center"\>
\<b\>Built with ❤️ by MattHeeper\</b\><br>
\<i\>Standardizing environments, one command at a time.\</i\>
\</p\>

```
```

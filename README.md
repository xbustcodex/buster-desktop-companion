# Buster Desktop Companion v8.0 Developer Edition

Buster Desktop Companion is a modular AI operating environment for Windows, designed to assist with software development, automation, hardware projects, and intelligent workflows.

Version 8.0 introduces a stable modular architecture with multi-agent coordination, project understanding, plugin support, persistent memory, AI provider abstraction, and a professional PySide6 desktop interface.

---

# Features

## AI Core

- AI Brain
- AI Planner
- Local Rules AI
- OpenRouter Provider
- Ollama Provider
- LM Studio Provider
- Automatic AI Provider Switching
- Background AI Tasks
- Thread Pool

## Desktop Interface

- PySide6 Desktop UI
- Modern Dark Theme
- Service Cards
- Live Performance Dashboard
- Face Widget
- Chat Console
- Planner Panel
- System Monitor
- Compact Mode
- Always-on-top Mode

## Agent Team

- Builder Agent
- Tester Agent
- Fixer Agent
- Reviewer Agent
- Verifier Agent
- Background Agent Workers
- Task Queue

## Project Intelligence

- Workspace Manager
- Project Indexer
- Repository Status
- File Scanner
- Project Analysis
- Build Planning
- Dependency Tracking
- Memory-Assisted Development

## Vision System

- Webcam Support
- Lazy Camera Loading
- YOLO Object Detection
- Face Detection
- Face Recognition
- Face Learning
- QR / Barcode Scanner
- Snapshot Capture

## Voice

- Text-to-Speech
- Speech Recognition
- Wake Word
- Listen Once
- Continuous Conversation Mode

## Memory

- SQLite Memory Database
- Recent Memory
- Long-Term Memory
- AI Memory Search

## Plugin System

- Plugin Loader
- Plugin Registry
- Plugin Marketplace (foundation)

## Hardware

- Hardware Detection
- System Information
- Performance Monitoring
- Desktop Automation

## Development Tools

- Diagnostics
- Service Manager
- Event Bus
- Service Container
- Runtime Monitoring
- Logging
- Configuration Manager

---

# Installation

```bat
git clone https://github.com/xbustcodex/buster_desktop_companion.git

cd buster_desktop_companion

python -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

python main.py
```

---

# Windows EXE

Build using PyInstaller:

```bat
scripts\build_exe.bat
```

Output:

```
dist\Buster\Buster.exe
```

Or download the latest pre-built Windows release from the **GitHub Releases** page.



# Example Commands

```bat
workspace
performance
system status
repo status
index project

ai status
use local
use ollama
use openrouter

listen once
start conversation

start vision
vision status
detect objects
detect faces
learn my face
who am i
take photo
scan qr

agents

builder create a calculator
builder create a weather app

diagnostics

plugins

hardware status
```

---

# Optional Ollama

```bat
ollama pull llama3.2
```

Inside Buster:

```
use ollama
ask write me a Python application
```

---

# Optional OpenRouter

```bat
setx OPENROUTER_API_KEY "your_api_key"
```

Restart your terminal, then:

```
use openrouter
```

---

# Project Structure

```
buster/
    brain/
    core/
    services/
    ui/
    plugins/
    learning/
    vision/
    voice/
    hardware/
    memory/

data/

scripts/

main.py
```

---

# Roadmap

- AI Task Scheduler
- Autonomous Agent Teams
- Repository Understanding
- Learning Engine
- Experience Memory
- Plugin Marketplace
- Android Companion
- Local LLM Optimisation
- Self-Updater
- Windows Installer
- GitHub Auto Releases

---

## Version

**Buster Desktop Companion v8.0 Developer Edition**

Built with Python, PySide6, OpenCV, YOLO, SQLite and modern AI providers.

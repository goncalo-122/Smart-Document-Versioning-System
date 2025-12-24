# Smart Document Versioning System

This project is a lightweight, event‑driven document versioning system built in Python.  
It monitors a target folder in real time, captures file events (create, modify, delete, move), and stores clean, consolidated version states.When the user presses Ctrl+C, the system automatically performs a flush, saving the latest version state of all tracked files before shutting down.
  

The system is designed with a minimal and predictable architecture:
- A watchdog observer detects file system events
- A custom event handler structures events and sends them to a thread‑safe queue
- The main loop processes events sequentially
- The VersionManager accumulates final states and saves versions only on flush
- Full separation of concerns between event detection, event queuing, and version processing

## Features
- Real‑time folder monitoring
- Clean event consolidation (no duplicates, no noise)
- Flush‑only version saving for maximum control
- Safe multi‑thread communication using a queue
- Modular, professional project structure

## Technologies
- Python 3
- watchdog
- queue
- pathlib



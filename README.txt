# Smart Document Versioning System
A lightweight, event‑driven document versioning system built in Python. It monitors a target directory in real time, captures file‑system events (create, modify, delete, move), and produces clean, consolidated version states. When the user terminates the program with Ctrl+C, the system performs a final flush, ensuring that the latest state of every tracked file is safely persisted before shutdown.

##  Architecture Overview
The system follows a minimal, predictable, and fully decoupled architecture:
- Watchdog Observer: continuously monitors the target folder for file‑system events.
- Custom Event Handler: normalizes raw Watchdog events and pushes structured messages into a thread‑safe queue.
- Main Event Loop: sequentially consumes events from the queue, ensuring deterministic processing.
- VersionManager: consolidates the final state of each file and writes version snapshots only during flush operations.
This separation of concerns results in a clean, robust, and maintainable design.

##  Key Features
- Real‑time folder monitoring
- Noise‑free event consolidation (no duplicates, no transient Office events)
- Flush‑only version saving for maximum control and consistency
- Thread‑safe communication via a queue
- Modular and production‑ready project structure
- Predictable behavior even under rapid file changes

##  System Flow
Watchdog Observer → Custom Event Handler → Thread‑Safe Queue → Main Loop → VersionManager → Backup / Deleted folders

##  Technologies Used
- Python 3
- watchdog
- queue
- pathlib


##  Running the System
python main.py
The system will immediately begin monitoring the configured folder. Press Ctrl+C at any time to trigger a safe flush and shutdown.

##  Limitations
- Monitors only a single directory (non‑recursive)
- Versions are saved exclusively during flush operations
- Designed for local environments, not distributed or networked setups
- Not intended as a full backup solution, but as a lightweight versioning layer

##  Future Enhancements
- Recursive monitoring
- Configurable versioning strategies (e.g., per‑event, per‑interval)
- Automatic PDF export for Office documents
- Web‑based interface for browsing versions
- Logging improvements and metrics collection
- Make code more efficient

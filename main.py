from queue import Queue, Empty
from src.file_monitor import FileMonitor
from src.version_manager import versionManager   

def main():
    folder_to_watch = r"C:\Users\gonca\Documents\Segue"
    backup_folder = r"C:\Users\gonca\Desktop\Backup\backups\versions"
    deleted_folder = r"C:\Users\gonca\Desktop\Backup\backups\deleted"

    queue_Events = Queue()
    version_manager = versionManager(backup_folder, deleted_folder)

    monitor = FileMonitor(folder_to_watch, queue_Events)
    monitor.start()

    try:
        while True:
            try:
                event = queue_Events.get(timeout=0.5)
                version_manager.add_event(event)
            except Empty:
                pass
            except Exception as e:
                print("[ERRO NO LOOP]", e)

    except KeyboardInterrupt:
        print("\n[Main] A terminar...")
        version_manager.flush()

if __name__ == "__main__":
    main()

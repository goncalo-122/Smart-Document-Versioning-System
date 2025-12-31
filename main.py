from queue import Queue, Empty
from src.file_monitor import FileMonitor
from src.version_manager import versionManager   
from queue import Empty
def main():
    folder_to_watch = r"C:\Users\gonca\Documents\Segue"
    backup_folder = r"C:\Users\gonca\Desktop\Backup\backups\versions"
    deleted_folder = r"C:\Users\gonca\Desktop\Backup\backups\deleted"

    queue = Queue()
    version_manager = versionManager(backup_folder, deleted_folder)

    monitor = FileMonitor(folder_to_watch, queue)
    monitor.start()

        # Main loop: reads events from the queue and processes them
    try:
        while True:
            try:
                event = queue.get(timeout=0.5)# Retrieves an event with a timeout so the loop never blocks indefinitely
                version_manager.add_event(event)
                
            except Empty:#Continues the loop when no event is detected

                continue
            except Exception as e:
                print("[LOOP ERROR]", e)

            

    except KeyboardInterrupt:
        print("\n[Main] Finishing...")
        version_manager.flush()

if __name__ == "__main__":
    main()

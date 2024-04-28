import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Destination directories
destination_pdf = "/Users/user/Downloads/PDF/"
destination_img = "/Users/user/Downloads/IMG/"
destination_audio = "/Users/user/Downloads/AUDIO/"
destination_video = "/Users/user/Downloads/VIDEO/"
source_dir = "/Users/user/Downloads"

class MoveHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            destination_dir = self.where_to_move(file_name)
            self.move_file(source_dir, destination_dir, file_name)

    def move_file(self, source_dir, destination_dir, file):
        source_file_path = os.path.join(source_dir, file)
        destination_file_path = os.path.join(destination_dir, file)
        try:
            print("Moving file: ", file)
            shutil.move(source_file_path, destination_file_path)
            print("File moved successfully")
        except Exception as e:
            print(f"Error moving file {file}: {e}")

    def where_to_move(self, file):
        if file.endswith(".pdf"):
            return destination_pdf
        elif any(file.endswith(ext) for ext in [".jpg", ".png", ".jpeg", ".heic"]):
            return destination_img
        elif any(file.endswith(ext) for ext in [".mp3", ".wav"]):
            return destination_audio
        elif any(file.endswith(ext) for ext in [".mp4", ".avi", ".mov"]):
            return destination_video
        else:
            return source_dir

if __name__ == '__main__':
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)
    observer.start()
    print("Monitoring for new files in ", source_dir)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

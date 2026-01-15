from watchdog.observers import Observer
from watchdog.events    import FileSystemEventHandler
from threading  		import Thread, Event
from pathlib 			import Path
from os.path			import join
from subprocess 		import run
from .database			import list_of_files
from time				import sleep

crc = list_of_files['vcs_all']['vX-2025.06-SP2']

def cksum(file):
	from subprocess import run
	result = run(['cksum', file], capture_output=True, text=True)
	return result.stdout.split()[0]


class MonitorDownloads(FileSystemEventHandler):
	def __init__(self, files, finished):
		self.files = set(files)
		self.finished = finished

		found_error = 0
		for file in list(self.files):
			print(f'Checking file {file}')
			path = Path.home() / 'Downloads' / file
			if path.is_file():
				if crc[file] == cksum(path):
					print(f'file {file} found, cksum ok')
					self.files.remove(file)
				else:
					print(f'file {file} found, cksum nok')
					found_error = 1

		if found_error:
			print('Please remove corrupted files and try again')

		sleep(1)

		if not self.files:
			print("All files downloaded!")
			self.finished.set() 

	def on_moved(self, event):
		filepath = Path(event.dest_path)
		filename = filepath.name
		print(f'{filename} finished, checking integrity')
		if crc[filename] == cksum(filepath):
			print(f'file {filename} found, cksum ok')

		if filename in self.files:
			self.files.remove(filename)
			print(f"Downloaded: {filename} ({len(self.files)} remaining)")
		
		if not self.files:
			print("All files downloaded!")
			self.finished.set() 


def wait_files(files):
	path = Path.home() / 'Downloads'

	# Event to block monitor
	finished = Event()

	# Configure observer
	monitor  = MonitorDownloads(files, finished)
	observer = Observer()
	observer.schedule(monitor, path, recursive=False)
	observer.start()

	print(f"Waiting files to be downloaded in: {path}...")

	try:
		finished.wait()
	except KeyboardInterrupt:
		print("Cancelled")
		
	observer.stop()
	observer.join()


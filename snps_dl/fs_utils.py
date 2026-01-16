from watchdog.observers import Observer
from watchdog.events    import FileSystemEventHandler
from threading  		import Thread, Event
from pathlib 			import Path
from time				import sleep
from os.path			import join
from subprocess 		import run
from .database			import list_of_files


def cksum(file):
	from subprocess import run
	result = run(['cksum', file], capture_output=True, text=True)
	return result.stdout.split()[0]


class MonitorDownloads(FileSystemEventHandler):
	def __init__(self, product, version, finished):
		self.files_crc = list_of_files[product][version]
		self.finished  = finished

		found_error = 0
		for file in list(self.files_crc):
			print(f'Checking file {file}')
			path = Path.home() / 'Downloads' / file
			if path.is_file():
				if self.files_crc[file] == cksum(path):
					print(f'file {file} found, cksum ok')
					del self.files_crc[file]
				else:
					print(f'error: file {file} found, but cksum is not valid')
					found_error = 1

		if found_error:
			print('Please remove corrupted files and try again')
			#TODO: Exit

		sleep(1) # Wait main thread to pool finished event

		if not self.files_crc:
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


def wait_files(product, version):
	path = Path.home() / 'Downloads'

	# Event to block monitor
	finished = Event()

	# Configure observer
	print(f"Waiting files to be downloaded in: {path}")

	monitor  = MonitorDownloads(product, version, finished)
	observer = Observer()
	observer.schedule(monitor, path, recursive=False)
	observer.start()

	try:
		finished.wait()
	except KeyboardInterrupt:
		print("Cancelled")
		
	observer.stop()
	observer.join()


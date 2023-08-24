import subprocess
import threading
import concurrent.futures

class Command():
    def __init__(self, command: str) -> None:
        self.command = command
        self.output = None
        self.error = None
        self.return_code = None

    def run(self) -> str:
        process = subprocess.run(
            self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
        )
        
        self.output = process.stdout
        self.error = process.stderr
        self.return_code = process.returncode

        self.callback(self)

        if process.returncode == 0:
            return process.stdout
        else:
            return process.stderr

    def threaded_run(self):
        threading.Thread(target=self.run).start()

    def callback(self, *args, **kwargs):
        pass

def concurrent_execute(functions: list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(func) for func in functions]
        concurrent.futures.wait(futures)
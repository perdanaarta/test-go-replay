# import queue
# import subprocess
# import threading
# from core.command import Command, concurrent_execute

# prod = Command("python prod.py")
# dev = Command("python dev.py")

# def capture_output(app_name, command, output_queue):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     while True:
#         line = process.stdout.readline()
#         if not line:
#             break
#         output_queue.put((app_name, line))
#     process.communicate()

# def main():
#     output = queue.Queue()

#     dev = threading.Thread(target=capture_output, args=("App 1", "python dev.py", output))
#     prod = threading.Thread(target=capture_output, args=("App 1", "python prod.py", output))

#     dev.start()
#     prod.start()
#     dev.join()
#     prod.join()

#     while not output.empty():
#         app_name, line = output.get()
#         print(line)
    
# if __name__ == "__main__":
#     main()

import threading
import subprocess
import os
import signal
import sys

# Function to read and print output from a process
def read_process_output(process: subprocess.Popen[str], name):
    for line in process.stdout:
        print(f"{name}: {line.strip()}")

# Function to run an app in a subprocess
def run_app(command, name):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    read_process_output(process, name)
    process.wait()
    return process.returncode

# Function to gracefully terminate an app
def terminate_app(process):
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

def main():
    app1_command = ["python3", "prod.py"]  # Replace with the actual command for app1
    app2_command = ["python3", "dev.py"]  # Replace with the actual command for app2

    app1_process = subprocess.Popen(app1_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)
    app2_process = subprocess.Popen(app2_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, preexec_fn=os.setsid)

    app1_thread = threading.Thread(target=read_process_output, args=(app1_process, "prod"))
    app2_thread = threading.Thread(target=read_process_output, args=(app2_process, "dev"))

    app1_thread.start()
    app2_thread.start()

    try:
        while app1_thread.is_alive() and app2_thread.is_alive():
            pass
    except KeyboardInterrupt:
        print("Termination signal received. Stopping both apps...")
        terminate_app(app1_process)
        terminate_app(app2_process)
        app1_thread.join()
        app2_thread.join()

if __name__ == "__main__":
    main()
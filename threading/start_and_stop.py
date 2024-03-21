# Vyasan Valavil
# 03-21-2024
# START AND STOP MULTIPLE INSTANCES OF A THREAD
# A thread can be started only once.

import threading
import time

class StoppableTask(threading.Thread):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg
        self._stop_event = threading.Event()

    def run(self):
        # a message announcing that the thread has started.
        print(f"Task started with argument: {self.arg}")
        arg = self.arg
        while not self._stop_event.is_set():
            # the actual task goes in here.
            print(arg, "is running...")
            time.sleep(1)  # Task work simulation

    def stop(self):
        self._stop_event.set()


# Start the task for the first time
print("\nFirst thread is starting...")
task1 = StoppableTask('First')
task1.start()

time.sleep(5)

# Stop the task forcefully
print("First thread is ending")
task1.stop()
task1.join()

print("\nSecond thread is starting...")
# Start the task again with a new instance
task2 = StoppableTask('Second')
task2.start()

# Let it run for a while and then stop
time.sleep(5)

print("Third thread is also starting...")
# Start the task for a third time so the second and third instance are both running.
task3 = StoppableTask('Third')
task3.start()
time.sleep(3)

# Now only end the third thread.
print("Third thread is ending\n")
task3.stop()
task3.join()

#Let the second thread run for 5 seconds.
time.sleep(5)

task2.stop()
task2.join()

print("end reached...")
#this is a threading example
import threading
import time
def worker_task(worker_id, sleep_time):
    print(f"worker {worker_id} starting...")
    time.sleep(sleep_time)
    print(f"Worker {worker_id} finished...")

threads = []

for i in range(5):
    t = threading.Thread(target=worker_task, args=(i, 2))
    #target is the function that each thread will execute
    threads.append(t) #we append each thread to a list threads
    t.start()#we start it

for t in threads:
    t.join() #we wait for all threads to finish

print("All threads have completed execution")
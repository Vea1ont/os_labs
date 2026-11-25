from multiprocessing import Process
import time

def worker(number):
    print(f"Процесс {number} начал работу")
    time.sleep(3)
    print(f"Процесс {number} закончил работу")
    
if __name__ == "__main__":
    p1 = Process(target=worker, args=(1,))
    p2 = Process(target=worker, args=(2,))
    
    
    p1.start()
    p2.start()


    p1.join()
    p2.join()
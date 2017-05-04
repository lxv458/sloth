import threading
import time


def threadB():
    print "start thread B"
    task = []
    task.append(threading.Thread(target=funcC, args=(1,)))
    task.append(threading.Thread(target=funcC, args=(2,)))
    task.append(threading.Thread(target=funcC, args=(3,)))
    task.append(threading.Thread(target=funcC, args=(4,)))
    task.append(threading.Thread(target=funcC, args=(5,)))
    task.append(threading.Thread(target=funcC, args=(6,)))
    task.append(threading.Thread(target=funcC, args=(7,)))
    task.append(threading.Thread(target=funcC, args=(8,)))
    task.append(threading.Thread(target=funcC, args=(9,)))
    task.append(threading.Thread(target=funcC, args=(10,)))
    task.append(threading.Thread(target=funcC, args=(11,)))
    task.append(threading.Thread(target=funcC, args=(12,)))
    for t in task:
        t.setDaemon(True)
    for t in task:
        t.start()
    time.sleep(5)
    print "thread B end"


def threadD():
    print "start thread D"
    t = threading.Thread(target=funcC, args=(1,))
    t.setDaemon(True)
    t.start()
    time.sleep(4)
    print "thread D end"


def funcC(num):
    print "the %d funcC start" % num
    print "hi %d" % num
    time.sleep(6)
    print "the %d funcC end" % num


if __name__ == "__main__":
    thread = threading.Thread(target=threadB, args=())
    thread.setDaemon(True)
    thread.start()
    thread.join(3)
    print "this is main thread"

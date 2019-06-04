from threading import Thread
from time import sleep
import time
import pdb


def function(thing1, thing2):
    global thread_wasteland
    print("sleeping for {}".format(thing1))
    sleep(thing1)
    thread_wasteland = thread_wasteland + [thing2]


def test():
    thread = {}
    end = 32
    init = time.time()
    thing2 = "thing2"
    cumulative = []
    global thread_wasteland
    thread_count = 16
    counter = 1

    for foo in range (0, end):
        if thing2:
            print("foo is {}".format(foo))
            modulo_idx = counter % thread_count
            if modulo_idx == 0: 
                counter += 1
                thread[0] = Thread(target = function, args = (foo,foo,))
                thread[0].start()
                thread[0].join(timeout=15)
                for i in range (1, (thread_count - 1)):
                    thread[i].join(timeout=15)
                thread = {}
            else:
                thread[modulo_idx] = Thread(target = function, args = (foo,foo,))
                thread[modulo_idx].start()
                counter += 1
                continue

            print("Incrementing cumulative")
            cumulative = cumulative + thread_wasteland
            thread_wasteland = []

    for i in range(1, thread_count-1):
        try:
            if thread[i]:
                thread[i].join(timeout=15)
        except:
            print("Failed to join thread {}".format(i))

    cumulative = cumulative + thread_wasteland


    endtime = time.time() - init

    print("All done in {} seconds".format(endtime))
    print(cumulative)




if __name__ == '__main__':
    thread_wasteland = []
    test()


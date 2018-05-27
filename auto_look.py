import requests
import time
import threading
import inspect
import ctypes

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def keep_learn(line):

    arr = line.split("|")
    url = arr[0]
    headers = eval("{" + arr[1] + "}")

    # num = int(arr[2][-4:-3])
    # arr[2] = arr[2].replace('"batchId":"' + str(num) + '",', '"batchId":"' + str(num + 1) + '"')
    payload = eval("{" + arr[2] + "}")

    # response = requests.request("POST", url, data=payload, headers=headers)
    # print(response.text)
    while (True):
        response = requests.request("POST", url, data=payload, headers=headers)
        print('================= %s is running ===============' % threading.current_thread().name)
        print(response.text)
        time.sleep(20)


def action_go():
    threads = []
    with open('saveButton.log', 'r') as f:
        line = f.readline()
        i = 1
        while line:
            t = threading.Thread(target=keep_learn, args=(line,),name='Thread '+ str(i))
            t.start()
            threads.append(t)
            time.sleep(1)
            i += 1
            line = f.readline()
    return threads

def kill_all(threads):
    for t in threads:
        if t.is_alive():
            _async_raise(t.ident, SystemExit)

# 5秒一轮回
threads = action_go()
while(True):
    time.sleep(5)
    kill_all(threads)
    threads = action_go()




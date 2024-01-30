import multiprocessing
import time

def e_process():
    s_process = multiprocessing.Process(target=second_process)
    s_process.start()
    #s_process.join()

    print('wow!')

    t_process = multiprocessing.Process(target=third_process)
    t_process.start()
    t_process.join()  # Ждем, пока второй процесс не завершится


def second_process():
    print("second process started")
    for i in range(10):
        print('second process working: ', i)
        time.sleep(1)
    print('second process ended')

def third_process():
    print("third process started")
    for i in range(10):
        print('third process working: ', i)
        time.sleep(1)
    print('third process ended')

if __name__ == "__main__":
    
    eternal_process = multiprocessing.Process(target=e_process)
    eternal_process.start()

    eternal_process.join()  # Ждем, пока вечный процесс не завершится
    print("all ended")

from crawler import *

if __name__ == '__main__':
    while True:
        now = int(time.time())
        part = (now - 1554051600) % (3600*24)
        if part > 0 and part < 40:
            print(datetime.datetime.now(),"......")
            main_crawl()
            time.sleep(30)
        time.sleep(2)
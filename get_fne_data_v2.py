# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import datetime
import pandas as pd
import pymysql as mysql
import urllib
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def data_catcher():
    t0 = time.time()
    my_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    try:
        page1 = pd.read_html('http://161.53.40.111:6080/p1.html')
        page2 = pd.read_html('http://161.53.40.111:6080/p2.html')
        page3 = pd.read_html('http://161.53.40.111:6080/p3.html')
        DCpower = page1[1][1][2].split()
        ACpower = page1[2][1][3].split()
        f_mreze = page1[2][1][4].split()
        MaxP = page1[2][1][9].split()
        eff = page2[0][1][0].split()
        t_conv = page2[0][1][1].split()
        E_today = page3[1][1][0].split()
        E_week = page3[1][1][1].split()
        E_month = page3[1][1][2].split()
        E_year = page3[1][1][3].split()
        E_total = page3[1][1][4].split()
        if int(ACpower[0]) == 0:
            print('Nema sunca! Pokušat ću kasnije.')
        else:
            db = mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
            c = db.cursor()
            insert_data = """INSERT INTO elektrana VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            c.execute(insert_data, (my_time, int(DCpower[0]), int(ACpower[0]), float(eff[0]), int(MaxP[0]), float(f_mreze[0]),
                                    int(t_conv[0]), float(E_today[0]), int(E_week[0]), int(E_month[0]), int(E_year[0]),
                                    int(E_total[0])))
            db.commit()
            db.close()
    except urllib.error.URLError:
        print('Greška u povezivanju.')
    except TimeoutError:
        print('Veza sa serverom je istekla.')
    except ValueError:
        print('Greška u manipulaciji s podacima.')
    finally:
        t1 = time.time()
        t = t1 - t0
        print(my_time)
        print('Vrijeme jedne operacije:{}'.format(t))

if __name__ == '__main__':
    data_catcher()
    sched.add_job(data_catcher, 'interval', minutes=5, max_instances=4)
    sched.start()

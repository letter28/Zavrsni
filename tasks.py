import datetime as dtime
import pymysql as mysql
import time
import numpy as np
import os
import pandas as pd
import urllib
import redis

from celery import Celery

celery_app = Celery("Celery App", broker=os.environ["REDIS_URL"])

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        45,  # seconds
        update_data.s(),
        name="Update data",
    )

@celery_app.task
def update_data():
    print("----> update_data")
    my_time = dtime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        page1 = pd.read_html('http://161.53.40.111:6080/p1.html')
        page2 = pd.read_html('http://161.53.40.111:6080/p2.html')
        page3 = pd.read_html('http://161.53.40.111:6080/p3.html')
        page4 = pd.read_html('http://meteo.hr/podaci.php?section=podaci_vrijeme&prikaz=abc')
        dfw = pd.DataFrame(page4[0])
        rijeka = dfw.loc[dfw['Postaja'] == 'Rijeka']
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
        t_zraka = rijeka.iloc[0, 2]
        vjetar = rijeka.iloc[0, 1]
        stanje_vr = rijeka.iloc[0, 3]
        if int(ACpower[0]) == 0:
            print('Panel ne proizvodi energiju! Pokusat cu kasnije.')
        else:
            conn = mysql.connect(host='pfw0ltdr46khxib3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
                                 user='kfd7pprqwrvy9uep',
                                 password='zvg9opaacxqy4mmu',
                                 db='oha3los99548olek')
            c = conn.cursor()
            insert_data = """INSERT INTO elektrana VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            c.execute(insert_data, (my_time, int(DCpower[0]), int(ACpower[0]), float(eff[0]), int(MaxP[0]), float(f_mreze[0]),
                                    int(t_conv[0]), float(E_today[0]), int(E_week[0]), int(E_month[0]), int(E_year[0]),
                                    int(E_total[0]), float(t_zraka), str(vjetar), str(stanje_vr)))
            conn.commit()
            conn.close()
    except urllib.error.URLError:
        print('Greska u povezivanju.')
    except TimeoutError:
        print('Veza sa serverom je istekla.')
    except ValueError:
        print('Greska u manipulaciji s podacima.')
    except Exception as e:
        print(str(e))
    finally:
        print(my_time)   
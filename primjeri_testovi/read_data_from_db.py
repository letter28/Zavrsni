import pandas as pd
import pymysql as mysql
import datetime as dtime
import matplotlib.pyplot as plt

my_time = dtime.datetime.now().strftime('%H:%M')
my_date = dtime.datetime.now().date()

#Konekcija s bazom podataka.
conn =  mysql.connect(host='localhost', user='root', password='lozinka', db='riteh1')
query = "SELECT * FROM elektrana"
df = pd.read_sql(query, conn)
#df.set_index('Vrijeme', inplace=True)
print(df.columns)
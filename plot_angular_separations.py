#!/usr/bin/env python

import numpy as np
import math
import ephem
import ephem.stars
import matplotlib.pylab as plt 
import pandas as pd

df = pd.read_csv('ninjasat_target_list.csv',
	skiprows=[0,1,2],sep=',')

star_lst = []
for index, row in df.iterrows():
	line  = '%s,' % row['Name']
	line += '%s,' % row['Type']
	line += '%s,' % row['RA (J2000)']
	line += '%s,' % row['DEC (J2000)']
	line += '%s,' % row['Magnitude']		
	line += '%s' % row['optional']		
	print(line)
	star_list.append(ephem.readdb(line))



sun = ephem.Sun()

# 名前,f(fixed)|S(Star)|スペクトルタイプ,RA|固有運動,Dec|固有運動,等級,分点,オプション
# Sirius,f|S|A0,6:45:09.3|-546.01,-16:42:47|-1223.08,-1.44,2000,0
scox1 = ephem.readdb("ScoX-1,f|S|Xray,16:19:55.07,-15:38:25.0,0.00,2000")
scox1 = ephem.readdb("Crab,f|S|Xray,5:34:32,22:00:52,0.00,2000")

f = open('separation.txt','w')
date_array = np.arange('2023-06','2024-06',dtype='datetime64[D]')
separation_degree_list = []
for date in date_array:
	print(date)
	sun.compute(str(date))
	scox1.compute(str(date))
	separation_degree = np.degrees(float(ephem.separation(sun,scox1)))
	print(date,separation_degree)
	f.write('%s,%.3f\n' % (date,separation_degree))
	separation_degree_list.append(separation_degree)
f.close()
separation_degree_array = np.array(separation_degree_list)

fig = plt.figure(figsize=(11.69,8.27),tight_layout=True)
plt.rcParams["mathtext.fontset"] = "dejavuserif"	
plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "serif"
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8

plt.plot(date_array,separation_degree_array,'r-',linewidth=2,
	label='Sun-scox1')
plt.tight_layout(pad=2)
plt.xlabel(r"Year-Month", labelpad=18)
plt.ylabel(r"Angular separation (degree)", labelpad=18)
plt.ylim(0,180)
plt.legend(loc='upper right')

plt.tick_params(axis="both", which='major', direction='in', length=8)
#plt.tick_params(axis="both", which='minor', direction='in', length=5)
plt.grid(True,which='major',linestyle='-')
#plt.minorticks_on()

plt.axhline(35.0)

plt.savefig('angular_separation_sun_scox1.pdf')

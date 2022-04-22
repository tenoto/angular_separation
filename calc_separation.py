#!/usr/bin/env python

import numpy as np
import math
import ephem
import ephem.stars
import matplotlib.pylab as plt 

sun = ephem.Sun()
antares = ephem.star('Antares')
# brightest star in optical near Sco X-1

f = open('separation.txt','w')
date_array = np.arange('2023-06','2024-04',dtype='datetime64[D]')
separation_degree_list = []
for date in date_array:
	print(date)
	sun.compute(str(date))
	antares.compute(str(date))
	separation_degree = np.degrees(float(ephem.separation(sun,antares)))
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
	label='Sun-Antares')
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

plt.savefig('angular_separation_sun_antares.pdf')

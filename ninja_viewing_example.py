#!/usr/bin/env python

import numpy as np 
import pandas as pd
import ephem
import matplotlib.pylab as plt 

YYYY_MM_START = '2023-06'
YYYY_MM_STOP = '2024-06'
date_array = np.arange(YYYY_MM_START,YYYY_MM_STOP,
	dtype='datetime64[D]')
Startracker_Violation_Angle = 35.0

class Target():
	def __init__(self,name,ra,dec):
		self.name = name
		self.ra = ra
		self.dec = dec

		line = "%s,f,%s,%s,0,J2000" % (self.name,self.ra,self.dec)
		self.ephem = ephem.readdb(line)

		self.separation_deg_lst = []
		for date in date_array:
			sun.compute(str(date))			
			self.ephem.compute(str(date))
			self.separation_deg_lst.append(np.degrees(
				float(ephem.separation(sun,self.ephem))))
		self.separation_deg = np.array(self.separation_deg_lst)

sun = ephem.Sun()

df = pd.read_csv('data/ninjasat_target_list - bright_sources.csv',
	skiprows=[0,1],sep=',')

target_lst = []
for index, row in df.iterrows():
	print(row['Name'],row['RA (J2000)'],row['DEC (J2000)'])
	target_lst.append(Target(row['Name'],row['RA (J2000)'],row['DEC (J2000)']))

fig = plt.figure(figsize=(11.69,8.27),tight_layout=True)
plt.rcParams["mathtext.fontset"] = "dejavuserif"	
plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "serif"
plt.rcParams['xtick.major.pad'] = 8
plt.rcParams['ytick.major.pad'] = 8

for target in target_lst:
	plt.plot(date_array,target.separation_deg,
		linewidth=2,label=target.name)
plt.axhline(Startracker_Violation_Angle,ls='--',
	label='Startracker')
plt.tight_layout(pad=2)
plt.xlabel(r"Year-Month", labelpad=18)
plt.ylabel(r"Angular separation from the Sun (degree)", labelpad=18)
plt.ylim(0,180)
plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

plt.tick_params(axis="both", which='major', direction='in', length=8)
#plt.tick_params(axis="both", which='minor', direction='in', length=5)
plt.grid(True,which='major',linestyle='-')
#plt.minorticks_on()

plt.savefig('ninja_viewing_example.pdf')

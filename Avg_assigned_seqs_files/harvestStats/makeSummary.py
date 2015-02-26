#!/usr/bin/python

import os
import re
import sys
import operator
import numpy
import time
import datetime


"""
Script to harvest stats from individual outputs in `singleFiles` directory. 
This creates a single text file with relevant information. 

"""


def makeSummary():

	newFile = open('summaryStats.txt', 'w')
	
    # put timestamp at the top along with other header info
	Time = time.time()
  	st = datetime.datetime.fromtimestamp(Time).strftime('%Y-%m-%d %H:%M:%S')
  	print >> newFile, st
 	print >> newFile, '\n------------\n'
	print >> newFile, 'studyName\tmeanAssigned\tsdAssigned\n'
    
    # ls directory
	fileList = os.listdir('singleFiles')

	# and pull stats from each one
	for file in fileList:
		
		dirFile = 'singleFiles/' + file
		f = open(dirFile)
		for line in f:
			meanMatch = re.search(r'^Mean\s\=\s\s(0\.\d+)', line)
			if meanMatch: 
				statSet = [file, meanMatch.group(1)]
			sdMatch = re.search(r'^SD\s\=\s\s(0\.\d+)', line)
			if sdMatch: 
				statSet.append(sdMatch.group(1))
			
				# name, mean, and sd were put into list  - this tab-delimits them. 
				print >> newFile, '\t'.join(map(str, statSet))


def catAll(): 
	newFile = open('summaryStatsAll.txt', 'w')
	
    # put timestamp at the top along with other header info
	Time = time.time()
  	st = datetime.datetime.fromtimestamp(Time).strftime('%Y-%m-%d %H:%M:%S')
  	print >> newFile, st
 	# print >> newFile, '\n------------\n'
	print >> newFile, 'studyName\tsampleName\tsplitTotal\totuTableTotal\tpercentAssigned'
    
    # ls directory
	fileList = os.listdir('singleFiles')

	# and pull stats from each one
	for file in fileList:
		
		dirFile = 'singleFiles/' + file
		f = open(dirFile)
		for line in f:
			rowMatch = re.search(r'^([\w\.]+)\t(\d+)\.0\t(\d+)\.0\t(0\.\d+)\n', line)
			if rowMatch: 
				rowSet = [file, rowMatch.group(1), rowMatch.group(2), rowMatch.group(3), rowMatch.group(4)]
			
				# name, mean, and sd were put into list  - this tab-delimits them. 
				print >> newFile, '\t'.join(map(str, rowSet))




def main():
  makeSummary()
  catAll()

if __name__ == '__main__':
  main()













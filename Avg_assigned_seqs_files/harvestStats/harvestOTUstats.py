#!/usr/bin/python

import os
import re
import sys
import operator
import numpy
import time
import datetime

"""
James Meadow
May 6 2014

Script to harvest stats from QIIME output files. 

We have a folder holding `...otu_table_stats.txt` files, 
and another holding `...split_libraries_log.txt` files. 
We want to recover this info:  
* average # seqs in each split_libraries_log sample
* average # of those that made it into OTU table. 

This requires getting the columns of samplenames/numbers
from each file and then deviding one by the other and 
averaging across them to get a single number. 

"""




def read_SLL(filename):
  
  # new tuples to hold things
  sampleTuple = ()
  countTuple = ()

  # open file listed in args
  f = open(filename)

  # whether 2 or 3 column split_library_log file (0 or 1)
  withBarcode = 0

  # check for 3rd column, and set withBarcode accordingly
  for line in f:
    checkBC = re.search(r'Barcode\n', line)
    if checkBC: 
      withBarcode = 1
      break
      f.close()

  # if no barcode, search for 2 column format
  # note - open file again to get out of line count
  # then put data into two different tuples
  f = open(filename)
  if withBarcode == 0:
    for line in f:
      match = re.search(r'^([\w\.]+)\t(\d+)\n', line)
      if match: 
        sampleTuple += (match.group(1), )
        countTuple += (match.group(2), )

  # same but for 3 column format
  if withBarcode == 1:
    for line in f:
      match = re.search(r'^([\w\.]+)\t(\d+)\t\w+\n', line)
      if match: 
        sampleTuple += (match.group(1), )
        countTuple += (match.group(2), )

  # this puts them into a new tuple together
  return sampleTuple, countTuple


# same but for otu_table_stats files
def read_OTS(filename):
  sampleTuple = ()
  countTuple = ()

  f = open(filename)
  for line in f:
    match = re.search(r'^\s([\w\.]+):\s(\d+)\.0\n', line)
    # these files have summary stats at the top, so filter them out
    if match: 
      if 'Max' in match.group(1):
        continue
      if 'Min' in match.group(1):
        continue
      if 'Mean' in match.group(1):
        continue
      if 'Median' in match.group(1):
        continue
      sampleTuple += (match.group(1), )
      countTuple += (match.group(2), )

  return sampleTuple, countTuple


# generate appropriate filename if not supplied. 
# this script currently doesn't take a filename - only makes a new one. 
def filename_function(outFileName, fallbackName):
  toName = re.match(r'(.+)\_split\_library\_log\.txt', fallbackName)
  if toName:
    checkDir = re.match(r'^\.\.\/split\_library\_log\/(.+)', toName.group(1))
    if checkDir:
      outFileName = checkDir.group(1) + '.txt'
    else: 
      outFileName = toName.group(1) + '.txt'
  else: 
    outFileName = 'EMPTYFILENAME'
  outFileNameWDir = 'singleFiles/' + outFileName
  return outFileNameWDir


# Put all data together and make output files
def join_tuples(sll, ots, fileToWrite, origSLL, origOTS):
  new_ots = ()
  new_sll = ()
  new_sll_names = ()

  # get length before anything else to put at top of file
  lensll = len(sll[0])
  lenots = len(ots[0])

  # jive order of things and match sample names. 
  for i in range(len(sll[0])):
    for j in range(len(ots[0])):
      strMatch = '\\b' + sll[0][i] + '\\b'
      match = re.search(strMatch, ots[0][j])
      if match:
        new_sll_names += (sll[0][i], )
        new_sll += (sll[1][i], )
        new_ots += (ots[1][j], )

  # turn them into numpy arrays - maybe shouldhave just done at the top
  new_names = numpy.array(map(str, new_sll_names))
  new_sll_array = numpy.array(map(float, new_sll))
  new_ots_array = numpy.array(map(float, new_ots))
  new_percent = numpy.divide(new_ots_array, new_sll_array)
  
  

  # create new file to write barcode data
  new = open(fileToWrite, 'w')   
  
  # timestamp
  Time = time.time()
  st = datetime.datetime.fromtimestamp(Time).strftime('%Y-%m-%d %H:%M:%S')
  print >> new, st

  print >> new, '\n------------\n'
  print >> new, lensll, 'samples in', origSLL
  print >> new, lenots, 'samples in', origOTS

  print >> new, '\n------------'
  print >> new, 'sample\tsplitLibLog\totuTableStats\tpercent'
  for i in range(len(new_names)):
    out = [new_names[i], new_sll_array[i], new_ots_array[i], new_percent[i]]
    print >> new, '\t'.join(map(str, out))
  print >> new, '------------'
  print >> new, 'Mean = ', numpy.average(new_percent), 'percent of seqs made it into OTU table'
  print >> new, 'SD = ', numpy.std(new_percent)

  new.close()





def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: splitlogfile otustatsfile'
    sys.exit(1)

  SLL = read_SLL(args[0])
  OTS = read_OTS(args[1])

  file_to_write = filename_function('none', args[0])

  join_tuples(SLL, OTS, file_to_write, args[0], args[1])

if __name__ == '__main__':
  main()

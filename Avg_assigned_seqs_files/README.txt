Info for split library and OTU table stat harvesting. 

created by: James Meadow

date: 2014 May 09

-----------------

Each study has a single file in `otu_table_stats/` 
and at least one in `split_library_log/`. 

Those with multiple runs that went into a single OTU table 
have multiple `split_library_log` (SLL) files 
for a single `otu_table_stats` (OTS) file. 

the `harvestStats/` directory contains 3 scipts to 
automate harvesting those stats:

* `makeIndividualFiles.sh` = an executable list of respective files. 
this was done by hand since catching edge cases was a bear. 
the output goes to `singleFiles/` directory, 
and there is one for each SLL file. 
This is the one to execute first - it calls `harvestOTUstats.py`
* `harvestOTUstats.py` = does most of the work. pulls out data from
both sets of files, jives sample names, divides SLL / OTS, gets mean and sd, 
creates output files. Gets called by `makeIndividualFiles.sh`
* `makeSummary.py` = takes summary info from each in `singleFiles/` and 
puts them together into a tab delimited table. Call this after others are done. 


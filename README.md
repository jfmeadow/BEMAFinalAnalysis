## Built Environment Meta-Analysis

#### RI Adams, AC Bateman, HM Bik, JF Meadow


This repository contains data and scipts that were used 
to conduct a meta-analysis of 16 high-throughput sequence 
datasets from built environments around the world. 
The analysis also includes 7 putative source environments. 

* `merged_datasets` contains the main OTU tables (in biom format) that 
were used during the analyis. 
* `individual_biom_tables` contains lots of individual OTU tables from each 
individual study. These were tied together using the script `mergeOTUTables.sh`. This folder also contains the stats from the resulting merged otu table. 
* `fungi` contains an OTU table, a mapping file, and an ordination output. 
We did not find enough studies to conduct a meaningful analysis for fungi, so 
this folder is included just for posterity. 
* `pinch_biom_tables` We used the phinch online platform for extensive data exploration. 
The biom tables in this folder already have metadata embedded to use directly 
in phinch. 
* `R` Almost all analysis and figure generation happened in R. This folder contains 
scripts in RMarkdown format. All data should be included to rerun and further explore 
the analysis we carried out. 
* `scripts` contains the `pickTheseOTUs.sh` script that was used to generate 
OTU tables from raw sequence files. We processed all datasets with identical parameters using this script. 
This also contains a few of the QIIME commands we used to generate some preliminary analysis. 

This study is currently in review. 



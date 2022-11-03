## HOW TO USE THE SCRIPT
Firstly you have to clone the repo

`git clone https://github.com/Baribor/hng9-chip-007.git`

After that, to run the script, you run the command below:

`python worker.py`

This assumes you have python installed and properly setup on your devices.

## PROJECT STRUCTURE
The [input files](input%20files) folder serves as a folder to put all csv files to be processed. Currently only a file - [Team Bevel.csv](input%20files/Team%20Bevel.csv) is there.
For the script to work according, all csv files must adhere strictly to the following headings:

**Series Number**\
**Filename**\
**Description**\
**Gender**\
**UUID**\
**Hash**\
These were picked based on the priority of the team's presentation.
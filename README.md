# Texas Executed Offenders' Data
This project was written for Michigan Univerty's
Python 4 Everybody fifth module: Capstone.

All data is available at https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html
(Should it be public, though?)

Remember: they were real people, 
in spite of whatever crimes they may
or may not have commited. Respect, always.

# Python

## crawler.py
crawler.py is a webscrapper that checks
tdcj's robot.txt file before scrapping.
If allowed, it will collect all the links
containing offender's information and 
their last statements.
It will read each url, parse the html,
and save the data in a database. 
It counts how many:
- times each word has been used
- people are of a certain race
- times X grade was the highest grade in school
- people were of a certain gender

TO DO: not differentiate yall from y'all

## calculator.py
calculator.py calculates usefull 
averages and ratios.
TO DO: more complex calculations, 
such as race ratio for males

## worddump.py
worddump.py finds top n most used
words, and searches the database for
a specific word.
TO DO: more complex NLP analysis, 
such as creating a lemma, selecting
nound, adjectives, adverbs, verbs,
normalizing with an english corpus.

## gword.py
gword.py was written by the staff of
Michigan University for another project,
but I tweaked it a little.
It counts words, generates a .js file,
which, in turn, is used in a .htm file 
to create a Word Cloud on the browser.

# JavaScript and HTML
These scripts were developed by the 
Michigan University's staff, and were not
modified by me.

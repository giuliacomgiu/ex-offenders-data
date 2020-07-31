""" Word Cloud of Texas' executed offenders' last statements. 

WRITTEN BY MICHIGAN UNIVERSITY,
MODIFIED BY GIULIA CIPRANDI
for Michigan University's Fifth Python 4 Everyone
module: Capstone: Retrieving, processing and
visualizing data, week 7, visualizing a data source.
This script will prompt the user for how many 
most used words it wants to see and create a 
javascript file to be opened by an html that
will create a word cloud on the browser.

Remember: they were real people, 
in spite of whatever crimes they may
or may not have commited. Respect.
"""
import sqlite3

print("""   WORD CLOUD BASED ON LAS STATEMENTS' MOST USED WORDS
*4 or more characters only""",end='\n\n')

# Connecting to database
db = input('Enter database name or press enter for default: ')
if len(db) < 1: db = 'last-words'
conn = sqlite3.connect(db+'.sqlite')
cur = conn.cursor()

cur.execute('SELECT word, count FROM Words ORDER BY count DESC')
wc = cur.fetchall()

print('How many words would you like to see? Max is',len(wc))
many = int(input(''))

wc_show = dict()

# Getting words w 4+ chars and no '
# TODO: FIX JS FILE TO INCLUDE '
for row in wc:
    word = row[0]
    if len(word) > 3 and "'" not in word:
        wc_show[word] = row[1]
        many -= 1
    if many < 1: break

# Sorting, limiting words
x = sorted(wc_show, key=wc_show.get, reverse=True)
highest = max(wc_show.values())
lowest = min(wc_show.values())
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

# Creating javascript for wordcloud
fhand = open('gword.js','w')
fhand.write("gword = [")
first = True
for k in x:
    if not first : fhand.write( ",\n")
    first = False
    size = wc_show[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to gword.js")
print("Open gword.htm in a browser to see the vizualization")

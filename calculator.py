""" Average data of Texas' executed offenders. 

WRITTEN BY GIULIA CIPRANDI
or Michigan University's Fifth Python 4 Everyone
module: Capstone: Retrieving, processing and
visualizing data, week 5, analysing a data source.
This script will create the main average from
offenders' information.

Remember: they were real people, 
in spite of whatever crimes they may
or may not have commited. Respect.
"""

import sqlite3

print('AVERAGE CALCULATOR FOR TEXAS\' EXECUTED OFFENDERS.')
db = input("Enter database name or press enter for default:")
if len(db) < 1 : db = 'last-words'

conn = sqlite3.connect(db+'.sqlite')
cur = conn.cursor()

print('Average calculator starting',end='\n\n')

# Average age
cur.execute("""SELECT age FROM Inmate WHERE age NOT NULL""")
age = cur.fetchall() #list of tuples
a_sum = 0
for item in age: a_sum += item[0]
a_avg = a_sum/len(age)
print('The average age is',a_avg,end='\n\n')
del a_sum, age

# Average education level
cur.execute('''SELECT education AS ed, count  
	FROM Education WHERE ed NOT NULL''')
ed_count = cur.fetchall()
ed_sum = 0
ed_c_sum = 0
for item in ed_count:
	if item[0] == '': continue
	ed_sum += item[0]*item[1]
	ed_c_sum += item[1]
ed_avg = ed_sum/ed_c_sum
print('The average highest education grade is', ed_avg,end='\n\n')
del ed_sum, ed_count, ed_c_sum

# Race ratio
r = []
c = []
cur.execute('''SELECT race, count  
	FROM Race WHERE race NOT NULL''')
rc = cur.fetchall()
for item in rc:
	r.append(item[0])
	c.append(item[1])
r_total = sum(c)
for item in c:
	r_rate = 100*item/r_total
	print(r_rate,'% of inmates were',r[c.index(item)])
print('')
del r, rc, c, r_rate,r_total

# Gender ratio
g = []
c = []
cur.execute('''SELECT gender, count  
	FROM Gender WHERE gender NOT NULL''')
gc = cur.fetchall()
for item in gc:
	g.append(item[0])
	c.append(item[1])
g_total = sum(c)
for item in c:
	g_rate = 100*item/g_total
	print(g_rate,'% of inmates were',g[c.index(item)])
print('')
del g,c,gc,g_rate,g_total
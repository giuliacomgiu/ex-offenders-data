""" Word counter for Texas' executed offenders' last words. 

WRITTEN BY GIULIA CIPRANDI
or Michigan University's Fifth Python 4 Everyone
module: Capstone: Retrieving, processing and
visualizing data, week 3, identifying a data source.
This script will create a database to store executed
offenders' information, their last words and a total
word counter. The main tables from the db are:
	Inmate(name, last words, age, gender id, race id, education id)
	Words(word, count).

It also checks the robots.txt file to make sure website
allows crawling
"""

import sqlite3
import ssl
import urllib.robotparser
from urllib.request import urlopen
from urllib.parse import urlparse,urlunparse
from bs4 import BeautifulSoup

# Prompt url - NOT NECESSARY
'''url = input('Enter url or enter:')
if len(url) < 1: url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
url_p = urlparse(url)
if url_p.scheme == None or url_p.netloc == None:
	print('There was something wrong with the url',url)
	quit()
print('Default:',url)'''

def saveFile(content,fname=''):
	success = False
	f = input('Enter a valid file name or enter for default:')
	if len(f) > 1: fname = f
	print('Saving to file',fname)
	
	try:
		content = str(content)
		success = True
	except:
		print(type(content), 'cant be converted to string. Cant save')

	if success == True:	
		try:
			with open(fname,'w') as f:
				print(content,file=f)
		except:
			print('Couldn\'t open or write file.')
			success = False
	return

def openReadHTML(url):
	success = False
	raw = None

	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	#Open Html
	try:
		with urlopen(url,context=ctx) as doc:
			if doc.getcode() != 200:
				print('Error on page: ',url,'\n',doc.getcode())
				raise ValueError('Couldnt open page')

			if 'text/html' not in doc.info().get_content_type():
				raise ValueError('Non html page')
 			
 			# Read page
			success = True
			raw = doc.read()
	except ValueError as err:
		print(err)
	except KeyboardInterrupt:
		quit()
	except:
		print('Couldnt open for reasons unknown')

	return success, raw

def findLinks():
	print('GETTING LAST STATEMENTS\' URLS FROM')

	# Checking robots.txt file
	url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
	print(url)
	url_p = urlparse(url)
	robot_p = url_p._replace(path='/robots.txt',params='',query='',fragment='')
	robot_u = urlunparse(robot_p)
	print('Attempting to open robots.txt as', robot_u)
	try:
		robot = urllib.robotparser.RobotFileParser()
		robot.set_url(robot_u)
		robot.read()
		auth = robot.can_fetch('*',url)
		print('Authorization for crawling is',auth)
		if auth != True: input('Proceed at your own risk')
	except:
		input('Couldnt open robots.txt, proceed at your own risk:')


	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	#Opening url
	success, u_raw = openReadHTML(url)
	if success != True: 
		print('Couldnt get offernder\'s urls')
		quit()

	# Parsing
	u_soup = BeautifulSoup(u_raw, 'html.parser')

	f = input('Would you like to save to a file? (y/n)')
	if f.lower == 'y': saveFile(u_soup.prettify(),'raw_html')

	# Paths for last statement and offender info
	url_lw = []
	url_info = []
	for link in u_soup.find_all('a'):
		if "Last Statement of" in str(link):
			url_lw.append(link)
		if "Offender Information for" in str(link):
			url_info.append(link)

	# Replacing old list with actual urls
	for link in url_lw: 
		path = '/death_row/'+link['href']
		i = url_lw.index(link)
		new_parse = url_p._replace(path=path,params='',query='',fragment='')
		url_lw[i] = urlunparse(new_parse)
		if url_lw[i] == 'https://www.tdcj.texas.gov/death_row/dr_info/no_last_statement.html':
			url_lw[i] = ''
	s = input('Would you like to save last words urls in a file? (y/n)')
	if(s.lower() == 'y'): saveFile(url_lw,'url_last_words')

	for link in url_info: 
		path = '/death_row/'+link['href']
		i = url_info.index(link)
		new_parse = url_p._replace(path=path,params='',query='',fragment='')
		url_info[i] = urlunparse(new_parse)
		if url_info[i] == 'https://www.tdcj.texas.gov/death_row/dr_info/no_info_available.html':
			url_info[i] = ''
	s = input('Would you like to save info urls in a file? (y/n)')
	if(s.lower() == 'y'): saveFile(url_info,'url_info')

	return url_lw,url_info

def nameParser(name):
	name = str(name)
	name = name.strip(' </p>').split('#')[0].strip()
	name = name.rstrip(' 	,TDCJ-')
	
	#Correcting 'Garza, Jr., Manuel'
	if ',' in name:
		full_name = name.split(',')
		if len(full_name) > 2: print('Check',name)
		name = full_name.pop(-1).strip(' 	.')
		for word in full_name:
			name += ' ' + word.strip(' 	.')
	return name

def infoFinder(info,html_ref):
	while info not in html_ref:
		html_ref = html_ref.next_element
	result = str(html_ref.next_element.next_element.next_element.string)

	# Fixing last words bug but maintaining age/edu integrity
	if result.isdecimal() == False and len(result) <= 1:
		result = str(html_ref.next_element.next_element.next_element.next_element.string)
	if result == '': result = None
	return result

def wordCounter(sentence):
	#Counts both words and decimals

	word_count = dict()
	words = sentence.lower().strip('\'"').split()

	for word in words:
		word = word.strip(' \t.,"!?-<>')

		if word.isalpha() or word.isdecimal():
			word_count[word] = word_count.get(word,0) +1

		# Considering words with apostrophes (let's)
		elif "'" in word:
			for part in word.split("'"): 
				if part.isalpha():
					word_count[word] = word_count.get(word,0) +1

	return word_count

def createDatabase():
	db = input('Enter new db name or enter for default:')
	if len(db) < 1: db = 'last-words'
	conn = sqlite3.connect(db+'.sqlite')
	cur = conn.cursor()

	cur.execute('''CREATE TABLE IF NOT EXISTS Inmate(
		name TEXT UNIQUE,
		age INTEGER,
		last_words TEXT,
		education_id INTEGER,
		race_id INTEGER, 
		gender_id INTEGER)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Education(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		education INTEGER UNIQUE,
		count INTEGER)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Race(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		race TEXT UNIQUE,
		count INTEGER)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Gender(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		gender TEXT UNIQUE,
		count INTEGER)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Words(
		word TEXT UNIQUE,
		count INTEGER)''')

	conn.close()
	return db+'.sqlite'

def getData(url_lwords,url_info):
	# Opening and reading offender info
	success, raw = openReadHTML(url_info)
	if success != True: 
		name = ''
		age = None
		edu = None
		race = None
		gender = None
	else:
		# Parsing
		soup = BeautifulSoup(raw,'html.parser')
		main = soup.find(id='maincontent')

		name = infoFinder('Name',main)
		name = nameParser(name)
		age = infoFinder('Age (',main)
		edu = infoFinder('Education',main)
		edu = edu.lower().strip(' abcdefghijklmnopqrstuvwxyv.()')
		race = infoFinder('Race',main).lower()
		gender = infoFinder('Gender',main).lower()

	# Aquire correspondent name from Offender info 
	name_i = name

	# Attempts to open Last words' url
	success, raw = openReadHTML(url_lwords)
	if success != True: last_words = ''
	else:
		# Parsing
		soup = BeautifulSoup(raw,'html.parser')
		f = soup.find(id='maincontent')
		
		# Finding name
		elem = infoFinder('Offender:',f)
		name = nameParser(elem)

		# Checking name compatibility.
		# The names from last words often
		# Dont include middle names.
		count = 0
		for word in name.split():
			if word in name_i: count +=1
			if count > 1: 
				name = name_i
				break

		# Finding last statement
		last_words = infoFinder('Last Statement:',f)
		last_words = last_words.strip('  	</p>').strip()
		
		#print(last_words,end='\n\n')

	return edu, race, gender, last_words, name, age



### SCRIPT BEGINS ###

word_count = dict()
edu_c = dict()
race_c = dict()
gen_c = dict()

# Get all offender urls from texas website
url_lw,url_info = findLinks()

# Making sure both lists are the same size
diff = len(url_lw) - len(url_info)
if diff > 0: 
	for i in range(diff): url_info.append('')
elif diff < 0: 
	for i in range(diff): url_lw.append('')

db_name = createDatabase()

# Store offender's data in db and get info,
conn = sqlite3.connect(db_name)
cur = conn.cursor()

for i in range(len(url_lw)):
	
	# Getting the data and counting
	edu, race, gen, last_words, name, age = getData(url_lw[i],url_info[i])
	print(name)
	if edu != None: edu_c[edu] = edu_c.get(edu,0) + 1
	if gen != None: gen_c[gen] = gen_c.get(gen,0) + 1
	if race != None: race_c[race] = race_c.get(race,0) +1

	sentence_count = wordCounter(last_words)
	if len(sentence_count) > 3:
		for k,v in sentence_count.items():
			word_count[k] = word_count.get(k,0) + 1
	else: last_words = None

	# Updating database
	if edu != None:
		cur.execute('''INSERT OR IGNORE INTO 
			Education(education) VALUES (?)''', (edu,))
		cur.execute('''SELECT id FROM Education 
			WHERE education = ?''',(edu,))
		edu_id = cur.fetchone()[0]

	if race != None:
		cur.execute('''INSERT OR IGNORE INTO 
			Race(race) VALUES (?)''', (race,))
		cur.execute('''SELECT id FROM Race 
			WHERE race = ?''',(race,))
		race_id = cur.fetchone()[0]

	if gen != None:
		cur.execute('''INSERT OR IGNORE INTO 
			Gender(gender) VALUES (?)''', (gen,))
		cur.execute('''SELECT id FROM Gender 
			WHERE gender = ?''',(gen,))
		gender_id = cur.fetchone()[0]

	if name != None:
		cur.execute('''INSERT OR IGNORE INTO 
		Inmate(name,age,education_id,race_id,gender_id) 
		VALUES (?, ?, ?, ?, ?)''',(name, age, edu_id, race_id, gender_id))

	if last_words != None:
		cur.execute('''INSERT OR IGNORE INTO Inmate(name, last_words)
			VALUES (?, ?)''',(name, last_words))
		cur.execute('''UPDATE Inmate SET last_words=? WHERE name=?''',
			(last_words,name))
	
	if i%20 == 0 : conn.commit()
conn.commit()

print(edu_c,'\n',gen_c,'\n',race_c)
print(word_count)

# Store counts to database
for edu, count in edu_c.items():
	cur.execute("""UPDATE Education SET count = ?
	WHERE education = ?""",(count,edu))
conn.commit()

for gen, count in gen_c.items():
	cur.execute('''UPDATE Gender SET count = ?
		WHERE gender = ?''',(count,gen))
conn.commit()

for race, count in race_c.items():
	cur.execute('''UPDATE Race SET count = ?
		WHERE race = ?''',(count,race))
conn.commit()

i = 0
for word, count in word_count.items():
	cur.execute('''INSERT OR IGNORE INTO Words(word,count)
		VALUES (?, ?)''', (word, count))
	cur.execute('''UPDATE Words SET count=? 
		WHERE word=?''', (count, word))
	i += 1
	if i%50 == 0: conn.commit()
conn.commit()
conn.close()

""" Word Dump of Texas' executed offenders' last statements. 

WRITTEN BY GIULIA CIPRANDI
or Michigan University's Fifth Python 4 Everyone
module: Capstone: Retrieving, processing and
visualizing data, week 5, analysing a data source.
This script will display n most used words
and check the database for a specific word,
including words with apostrophes (Y'all).
and digits (7).

Remember: they were real people, 
in spite of whatever crimes they may
or may not have commited. Respect.
"""

import sqlite3


print('LAST STATEMENTS\' DUMP FOR TEXAS\' EXECUTED OFFENDERS.')

# Attempting to connect to database
con = False
while con == False:
	try:
		db = input("Enter database name or press enter for default:")
		if len(db) < 1 : db = 'last-words'

		conn = sqlite3.connect(db+'.sqlite')
		cur = conn.cursor()
		
		print('Connected to',db)
		con = True
	
	except KeyboardInterrupt: 
		print('\nGoing so soon? See you later!')
		quit()

	except:
		print('Couldnt connect to database\n\n')
		pass

# Prompt user for option and execute
while True:
	try:
		opt = input('''\nType in the option you want:
1) Most used words
2) Search for a word in databse
3) Quit\n''')
		opt = int(opt)

	except KeyboardInterrupt:
		print('Bye bye!')
		quit()

	except:
		print('Invalid input format. Digits only.')
		continue
	
	# N most used words
	try:
		if opt == 1:
			
			many = input('How many of the most used words would you like to see?\n').strip()
			
			if many.isdigit():
				many = int(many)
				cur.execute('''SELECT word, count  
					FROM Words WHERE word NOT NULL
					ORDER BY count DESC LIMIT ?''',(many,))
				wc = cur.fetchall()
			
				print(many,'most used words are:')
				for item in wc: print(item[0],', ',item[1],sep='')
				print('')

			else: 
				raise ValueError('Ivalid input format. Digits only.')
				continue

		# Search database for specific word
		elif opt == 2:
			valid = False
			word = input('Type in the desired word: ').lower().strip()
			
			# Check for words with ' (Let's)
			if "\'" in word:
				subwords = word.split("\'")
				if len(subwords) <=2: valid = True

			elif word.isdigit() or word.isalpha(): valid = True

			if valid == True:
				cur.execute('''SELECT count  
					FROM Words WHERE word = ?''',(word,))
				try: count = cur.fetchone()[0]
				except: count = 0
				print(word,'was used',count,'times')

			else: raise ValueError('Invalid format. Characters or digits only.')

		else: raise KeyboardInterrupt
	
	except KeyboardInterrupt:
		print('Bye bye!')
		quit()
	
	except ValueError as err:
		print(err)
		pass
	
	except:
		pass

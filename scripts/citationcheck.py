import re
import sys

BIB = 'report/biblio.bib'

def checker(file_content, biblio):
	"""
	This function checks the citations in the .bib file was cited in the .tex file and if the citation was checked
	back in the .bib file.
	Checked files have a '% X' at the end of the entry
	
	Args:
		file_content (_type_): content of the .tex file
		biblio (_type_): content of the .bib file
	"""

	match_table = {}

	# Extract all keys from biblio.bib
	bib_keys = re.findall(r'@[^{]+\{([^,]+),', biblio)
	
	citation_keys = re.findall(r'\\cite(?:p)?\{([^}]+)\}', file_content)
	
	# For each bib key, check if it was cited in the .tex file
	for key in bib_keys:
		match_table[key] = [key in citation_keys, False]
			
	# for each citation key, check if it was checked in biblio.bib
	for key in citation_keys:
		match_table[key][1] = key in bib_keys
		
	return match_table

def print_table(table):
	"""
	Print the table in a formatted way:
	|--------------|-------|---------|
	| Citation key | Cited | Checked |
	|--------------|-------|---------|
	|     key1     |  Y/N  |   Y/N   |
	|     key2     |  Y/N  |   Y/N   |
	|--------------|-------|---------|
	
	All columns are aligned to the center and have the same width, based on the longest string in the key column.

	Args:
		table (_type_): dictionary with the citation keys as keys and a list with two booleans as values
	"""
	
	# Find the kay with the longest length
	max_key_length = max([len(key) for key in table.keys()])
	
	# Print the table
	print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")
	print(f"| {'Citation key':^{max_key_length}} | {'Cited':^5} | {'Checked':^7} |")
	print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")
	for key, value in table.items():
		print(f"| {key:^{max_key_length}} | {'Y' if value[0] else 'N':^5} | {'Y' if value[1] else 'N':^7} |")
	print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")

def export_table(table, filename):
	"""
	Export the table to a .csv file
	"""

	filepath = 'documents/' + filename + '_citcheck.csv'

	with open(filepath, 'w') as file:
		file.write('Citation key,Cited,Checked\n')

		for key, value in table.items():
			file.write(f"{key},{value[0]},{value[1]}\n")
	
	print('Table exported to' + filepath)
	
# all the code below is executed when the script is called from the command line
if __name__ == '__main__':
    
	# Read the content of the .tex file passed as argument to the script
	filename = sys.argv[1]
	filepath = 'report/' + filename + '.tex'

	with open(filepath, 'r') as file:
		file_content = file.read()

	# Read the content of the .bib file
	with open(BIB, 'r') as file:
		biblio = file.read()

	# Check the citations
	table = checker(file_content, biblio)

	# if argument 2 is 1, print the table
	# if argument 2 is 2, export the table to a .csv file
	# if argument 2 is 3, print the table and export it to a .csv file
	if sys.argv[2] == '1':
		print_table(table)
	elif sys.argv[2] == '2':
		export_table(table, filename)
	elif sys.argv[2] == '3':
		print_table(table)
		export_table(table, filename)
	else:
		print('Invalid argument 2. Use 1, 2 or 3')
		exit(1)
import re
import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

BIB = 'report/biblio.bib'

def parse_bibtex_file(bibtex_filepath):
    with open(bibtex_filepath) as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
    return bib_database

def checker(file_content, bib_database):
	"""
	This function checks the citations in the .bib file was cited in the .tex file
 	and if the citation was checked back in the .bib file.
	Checked files have a '% X' at the end of the entry so the end of the entry looks like this:
		@article{key,
			...
			...
		} % X
	
	Args:
		file_content (): content of the .tex file
		bib_database (_type_): content of the .bib file

	Returns:
		match_table (dict): dictionary with the citation keys as keys and a list with two booleans as values
	"""

	cited_keys = re.findall(r'\\cite(?:p)?\{([^}]+)\}', file_content)
	checked_keys = [entry['ID'] for entry in bib_database.entries if 'note' in entry and entry['note'].strip().endswith('used')]

	match_table = {entry['ID']: [entry['ID'] in cited_keys, entry['ID'] in checked_keys] for entry in bib_database.entries}

	return match_table

def print_table(table):
	"""
	Print the table in a formatted way:
	|--------------|-------|---------|
	| Citation_key | Cited | Checked |
	|--------------|-------|---------|
	|     key1     |  Y/N  |   Y/N   |
	|     key2     |  Y/N  |   Y/N   |
	|--------------|-------|---------|
	
	All columns are aligned to the center and have the same width, based on the longest string in the key column.

	Args:
		table (dict): dictionary with the citation keys as keys and a list with two booleans as values
	"""
	
	# Find the kay with the longest length
	max_key_length = max([len(key) for key in table.keys()])
	
	# Print the table
	print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")
	print(f"| {'Citation_key':^{max_key_length}} | {'Cited':^5} | {'Checked':^7} |")
	print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")
	for key, value in table.items():
		print(f"| {key:^{max_key_length}} | {'Y' if value[0] else 'N':^5} | {'Y' if value[1] else 'N':^7} |")
	print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")

def export_table(table, filename):
	"""
	Export the table to a .csv file

	Args:
		table (dict): dictionary with the citation keys as keys and a list with two booleans as values
		filename (str): name of the .tex file without the extension
	"""

	filepath = 'documents/' + filename + '_citcheck.csv'

	with open(filepath, 'w') as file:
		file.write('Citation_key;Cited;Checked\n')

		for key, value in table.items():
			file.write(f"{key};{value[0]};{value[1]}\n")
	
	print('Table exported to ' + filepath)

def sort_table(table):
	"""
	Sort the table by putting cited keys first and uncited keys last.
	Sort the cited keys by putting checked keys first and unchecked keys last.
 
	returns: sorted_table (dict): the sorted table with the same structure as the input table
	"""
	
	# Sort the table by putting cited keys first and uncited keys last
	sorted_table = {k: v for k, v in sorted(table.items(), key=lambda item: item[1][0], reverse=True)}

	# Sort the cited keys by putting checked keys first and unchecked keys last
	sorted_table = {k: v for k, v in sorted(sorted_table.items(), key=lambda item: item[1][1], reverse=True)}

	return sorted_table
	
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

	# Parse the .bib file
	biblio = parse_bibtex_file(BIB)

	# Check the citations
	table = sort_table(checker(file_content, biblio))

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
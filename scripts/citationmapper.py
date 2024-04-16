import re
import sys
import os
import pandas as pd
import numpy as np


def mapper():
	"""
	Map the .tex files where each citation was cited and checked back in the .bib file.
	The function returns a dictionary that will be used to produce a table with the following
	format:
	|--------------|-------|---------|----------------|----------------|-----|----------------|
	| Citation_key | Cited | Checked | [texfilename1] | [texfilename2] | ... | [texfilenameN] |
	|--------------|-------|---------|----------------|----------------|-----|----------------|
	|     key1     |  Y/N  |   Y/N   |      Y/N       |      Y/N       | ... |      Y/N       |
	|     key2     |  Y/N  |   Y/N   |      Y/N       |      Y/N       | ... |      Y/N       |
	|--------------|-------|---------|----------------|----------------|-----|----------------|


	Returns:
		mapped_table (dict): dictionary with the citation keys as keys and a list 
	"""

	filepath = 'documents/citchecks/'

	# Get the list of .csv files in the directory
	files = [file for file in os.listdir(filepath) if file.endswith('.csv')]

	# Create a dictionary with the citation keys as keys and a list with two booleans as values
	mapped_table = {
		"Citation_key": [],
		"Cited": [],
		"Checked": [],
	}

	# for each file in the directory, add a new column to the table
	for file in files:
		# extract the name of the .tex file from the .csv file
		texfile = file.split('_')[0]

		# add the name of the .tex file to the dictionary as a key
		mapped_table[texfile] = []

		# read the .csv file
		df = pd.read_csv(filepath + file, delimiter=';')

		# add the citation keys to the dictionary
		mapped_table["Citation_key"] += df['Citation_key'].tolist()

		# add the cited and checked columns to the dictionary
		mapped_table["Cited"] += df['Cited'].tolist()
		mapped_table["Checked"] += df['Checked'].tolist()

		# add the .tex file to the dictionary
		mapped_table[texfile] = df['Cited'].tolist()

	return mapped_table



def print_mapped_table(table=mapper()):
	"""
	Print the mapped table in a formatted way:
	|--------------|-------|---------|----------------|----------------|-----|----------------|
	| Citation_key | Cited | Checked | [texfilename1] | [texfilename2] | ... | [texfilenameN] |
	|--------------|-------|---------|----------------|----------------|-----|----------------|
	|     key1     |  Y/N  |   Y/N   |      Y/N       |      Y/N       | ... |      Y/N       |
	|     key2     |  Y/N  |   Y/N   |      Y/N       |      Y/N       | ... |      Y/N       |
	|--------------|-------|---------|----------------|----------------|-----|----------------|
	
	All columns are aligned to the center and have the same width, based on the longest string in the key column.

	Args:
		table (dict): dictionary with the citation keys as keys and a list with two booleans as values
	"""

	# Get the length of the longest key
	max_key_length = max([len(key) for key in table['Citation_key']])


def export_mapped_table(table, filename):
	"""
	Export the mapped table to a .csv file

	Args:
		table (dict): dictionary with the citation keys as keys and a list with two booleans as values
		filename (str): name of the .tex file without the extension
	"""

	filepath = 'documents/citchecks/' + filename + '_citmap.csv'

	with open(filepath, 'w') as file:
		file.write('Citation_key;Cited;Checked\n')

		for key, value in table.items():
			file.write(f"{key};{value[0]};{value[1]}\n")
	
	print('Mapped table exported to ' + filepath)

print(mapper())
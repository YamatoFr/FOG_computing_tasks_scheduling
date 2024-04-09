from threading import local
import pandas as pd

def process_data(csv_file):
	# Read the CSV file into a pandas DataFrame
	df = pd.read_csv(csv_file, header=[0], sep=";")

	local_processing = 0
	remote_processing = 0

	# iterate through the rows of the penuultimate column
	for index, row in df.iterrows():

		# Get the value of the penultimate column
		value = row.iloc[-2]

		# Perform some operation on the value
		if value >= 12.0 and value <= 24.0:
			local_processing += 1
		elif value >= 60.0 and value <= 72.0:
			remote_processing += 1

	# Return the processed data 
	return local_processing, remote_processing

def process_data_v2(csv_file):
	# Read the CSV file into a pandas DataFrame
	df = pd.read_csv(csv_file, header=[0], sep=";")
	values = {}

	# iterate through the rows of the penuultimate column
	for index, row in df.iterrows():

		# Get the value of the last column
		# the data contained is a string with the following format:
		# "0.000/local_processing + 0.000/remote_processing"
		string = row.iloc[-1]

		# Parse the string to extract the values of local_processing and remote_processing
		value_local = float(string.split("/")[0])
		value_remote = float(string.split("/")[1].split("+")[1])

		# add the values to a list along with the index 
		# the index is used to identify the task
		values[index] = [value_local, value_remote]

	# Return the processed data 
	return values

if __name__ == "__main__":
	# Specify the path to your CSV file
	csv_file_path = "C:/Users/theof/OneDrive/Documents/Github/FOG_computing_tasks_scheduling/documents/fuzzy_results.csv"

	# Call the process_data function with the CSV file path
	print(process_data(csv_file_path))
	print(process_data_v2(csv_file_path))
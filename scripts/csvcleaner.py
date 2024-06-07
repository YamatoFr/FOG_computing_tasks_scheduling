import pandas as pd

# read the csv file
df = pd.read_csv("C:/Users/theof/OneDrive/Documents/Github/FOG_computing_tasks_scheduling/documents/fuzzy-results/fuzzy_results_maximum.csv", sep=";")
pd.options.mode.copy_on_write = True

df_copy = df.copy()

# get last column
last_column = df_copy.columns[-1]

# treat values in last column,  ignore header
for i in range(len(df)):
	# split the string
	local = float(df[last_column][i].split("/")[0])
	remote = float(df[last_column][i].split("/")[1].split(" + ")[1])

	# replace the string accordingly to the rules
	if local > remote:
		df_copy.loc[i, last_column] = "local_processing"
	elif remote > local:
		df_copy.loc[i, last_column] = "remote_processing"
	else:
		# no change
		pass


# save the new csv file
df_copy.to_csv("data3.csv", index=False)

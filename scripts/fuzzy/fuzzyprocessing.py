from math import nan
from fuzzyengine import Mean3Pi, AggregatedMean3Pi, engine
from engineV2 import engine_V2
from numpy.random import Generator, PCG64
import pandas as pd
import fuzzylite as fl

# random number generator for each input variable
# (bandwidth, battery, load, memory, nb_user) min: 0, max: 100
# (datasize) min: 0, max: 600
# (vm) min: 0, max: 50


# create an empty table to store the values, the headers are the variables
table = {
	"Bandwidth": [],
	"Datasize": [],
	"NB_concurrent_users": [],
	"Memory": [],
	"Load": [],
	"Processing": [],
	"Fuzzy_output": []
}

# create a copy of the table
table_copy = {
	"Bandwidth": [],
	"Datasize": [],
	"NB_concurrent_users": [],
	"Memory": [],
	"Load": [],
	"Processing": [],
	"Fuzzy_output": []
}

# define the input variables for ease of use
bandwidth = engine.input_variable("Bandwidth")
datasize  = engine.input_variable("Datasize")
load      = engine.input_variable("Load")
memory    = engine.input_variable("Memory")
nb_users  = engine.input_variable("NB_concurrent_users")

bandwidth_v2 = engine_V2.input_variable("Bandwidth")
datasize_v2  = engine_V2.input_variable("Datasize")
load_v2      = engine_V2.input_variable("Load")
memory_v2    = engine_V2.input_variable("Memory")
nb_users_v2  = engine_V2.input_variable("NB_concurrent_users")

def random_input(min, max):
	"""
	Generates a random integer between the given minimum and maximum values.

	Parameters:
	min (int): The minimum value for the random integer.
	max (int): The maximum value for the random integer.

	Returns:
	int: A random integer between min and max (inclusive).
	"""
	rng = Generator(PCG64())
	value = rng.integers(min, max)
	return value

def process_engine(engine, table=table, table_copy=table_copy):

	"""
	Start by setting the aggregation method to Maximum, then process the engine
	and add the results to the table. Then set the aggregation method to TriplePi
	and process the engine again, adding the results to the another table.

	Args:
		engine (Engine): the fuzzy engine
	"""

	# set the aggregation method to Maximum
	engine.output_variable("Processing").fuzzy = fl.Aggregated("Processing", 0, 100, fl.Maximum())

	engine.process()

	# if the output value != nan, store it in the table
	if engine.output_variable("Processing").fuzzy_value() != nan:
		table["Processing"].append(round(float(engine.output_variable("Processing").value), 3))
	else:
		table["Processing"].append("nan")

	table["Fuzzy_output"].append(engine.output_variable("Processing").fuzzy_value())

	# set the aggregation method to TriplePi
	engine.output_variable("Processing").fuzzy = AggregatedMean3Pi("Processing", 0, 100, Mean3Pi())

	engine.process()

	# if the output value != nan, store it in the table
	if engine.output_variable("Processing").fuzzy_value() != nan:
		table_copy["Processing"].append(round(float(engine.output_variable("Processing").value), 3))
	else:
		table_copy["Processing"].append("nan")

	table_copy["Fuzzy_output"].append(engine.output_variable("Processing").fuzzy_value())

	engine.restart()

def dual_process(engine, engine_v2, table=table, table_copy=table_copy):
	
	engine.process()

	# if the output value != nan, store it in the table
	if engine.output_variable("Processing").fuzzy_value() != nan:
		table["Processing"].append(round(float(engine.output_variable("Processing").value), 3))
	else:
		table["Processing"].append("nan")

	table["Fuzzy_output"].append(engine.output_variable("Processing").fuzzy_value())

	engine_v2.process()

	# if the output value != nan, store it in the table
	if engine_v2.output_variable("Processing").fuzzy_value() != nan:
		table_copy["Processing"].append(round(float(engine_v2.output_variable("Processing").value), 3))
	else:
		table_copy["Processing"].append("nan")

	table_copy["Fuzzy_output"].append(engine_v2.output_variable("Processing").fuzzy_value())

	engine.restart()

def generate_fuzzy_table(engine, engine_v2, table=table, table_copy=table_copy):

	# loop through the input variables and set the values
	for i in range(0, 500):
		# print the iteration number
		print("\nIteration: ", i+1)

		# set the input values
		bandwidth.value = random_input(1, 100)
		datasize.value  = random_input(1, 600)
		load.value      = random_input(1, 100)
		memory.value    = random_input(1, 100)
		nb_users.value  = random_input(1, 100)

		bandwidth_v2.value = bandwidth.value
		datasize_v2.value  = datasize.value
		load_v2.value      = load.value
		memory_v2.value    = memory.value
		nb_users_v2.value  = nb_users.value

		# store the values in the tables 
		table["Bandwidth"].append(bandwidth.value)
		table["Datasize"].append(datasize.value)
		table["Load"].append(load.value)
		table["Memory"].append(memory.value)
		table["NB_concurrent_users"].append(nb_users.value)

		table_copy["Bandwidth"].append(bandwidth.value)
		table_copy["Datasize"].append(datasize.value)
		table_copy["Load"].append(load.value)
		table_copy["Memory"].append(memory.value)
		table_copy["NB_concurrent_users"].append(nb_users.value)

		# process the engines
		dual_process(engine, engine_v2)

	df = pd.DataFrame(table)
	df_copy = pd.DataFrame(table_copy)

	# save the tables to csv files with ; as separator
	df.to_csv("documents/fuzzy-results/fuzzy_test_V1.csv", sep=";", index=False)
	df_copy.to_csv("documents/fuzzy-results/fuzzy_test_V2.csv", sep=";", index=False)

generate_fuzzy_table(engine, engine_V2)
from numpy import random as rd
from fuzzyengine import engine
from numpy.random import Generator, PCG64

# define the input variables for ease of use
bandwidth = engine.input_variable("Bandwidth")
datasize = engine.input_variable("Datasize")
battery = engine.input_variable("Residual_bat_charge")
load = engine.input_variable("Load")
memory = engine.input_variable("Memory")
vm = engine.input_variable("VM_available")
nb_users = engine.input_variable("NB_concurrent_users")

# random number generator for each input variable
# bandwidth, battery, load, memory, nb_user min: 0, max: 100
# datasize min: 0, max: 600
# vm min: 0, max: 50


def random_input(min, max):
	rng = Generator(PCG64())
	
	value = rng.integers(min, max)

	return value

# create an empty table to store the values, the headers are the variables
table = {
	"Bandwidth": [],
	"Datasize": [],
	"Residual_bat_charge": [],
	"Load": [],
	"Memory": [],
	"VM_available": [],
	"NB_concurrent_users": [],
	"Processing": [],
}

# loop through the input variables and set the values
for i in range(0, 20):
	# print the iteration number
	print("\nIteration: ", i)

	# set the input values
	bandwidth.value = random_input(0, 100)
	datasize.value = random_input(0, 600)
	battery.value = random_input(0, 100)
	load.value = random_input(0, 100)
	memory.value = random_input(0, 100)
	vm.value = random_input(0, 50)
	nb_users.value = random_input(0, 100)

	# store the values in the table
	table["Bandwidth"].append(bandwidth.value)
	table["Datasize"].append(datasize.value)
	table["Residual_bat_charge"].append(battery.value)
	table["Load"].append(load.value)
	table["Memory"].append(memory.value)
	table["VM_available"].append(vm.value)
	table["NB_concurrent_users"].append(nb_users.value)

	print("Bandwidth: ", bandwidth.fuzzy_value(), "\nDatasize: ", datasize.fuzzy_value(), "\nBattery: ", battery.fuzzy_value(), "\nLoad: ", load.fuzzy_value(), "\nMemory: ", memory.fuzzy_value(), "\nVM: ", vm.fuzzy_value(), "\nUsers: ", nb_users.fuzzy_value())

	engine.process()

	print("\nOutput value: ", round(float(engine.output_variable("Processing").value), 3))
	table["Processing"].append(round(float(engine.output_variable("Processing").value), 3))
	print("\nfuzzy output: ", engine.output_variable("Processing").fuzzy_value())
	# print("\n")

# save the table to a csv file, use ; as separator
import pandas as pd

df = pd.DataFrame(table)
df.to_csv("documents/fuzzy_results.csv", sep=';')


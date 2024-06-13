from ctypes import Array
import fuzzylite as fl
import numpy as np

from fuzzylite.types import Scalar

_all_ = [
	"Mean3Pi",
	"AggregatedMean3Pi",
	"engine"
	]

def check_zeros(scalar: Scalar) -> bool:
	"""
	Check if the given scalar value contains any zeros or NaN values.

	Parameters:
		scalar (Scalar): The scalar value to check for zeros or NaN values.

	Returns:
		bool: True if the scalar contains zeros or NaN values, False otherwise.

	Raises:
		TypeError: If the type of scalar is not supported.
	"""
	if isinstance(scalar, (float, np.floating, Array)):
		return scalar == 0 or np.isnan(scalar)
	elif isinstance(scalar, np.ndarray):
		return np.count_nonzero(scalar) != np.size(scalar) or np.isnan(scalar).any() # type: ignore
	else:
		raise TypeError("Unsupported type for scalar: " + str(type(scalar)))

# create custom 3pi aggregation operator
class Mean3Pi(fl.SNorm):
	def compute(self, a: Scalar, b: Scalar) -> Scalar:

		a = fl.scalar(a)
		b = fl.scalar(b)

		if not check_zeros(a) and not check_zeros(b):
			numerator = np.sqrt(a) * np.sqrt(b)
			denominator = np.sqrt(a) * np.sqrt(b) + np.sqrt(1 - a) * np.sqrt(1-  b)

			result = numerator / denominator

			return result

		elif check_zeros(a) or check_zeros(b):
			if not check_zeros(a) and check_zeros(b):
				return np.sqrt(a) / (np.sqrt(a) + np.sqrt(1 - a))
			elif check_zeros(a) and not check_zeros(b):
				return np.sqrt(b) / (np.sqrt(b) + np.sqrt(1 - b))

		return 0.0

class AggregatedMean3Pi(fl.Aggregated):
	def membership(self, x: Scalar) -> Scalar:
		r"""Aggregate the activated terms' membership function values of $x$ using the aggregation operator.

		Args:
			x: scalar

		Returns:
			
		"""

		if self.terms and not self.aggregation:
			raise ValueError("expected an aggregation operator, but found none")

		y = fl.scalar(0.0)
		
		for term in self.terms:

			if not check_zeros(x):
				y = self.aggregation.compute(y, term.membership(x))  # type: ignore
			
		return y

# import the engine
engine = fl.Engine(
	name="TaskOffloading",
	input_variables=[
		fl.InputVariable(
			name="Bandwidth",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Trapezoid("bw_low", 0.0, 20.0, 30.0, 40.0),
				fl.Trapezoid("bw_medium", 35.0, 45.0, 60.0, 70.0),
				fl.Trapezoid("bw_high", 65.0, 75.0, 90.0, 100.0)
			]
		),
		fl.InputVariable(
			name="Datasize",
			minimum=0.0,
			maximum=600.0,
			terms=[               
				fl.Trapezoid("data_low", 0.0, 0.0, 230.0, 360.0),
				fl.Trapezoid("data_medium", 250.0, 350.0, 470.0, 590.0),
				fl.Trapezoid("data_high", 450.0, 540.0, 600.0, 600.0)
			]
		),
		fl.InputVariable(
			name="Load",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Trapezoid("load_low", 0.0, 0.0, 25.0, 40.0),
				fl.Trapezoid("load_medium", 35.0, 45.0, 60.0, 70.0),
				fl.Trapezoid("load_high", 65.0, 80.0, 100.0, 100.0)
			]
		),
		fl.InputVariable(
			name="Memory",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Trapezoid("mem_low", 0.0, 0.0, 25.0, 40.0),
				fl.Trapezoid("mem_medium", 35.0, 45.0, 60.0, 70.0),
				fl.Trapezoid("mem_high", 65.0, 80.0, 100.0, 100.0)
			]
		),
		fl.InputVariable(
			name="NB_concurrent_users",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Trapezoid("user_low", 0.0, 0.0, 25.0, 40.0),
				fl.Trapezoid("user_medium", 30.0, 40.0, 60.0, 70.0),
				fl.Trapezoid("user_high", 60.0, 75.0, 100.0, 100.0)
			]
		)
	],
	output_variables=[
		fl.OutputVariable(
			name="Processing",
			minimum=0.0,
			maximum=100.0,
			aggregation = fl.Maximum(),
			defuzzifier=fl.Centroid(200),
			terms=[
				fl.Trapezoid("local_processing", 0.0, 12.0, 24.0, 48.0),
				fl.Trapezoid("remote_processing", 36.0, 60.0, 72.0, 100.0)
			]
		)
	],
	rule_blocks = [
		fl.RuleBlock(
	  		name = "Mamdani",
			conjunction = fl.Minimum(),
			disjunction = fl.Maximum(),
			implication = fl.Minimum(),
			activation = fl.General(),
			rules = [
				fl.Rule.create("if Bandwidth is bw_low then Processing is local_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is not data_low then Processing is remote_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and (Load is load_high or Memory is mem_low) then Processing is remote_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and (NB_concurrent_users is user_low or Memory is mem_low) then Processing is remote_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and NB_concurrent_users is not user_low and Memory is not mem_low and Load is load_low then Processing is local_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and NB_concurrent_users is not user_low and Memory is not mem_low and Load is not load_low then Processing is remote_processing"),
			]
		)
	]
)

fl.FllExporter().to_file("scripts/fuzzy/task_offloading.fll", engine)
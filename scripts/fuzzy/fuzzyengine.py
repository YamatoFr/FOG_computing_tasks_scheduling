import fuzzylite as fl
from numpy import minimum

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
			name="Residual_bat_charge",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Trapezoid("bat_low", 0.0, 0.0, 25.0, 35.0),
				fl.Trapezoid("bat_medium", 25.0, 40.0, 60.0, 75.0),
				fl.Trapezoid("bat_high", 60.0, 75.0, 100.0, 100.0)
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
			name="VM_available",
			minimum=0.0,
			maximum=50.0,
			terms=[
				fl.Trapezoid("vm_low", 0.0, 0.0, 15.0, 20.0),
				fl.Trapezoid("vm_medium", 15.0, 22.5, 27.5, 35.0),
				fl.Trapezoid("vm_high", 30.0, 35.5, 50.0, 50.0)
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

				fl.Rule.create("if Bandwidth is not bw_high and (Datasize is data_high or Datasize is data_medium) then Processing is remote_processing"),

				fl.Rule.create("if Bandwidth is bw_medium and Datasize is data_low and NB_concurrent_users is user_low then Processing is remote_processing"),

				fl.Rule.create("if (Bandwidth is bw_medium or Bandwidth is bw_high) and Datasize is data_low and (Load is load_high or Memory is mem_low) then Processing is remote_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and (VM_available is vm_medium or VM_available is vm_high) and (NB_concurrent_users is user_low or Memory is mem_low) then Processing is remote_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and VM_available is vm_low and NB_concurrent_users is not user_low and Memory is not mem_low and Load is load_low then Processing is local_processing"),

				fl.Rule.create("if Bandwidth is not bw_low and Datasize is data_low and VM_available is not vm_low and NB_concurrent_users is not user_low and Memory is not mem_low and Load is not load_low then Processing is remote_processing"),
			]
        )
    ]
)
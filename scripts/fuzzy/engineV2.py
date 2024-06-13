import fuzzylite as fl

# import the engine
engine_V2 = fl.Engine(
	name="TaskOffloading",
	input_variables=[
		fl.InputVariable(
			name="Bandwidth",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Triangle("bw_low", 0.0, 20.0, 40.0),
				fl.Triangle("bw_medium", 30.0, 37.0, 75.0),
				fl.Triangle("bw_high", 65.0, 82.0, 100.0)
			]
		),
		fl.InputVariable(
			name="Datasize",
			minimum=0.0,
			maximum=600.0,
			terms=[               
				fl.Triangle("data_low", 0.0, 180.0, 360.0),
				fl.Triangle("data_medium", 250.0, 420.0, 590.0),
				fl.Triangle("data_high", 450.0, 600.0, 600.0)
			]
		),
		fl.InputVariable(
			name="Load",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Triangle("load_low", 0.0, 20.0, 40.0),
				fl.Triangle("load_medium", 35.0, 52.0, 70.0),
				fl.Triangle("load_high", 65.0, 82.0, 100.0)
			]
		),
		fl.InputVariable(
			name="Memory",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Triangle("mem_low", 0.0, 20.0, 40.0),
				fl.Triangle("mem_medium", 35.0, 52.0, 70.0),
				fl.Triangle("mem_high", 65.0, 82.0, 100.0)
			]
		),
		fl.InputVariable(
			name="NB_concurrent_users",
			minimum=0.0,
			maximum=100.0,
			terms=[
				fl.Triangle("user_low", 0.0, 20.0, 40.0),
				fl.Triangle("user_medium", 30.0, 50.0, 70.0),
				fl.Triangle("user_high", 60.0, 80.0, 100.0)
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
				fl.Triangle("local_processing", 0.0, 24.0, 48.0),
				fl.Triangle("remote_processing", 36.0, 62.867, 100.0)
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


fl.FllExporter().to_file("scripts/fuzzy/task_offloading_V2.fll", engine_V2)
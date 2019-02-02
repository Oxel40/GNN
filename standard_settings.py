def get_standard_settings():
	out = {}

	out["node_add_rate"] = 0.2
	out["connection_add_rate"] = 0.3
	out["new_weight_min"] = -6.
	out["new_weight_max"] = 6.
	out["weight_change_rate"] = 0.8
	out["weight_change_magnitude_min"] = 0.8
	out["weight_change_magnitude_max"] = 1.2
	out["activation_change_rate"] = 0.

	#out[""] = 	
	return out
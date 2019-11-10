def get_standard_settings():
	out = {}

	out["computing_threads"] = 4

	out["node_add_rate"] = 0.2
	out["node_remove_rate"] = 0.05
	out["connection_add_rate"] = 0.3

	out["new_weight_min"] = -6.
	out["new_weight_max"] = 6.
	out["weight_change_rate"] = 0.8
	out["weight_change_magnitude_min"] = 0.8
	out["weight_change_magnitude_max"] = 1.2

	out["activation_change_rate"] = 0.

	out["sexual_breeding"] = False
	out["new_individual_rate"] = 0.3

	return out

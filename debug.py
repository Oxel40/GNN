import GNN

def te(y, y_):
	out = 0
	for q in range(len(y)):
		out += (y[q][0] - y_[q][0])**2
	out *= -1
	return out

sett = GNN.get_standard_settings()

sett["weight_change_magnitude_min"] = 0
sett["weight_change_magnitude_max"] = 2

e = GNN.Population(1000, (5, 3), 2, 1, [GNN.Activation.sigmoid], sett)

for x in range(101):
	_ = e.fitt([[1, 1], [1, 0], [0, 0], [0, 1]], te, [[0], [1], [0], [1]], True)
	if _ == 0:
		print(x, _)
		break
	else:
		if x % 10 == 0:
			print(x, _)

ind = e.get_fittest_individual([[1, 1], [1, 0], [0, 0], [0, 1]], te, [[0], [1], [0], [1]])
print(ind.run([[1, 1]]))
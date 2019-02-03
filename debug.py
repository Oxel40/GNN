import GNN
from copy import deepcopy

sett = GNN.get_standard_settings()
sett["node_add_rate"] = 0.
sett["connection_add_rate"] = 1.

e = GNN.Genome(1, (5, 3), 2, 1, [GNN.Activation.sigmoid], sett)
for x in e.space:
       print(x)

print("-"*20)

for x in e.space:
	for y in x:
		try:
			print(y.con, end=", ")
		except:
			print(y, end=", ")
	print("")

print("-"*20)

q = deepcopy(e)

e.mutate()

for x in e.space:
       print(x)

print("-"*20)

for x in e.space:
	for y in x:
		try:
			print(y.con, end=", ")
		except:
			print(y, end=", ")
	print("")

print("-"*20)

print("q:", q.run([1, 0]))
print("e:", e.run([1, 0]))
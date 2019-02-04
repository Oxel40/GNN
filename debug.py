import GNN

sett = GNN.get_standard_settings()

sett["computing_threads"] = 4

e = GNN.Population(10000, (5, 3), 2, 1, [GNN.Activation.sigmoid], sett)

res = e.run([1, 1], lambda x: x)
print(res)
print(len(res))
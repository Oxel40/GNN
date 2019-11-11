import GNN
import time


def te(y, y_):
    out = 0.
    for q in range(len(y)):
        out -= (y[q][0] - y_[q][0])**2
    return out


sett = GNN.get_standard_settings()

sett["weight_change_magnitude_min"] = 0
sett["weight_change_magnitude_max"] = 2

sett["computing_threads"] = 4

e = GNN.Population(1000000, (5, 4), 3, 1, [GNN.Activation.sigmoid], sett)
start = time.time()
for x in range(1):
    _ = e.fitt([[1, 1, 0], [1, 0, 0], [0, 0, 1], [0, 1, 1], [
               1, 1, 1]], te, [[0], [1], [0], [1], [0]], True)
    if _ == 0:
        print(x, _)
        break
    else:
        if x % 10 == 0:
            print(x, _)
print(time.time() - start)
ind = e.get_fittest_individual([[1, 1, 0], [1, 0, 0], [0, 0, 1], [0, 1, 1], [
                               1, 1, 1]], te, [[0], [1], [0], [1], [0]])
print(ind.run([[1, 1, 1], [0, 0, 0]]))

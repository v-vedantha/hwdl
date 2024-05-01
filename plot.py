import matplotlib.pyplot as plt
from test import *
import math
import numpy
class Trial:
    def __init__(self):
        self.vals = []
    def add(self, val):
        self.vals.append(val)
    def mean(self):
        return sum(self.vals) / len(self.vals)
    def std(self):
        return numpy.std(self.vals)

trials = 10
# Plot 1. N = T. 2 streams of the same length, but increasing density.
densities = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
results=[[],[],[],[]]
buf=10
for d in densities:
    for i in range(4):
        results[i].append(Trial())
l = 1000
for trial in range(trials):
    for idx, d in enumerate(densities):
        temp = test_matmul(d, d, 1, l, 1, buf, buf, buf)
        print(temp)
        assert(len(temp)   == 4)
        for i in range(4):
            results[i][idx].add(temp[i][1])
for i in range(4):
    plt.errorbar(densities, list(map(lambda x : x.mean(), results[i])), list(map(lambda x: x.std(), results[i])), label=collider_names[i], capsize=3)
plt.xlabel('Density')
plt.ylabel('Cycles')
plt.title(f'Density vs Cycles for a {l} length array, buffer size {buf}')
# Show labels
plt.legend()
plt.savefig('plt1.png')
plt.clf()




# Plot 2. N = T. 2 streams of the same sparsity, but increasing length.
lengths = [100, 200, 300, 400, 500, 600, 700]
results=[[], [], [], []]
density = 0.05
buf = 10
for l in lengths:
    for i in range(4):
        results[i].append(Trial())
for trial in range(trials):
    for idx, l in enumerate(lengths):
        temp = test_matmul(density, density, 1, l, 1, buf, buf, buf)
        print(temp)
        assert(len(temp)  == 4)
        for i in range(4):
            results[i][idx].add(temp[i][1])

for i in range(4):
    plt.errorbar(lengths, list(map(lambda x : x.mean(), results[i])), list(map(lambda x: x.std(), results[i])), label=collider_names[i], capsize=5)
plt.xlabel('Density')
plt.ylabel('Cycles')
plt.title(f'Array length vs Cycles for a {density} dense {l} length array, buffer size {buf}')
# Show labels
plt.legend()
plt.savefig('plt2.png')
plt.clf()

# Plot streams of same sparsity, and length, but increasing N, T
Ts = [1, 2, 4, 8, 16, 32]
results=[[], [], [], []]
density = 0.05
length = 1000
for t in Ts:
    for i in range(4):
        results[i].append(Trial())
for trial in range(trials):
    for idx, t in enumerate(Ts):
        temp = test_matmul(density, density, 1, l, 1, t, t, t)
        print(temp)
        assert(len(temp)  == 4)
        for i in range(4):
            results[i][idx].add(temp[i][1])

for i in range(1,4):
    plt.errorbar(Ts, list(map(lambda x : x.mean(), results[i])), list(map(lambda x: x.std(), results[i])), label=collider_names[i], capsize=5)
plt.xlabel('Buffer size')
plt.ylabel('Cycles')
plt.title(f'Buffer size vs Cycles for a {density} dense {length} length array')
# Show labels
plt.legend()
plt.savefig('plt3.png')
plt.clf()

# Plot skips for ideal and hardware version
# results_hist = []
# for trial in range(trials):
#     results_hist.append(test_skips(0.05, 0.05, 1, 1000, 1, 10, 10, 10))

# results_lookahead = []
# results_friendly = []
# for result in results_hist:
#     results_lookahead.append(result[0])
#     results_friendly.append(result[1])

# hists = []
# for result in results_lookahead:
#     hists.append(numpy.histogram(result[1], bins=range(10))[0])
# hists=numpy.vstack(hists)
# breakpoint()
# stds = numpy.std(hists, axis=1)
# means = numpy.mean(hists, axis=1)
# plt.bar(range(10), means, label=collider_names[result[0]], alpha=0.5, yerr=stds)

# hists = []
# for result in results_friendly:
#     hists.append(numpy.histogram(result[1], bins=range(10))[0])
# hists=numpy.vstack(hists)
# stds = numpy.std(hists, axis=1)
# means = numpy.mean(hists, axis=1)
# plt.bar(range(10), means, label=collider_names[result[0]], alpha=0.5, yerr=stds)
# plt.xlabel('Skips')
# plt.ylabel('Frequency')
# plt.title('Skips for 0.05 dense 1000 length array')
# plt.legend()

# plt.savefig("plt4.png")
# plt.clf()

# Plot a histogram of the results
density = 0.05
length = 1000
buf = 10
results = test_skips(density, density, 1, length, 1, buf, buf, buf)
for result in results:
    plt.hist(result[1], bins=8, label=collider_names[result[0]], alpha=0.5)
plt.xlabel('Skips')
plt.ylabel('Frequency')
plt.title(f'Skips for {density} dense {length} length array')
plt.legend()
plt.savefig('plt4.png')




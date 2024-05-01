import matplotlib.pyplot as plt
from test import *


# Plot 1. N = T. 2 streams of the same length, but increasing density.
densities = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
results=[[], [], [], []]
l = 1000
for d in densities:
    temp = test_matmul(d, d, 1, l, 1, 10, 10, 10)
    print(temp)
    assert(len(temp)   == 4)
    for i in range(4):
        results[i].append(temp[i][1])

print(results)
for i in range(4):
    plt.plot(densities, results[i], label=collider_names[i])
plt.xlabel('Density')
plt.ylabel('Cycles')
plt.title('Density vs Cycles for a 1000 length array')
# Show labels
plt.legend()
plt.savefig('plt1.png')
plt.clf()




# Plot 2. N = T. 2 streams of the same sparsity, but increasing length.
lengths = [100, 200, 300, 400, 500, 600, 700]
results=[[], [], [], []]
density = 0.05
for l in lengths:
    temp = test_matmul(density, density, 1, l, 1, 10, 10, 10)
    print(temp)
    assert(len(temp)  == 4)
    for i in range(4):
        results[i].append(temp[i][1])

print(results)
for i in range(4):
    plt.plot(lengths, results[i], label=collider_names[i])
plt.xlabel('Density')
plt.ylabel('Cycles')
plt.title('Array length vs Cycles for a 0.05 dense length array')
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
    temp = test_matmul(density, density, 1, l, 1, t, t, t)
    print(temp)
    assert(len(temp)  == 4)
    for i in range(4):
        results[i].append(temp[i][1])

print(results)
for i in range(4):
    plt.plot(Ts, results[i], label=collider_names[i])
plt.xlabel('T/N')
plt.ylabel('Cycles')
plt.title('T/N vs Cycles for a 0.05 dense 1000 length array')
# Show labels
plt.legend()
plt.savefig('plt3.png')
plt.clf()

# Plot skips for ideal and hardware version
results = test_skips(0.05, 0.05, 1, 1000, 1, 10, 10, 10)

# Plot a histogram of the results
for result in results:
    plt.hist(result[1], bins=8, label=collider_names[result[0]], alpha=0.5)
plt.xlabel('Skips')
plt.ylabel('Frequency')
plt.title('Skips for 0.05 dense 1000 length array')
plt.legend()
plt.savefig('plt4.png')




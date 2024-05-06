For people just looking at this
test.py contains the simulators for the 4 intersection units we evaluate
plot.py runs the simulations and generates plots. Just run ```python plots.py ```


So the plan is 
1) We need to be able to simulate a really simple sparse matrix multiplication. Ideally this uses TEAAL or something.
- Ok after testing, TEAAL is entirely unfeasable. Instead we need to come up with some way to argue that large matrices are useful.
- So maybe just estimate how long a matrix takes using sparseloop (this is much faster)
- Ok, but these assume perfect intersections. What about imperfect intersections?

Big news:
- Extensor does poorly with skipping giving zero speedup on NN style worklaods since the sparsity is not high enough for large skips if S/T is large
- Just a look at next N does massively better


2) Test this out with sim
- Simulated basic
- Simulated extensor
- Simulated look at next N
- Simulated a hardware friendly version of look at next N

We get roughly 20-25% speedup using what I believe is the exact same hardware

Now the next steps.
 - Synthesize on real hardware? IMO not worth it. It'll take a full day for a single number. I don't think that amount of time exists.

Understand wether we are bottlenecked by the next intersection generator
 - How to test this? Once again will need to simulate the entire thing.
 - One option is to see how long the matmul will take normally, and how long it will take to generate the intersections.
 - Yeah this is a pretty decent approach. Can use sparseloop for this.
 - Maybe talk to joel about this. Seems a little troll.

Results (just in case anyone actually looks at this repo):


Simulating a matmul with parameters densityA 0.25 densityB 0.5 A = [80, 90] B = [90, 80]
- Algorithmic ops:  576000
- Real computes: 72281
- classic : 351670 cycles
- extensor (with skip optimizations) : 301565 cycles
- our custom version (lookahead) : 253858 cycles
- hardware friendy lookahead : 268569 cycles

Simulating a matmul with parameters densityA 0.25 densityB 0.5 A = [8, 900] B = [900, 8]
- Algorithmic ops:  57600
- Real computes: 7110
- classic : 35956 cycles
- extensor (with skip optimizations) : 35335 cycles
- our custom version (lookahead) : 24940 cycles
- hardware friendy lookahead : 28820 cycles

Why not just use a vector pipeline? Causes you to need an NxN comparison. The idea here is we use the exact same hardware as the single-cycle version but get 20% better performance.

Yeah so the goal is how can we do more by just reading out a single value in a particular cycle from the containing memory.

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

T = 10
Simulating a matmul with parameters densityA 0.25 densityB 0.5 A = [80, 90] B = [90, 80]
- Algorithmic ops:  576000
- Real computes: 70074
- classic : 349415 cycles
- extensor (with skip optimizations) : 311537 cycles
- our custom version (lookahead) : 248786 cycles
- hardware friendy lookahead : 264281 cycles

Simulating a matmul with parameters densityA 0.25 densityB 0.5 A = [8, 900] B = [900, 8]
- Algorithmic ops:  57600
- Real computes: 7233
- classic : 35894 cycles
- extensor (with skip optimizations) : 35450 cycles
- our custom version (lookahead) : 25278 cycles
- hardware friendy lookahead : 28720 cycles

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


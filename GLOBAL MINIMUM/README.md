# **Approximating Global Minimum of 1D and 2D Functions**

**[Polish version](README_PL.md)**

The task involves creating an algorithm to search for the global minimum of the following functions: One-dimensional function:

\[ f(x) = 2x^2 + 3x + 1 \]

Two-dimensional function:

\[ g(x_1, x_2) = 1 - 0.6e^{-x_1^2 - x_2^2} - 0.4e^{-(x_1+1.75)^2 - (x_2-1)^2} \]

The gradients of the above functions are provided in the task instructions and are included in the code. Key algorithm parameters are described in points 2 and 3, namely:

- **learning\_rate** – step size coefficient,
- **precision** – accuracy of the found solution (between the last two iterations),
- **max\_steps** – iteration limit.

## 1. **ONE-DIMENSIONAL FUNCTION \( f(x) \)**

Analysis of running the algorithm for an initial value (x = 2):

![Fig. 1](img/fig_1.jpeg)

*Fig.  1. Function \( f(x) \) for \( x=2 \).* 

Iteration 1: 2 

Iteration 2: 1.89 

Iteration 3: 1.7844 

(...) 

Iteration 169: -0.7471099866795737 
Iteration 170: -0.7472255872123907 
Iteration 173: -0.7475453771279417 

**RESULTS SUMMARY FOR \( f(x) \):**

- *learning\_rate:*   0.01 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*     2 
- *x\_final:*       -0.747643562042824 
- *iterations:*    173 

*Learning\_rate* determines how quickly the algorithm should move towards the minimum of the function. If it is too small, it may prolong the computation time and provide less accurate solutions. For example:

**RESULTS SUMMARY FOR \( f(x) \):**

- *learning\_rate:*   **0.001** 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*     2 
- *x\_final:*    -0.72512311472929 
- *iterations:*    1174 

Despite the smaller learning rate, the final result is less accurate. On the other hand, in the case of a too large *learning\_rate*, the algorithm may "skip" local minimums and never reach them:

**RESULTS SUMMARY FOR \( f(x) \):**

- *learning\_rate:*   **0.5** 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*     2 
- *x\_final:*    2.0 
- *iterations:*    10000 

Consider another one-dimensional function with two minima:

\[ f_2(x) = 4 \cdot 3 - 8 \cdot x + 1 \]

![Fig. 2](img/fig_2.jpeg)

*Fig.  2. Function \( f_2(x) \).* 

The final result strongly depends on the initial point. Points greater than \( x = 0 \) have little chance of finding the global minimum. A random factor or an increased *learning\_rate* could be used, with the consequences described above, as the algorithm will converge towards the most promising direction (mathematically).

The discussion of the algorithm continues in point 2. Two-dimensional function.

## 2. **TWO-DIMENSIONAL FUNCTION \( g(x) \)**

![Fig. 3](img/fig_3.jpeg)

*Fig.  3. Source of graphs: wolframalpha.com.* 

Analysis of running the algorithm for example values **\( x_1 = 1, x_2 = 1 \)**:

![Fig. 4](img/fig_4.jpeg)

*Fig.  4. Function \( g(x) \) for the starting point (1,1).* 

Iteration 1: (0.9983645459581533, 0.9983759766011606) 
Iteration 2: (0.9967210560921321, 0.9967440018664104) 
Iteration 3: (0.9950694732051684, 0.9951040195353547) 

(...) 

Iteration 540: (-0.011180401331944471, 0.02053098715316187) 
Iteration 541: (-0.011305496913203547, 0.020430748805464097) 
Iteration 542: (-0.011429135203858663, 0.02033176213582331) 

**RESULTS SUMMARY FOR \( g(x) \):**

- *learning\_rate:*   0.01 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*        (1, 1) 
- *x\_final:*          (-0.011429135203858663, 0.02033176213582331) 
- *iterations:*     542 

The algorithm ended after 542 iterations. A significant increase in *learning\_rate = 1* will multiply the gradient by a greater value, and the "step" to the next point will be larger, so the solution will be found in fewer iterations:

**RESULTS SUMMARY FOR \( g(x) \):**

- *learning\_rate:*   1 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*        (1, 1) 
- *x\_final:*          (-0.02194210570455997, 0.012552612680346655) 
- *iterations:*     9 

However, now there is a risk that multiplying by a too large value, we might "jump over" the correct solution, and the algorithm will converge to the wrong point. For example, for *learning\_rate = 1:*

![Fig. 5](img/fig_5.jpeg)

*Fig. 5. Function g(x) for learning\_rate = 1.*

The *“precision”* parameter, comparing the difference between the last two points, has similar advantages and disadvantages: a higher precision value may reduce the number of iterations but may also not get close enough to the ideal result.

The *“max\_steps”* parameter acts as a safeguard to prevent the algorithm from taking a very large number of steps. Exceeding the assumed value indicates that the result with the required accuracy has not been found.

Let's consider other initial points for the function g(x): **(x1 = 4, x2 = 4)**

![Fig. 6](img/fig_6.jpeg)

*Fig. 6. Function g(x) for a distant initial point.*

**RESULTS SUMMARY FOR g(x):**

- *learning\_rate:*   0.01 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*        (4, 4) 
- *x\_final:*          (3.9999999999999996, 3.9999999999999996) 
- *iterations:*     1

Function g(x) has 2 significant minima, but outside of them, on the X1-X2 plane, it is very constant (identity), so steps taken far from the extremum will result in small changes, and the *“precision”* condition will be met in 1 step. You can increase *“learning\_rate”*, but we have to face the consequences described above (jumping over the correct solution).

Another interesting initial point is in the vicinity of a local minimum, for example, **(x1 = -2, x2 = 2)**.

![Fig. 7](img/fig_7.jpeg)

*Fig. 7. Local minimum problem in function g(x).*

**RESULTS SUMMARY FOR g(x):**

- *learning\_rate:*   0.01 
- *precision:*   0.001 
- *max\_steps:*   10000 
- *x\_initial:*        (-2, 2) 
- *x\_final:*          (-1.7109787562145413, 0.9918727284019442) 
- *iterations:*     590

Despite performing a large number of iterations, the algorithm provided a local minimum value, due to the decreasing precision of the step between consecutive points in its vicinity.

Conclusions and proposed solutions to the mentioned problems are described in 3. Conclusions.

It is worth noting that in the described algorithm, changes in steps for x1 and x2 are made in parallel (in one loop). In the case of a function with a descent that is roughly the same from each side, this is not a problem. However, this solution would not be applicable to more challenging optimization test functions, e.g., the Rosenbrock banana function, which has narrow strips of local minima.

![Fig. 8](img/fig_8.png)

*Fig. 8. Source of the graph: A. Eilmes, Numerical Methods in Chemistry.*

This means that starting from the point (x = 1.5, y = 2.5), the algorithm should first modify the y values, staying in a narrow range *0.5 < x < 1.5*. As it approaches the global minimum, leave the y values in the range *0 < y < 0.5* and take larger steps for x.

## **3. CONCLUSIONS**

There is no unequivocal solution to the above problems with parameter selection. As seen, changing their values (*learning\_rate, precision, max\_steps*) is still random attempts with low chances of success. A much more optimal solution would be to run the algorithm for several different initial points and statistically determine the best one (e.g., average, median). Most search algorithms operate in random mode, but it happens that before optimization, we have so-called "expert knowledge." In such cases, research should be focused on the suggested area.

Regardless of the initial method, after finding the best point, the search in its vicinity can be further narrowed down significantly by reducing *“learning\_rate”* and *“precision”*, depending on how accurate a solution is desired (usually differences in the range of 0.1 – 0.001 are considered optimal).

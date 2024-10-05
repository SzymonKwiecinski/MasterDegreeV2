# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A quantity y is known to depend on another quantity x. A set of corresponding values has been collected for x and y and is presented.
- The \var{k}-th y value takes \var{y_{k}} and the \var{k}-th x value takes \var{x_{k}}.

INPUT FORMAT:

{
    "y": [y_{k} for k = 1,...,K],
    "x": [x_{k} for k = 1,...,K]
}


OBJECTIVE: Fit the ‘best’ straight line y = bx + a where the objective is to minimize the maximum deviation of all the observed values of y from the value predicted by the linear relationship.

OUTPUT INFO:

- \var{intercept} represents the intercept of the fitted line
- \var{slope} represents the slope of the fitted line

OUTPUT FORMAT:

{
    "intercept": intercept,
    "slope": slope
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To fit the best straight line \( y = bx + a \) by minimizing the maximum deviation of all the observed values from the linear relationship, we can set up the following linear programming model. 

This approach involves formulating the problem using Chebyshev approximation, which aims to minimize the maximum absolute deviation:

Given:
- A set of data points \((x_k, y_k)\) for \( k = 1, \dots, K \).

Objective:
- Minimize the maximum absolute deviation: \( \min \max |y_k - (bx_k + a)| \) for all \( k \).

We introduce a new variable \( t \) such that:
- \( |y_k - (bx_k + a)| \leq t \) for all \( k \).

The problem then can be expressed as a linear program:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize:} \quad & t \\
\text{Subject to:} \quad & y_k - (bx_k + a) \leq t, \quad \forall k = 1, \dots, K, \\
                        & -(y_k - (bx_k + a)) \leq t, \quad \forall k = 1, \dots, K.
\end{align*}

\textbf{Where:}
\begin{align*}
b & : \text{Slope of the best fit line} \\
a & : \text{Intercept of the best fit line} \\
t & : \text{Maximum absolute deviation, to be minimized}
\end{align*}

\end{document}
```

Solving this linear programming problem will provide the values of \( a \) (intercept) and \( b \) (slope) that best fit the data in terms of minimizing the maximum deviation. The LP solver would give you the specific values for intercept and slope which can be provided in the specified output format:

```json
{
    "intercept": intercept_value,
    "slope": slope_value
}
```

Replace `intercept_value` and `slope_value` with the corresponding results obtained from solving the linear programming model.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize:} \quad & t \\
\text{Subject to:} \quad & y_k - (bx_k + a) \leq t, \quad \forall k = 1, \dots, K, \\
                        & -(y_k - (bx_k + a)) \leq t, \quad \forall k = 1, \dots, K.
\end{align*}

\textbf{Where:}
\begin{align*}
b & : \text{Slope of the best fit line} \\
a & : \text{Intercept of the best fit line} \\
t & : \text{Maximum absolute deviation, to be minimized}
\end{align*}

\end{document}
{
    "intercept": intercept_value,
    "slope": slope_value
}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Model parameters
intercept_value = None
slope_value = None

#### Unpack data
K = data['NumObs']
y = data['Y']
x = data['X']

#### Create a new LP problem
problem = pulp.LpProblem("Minimize_Max_Absolute_Deviation", pulp.LpMinimize)

#### Decision variables
t = pulp.LpVariable('t', lowBound=0, cat='Continuous')  #### Minimize this
b = pulp.LpVariable('b', cat='Continuous')             #### Slope
a = pulp.LpVariable('a', cat='Continuous')             #### Intercept

#### Objective function
problem += t

#### Constraints
for k in range(K):
    problem += y[k] - (b * x[k] + a) <= t
    problem += -(y[k] - (b * x[k] + a)) <= t

#### Solve the problem
problem.solve()

#### Print the value of the objective function
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```



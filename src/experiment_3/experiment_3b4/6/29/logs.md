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
To tackle the problem of fitting the best straight line \( y = bx + a \) such that the maximum deviation of the observed values from the predicted values is minimized, we can employ the method of Linear Programming. This problem is specifically known as the Chebyshev Approximation problem.

The objective is to minimize the maximum absolute deviation of the observed data points from the line. Mathematically, this can be expressed as:

\[
\min_{a, b, e} \quad e
\]

subject to the constraints:

\[
y_k - bx_k - a \leq e, \quad \text{for } k = 1, 2, \ldots, K
\]
\[
bx_k + a - y_k \leq e, \quad \text{for } k = 1, 2, \ldots, K
\]

Here, \( a \) is the intercept of the line, \( b \) is the slope of the line, and \( e \) is the maximum absolute deviation that we aim to minimize.

The following is a latex representation of the mathematical model for this linear programming problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Chebyshev Approximation Linear Programming Formulation}

We want to find the line \( y = bx + a \) that minimizes the maximum deviation from the observed data points \((x_k, y_k)\).

\subsection*{Objective Function}
\[
\min_{a, b, e} \quad e
\]

\subsection*{Constraints}
For each data point \( (x_k, y_k) \), we have the following constraints:
\[
y_k - bx_k - a \leq e, \quad \text{for } k = 1, 2, \ldots, K
\]
\[
bx_k + a - y_k \leq e, \quad \text{for } k = 1, 2, \ldots, K
\]

Here:
- \( a \) is the intercept of the line,
- \( b \) is the slope of the line,
- \( e \) is the maximum absolute deviation that we want to minimize.

\end{document}
```

Once you solve this linear programming problem using a solver, the variables \( a \) and \( b \) will give you the intercept and slope of the line, respectively. The value of \( e \) will be the minimized maximum deviation. The result can be presented in the specified output format as:

```json
{
    "intercept": intercept,
    "slope": slope
}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Chebyshev Approximation Linear Programming Formulation}

We want to find the line \( y = bx + a \) that minimizes the maximum deviation from the observed data points \((x_k, y_k)\).

\subsection*{Objective Function}
\[
\min_{a, b, e} \quad e
\]

\subsection*{Constraints}
For each data point \( (x_k, y_k) \), we have the following constraints:
\[
y_k - bx_k - a \leq e, \quad \text{for } k = 1, 2, \ldots, K
\]
\[
bx_k + a - y_k \leq e, \quad \text{for } k = 1, 2, \ldots, K
\]

Here:
- \( a \) is the intercept of the line,
- \( b \) is the slope of the line,
- \( e \) is the maximum absolute deviation that we want to minimize.

\end{document}
{
    "intercept": intercept,
    "slope": slope
}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Variable initialization
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
e = pulp.LpVariable('e', lowBound=0, cat='Continuous')

#### Problem setup
problem = pulp.LpProblem("Chebyshev_Approximation", pulp.LpMinimize)

#### Objective function
problem += e

#### Constraints
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += y_k - (b * x_k + a) <= e
    problem += b * x_k + a - y_k <= e

#### Solve the problem
problem.solve()

#### Print results
print(f'Objective value: <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


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


OBJECTIVE: Fit the ‘best’ quadratic curve y = c * x^2 + b * x + a to this set of data points. The objective is to minimize the sum of absolute deviations of each observed value of y from the value predicted by the quadratic relationship.

OUTPUT INFO:

- \var{quadratic} represents the coefficient of quadratic term
- \var{linear} represents the coefficient of linear term
- \var{constant} represents the coefficient of constant

OUTPUT FORMAT:

{
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To fit the best quadratic curve \(y = c \cdot x^2 + b \cdot x + a\) to the given set of data points by minimizing the sum of absolute deviations, we can formulate this as a linear programming problem.

Given the set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), the objective is to minimize the sum of absolute deviations:

\[
\sum_{k=1}^K |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

This can be modeled using linear programming by introducing auxiliary variables to represent the absolute deviations. Here is the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we want to find the coefficients \(c\), \(b\), and \(a\) of the quadratic curve \(y = c \cdot x^2 + b \cdot x + a\) that minimizes the sum of absolute deviations.

\[
\text{Minimize: } \sum_{k=1}^K v_k
\]

Subject to:

\[
v_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K
\]

\[
v_k \geq - (y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad k = 1, \ldots, K
\]

Where:
- \(v_k\) is the auxiliary variable representing the absolute deviation for the \(k\)-th observation.

The decision variables are \(c\), \(b\), \(a\), and \(v_k\) for \(k = 1, \ldots, K\).

\end{document}
```

This formulation uses linear constraints to handle the absolute deviations, allowing us to use linear programming techniques to solve for the coefficients \(c\), \(b\), and \(a\) that minimize the sum of these deviations. Solvers like CPLEX, Gurobi, or open-source options like SciPy's `linprog` can then be used to find the optimal solution.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we want to find the coefficients \(c\), \(b\), and \(a\) of the quadratic curve \(y = c \cdot x^2 + b \cdot x + a\) that minimizes the sum of absolute deviations.

\[
\text{Minimize: } \sum_{k=1}^K v_k
\]

Subject to:

\[
v_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K
\]

\[
v_k \geq - (y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad k = 1, \ldots, K
\]

Where:
- \(v_k\) is the auxiliary variable representing the absolute deviation for the \(k\)-th observation.

The decision variables are \(c\), \(b\), \(a\), and \(v_k\) for \(k = 1, \ldots, K\).

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Extract data points
x = data['x']
y = data['y']
K = len(y)

#### Create LP problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Decision variables
c = pulp.LpVariable("c", lowBound=None)  #### Coefficient for x^2
b = pulp.LpVariable("b", lowBound=None)  #### Coefficient for x
a = pulp.LpVariable("a", lowBound=None)  #### Constant term
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(K)]  #### Auxiliary variables for absolute deviations

#### Objective function: minimize sum of v_k
problem += pulp.lpSum(v), "MinimizeAbsoluteDeviations"

#### Constraints
for k in range(K):
    problem += v[k] >= y[k] - (c * (x[k] ** 2) + b * x[k] + a), f"UpperBound_{k}"
    problem += v[k] >= - (y[k] - (c * (x[k] ** 2) + b * x[k] + a)), f"LowerBound_{k}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


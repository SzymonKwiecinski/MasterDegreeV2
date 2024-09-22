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
To solve the problem of fitting the 'best' quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the given set of data points, we can formulate it as a Linear Programming (LP) problem. The objective is to minimize the sum of absolute deviations between the observed values of \( y \) and the values predicted by the quadratic relationship.

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Quadratic Curve Fitting via Linear Programming}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we aim to fit a quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) by minimizing the sum of absolute deviations between observed and predicted values of \( y \).

\subsection*{Objective}

Minimize:
\[
\sum_{k=1}^K |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

\subsection*{Linear Programming Formulation}

Introduce non-negative variables \( u_k \) and \( v_k \) to represent the positive and negative deviations, respectively:

For each data point \( k = 1, \ldots, K \):
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = u_k - v_k
\]
\[ 
u_k, v_k \geq 0
\]

The linear programming objective is to minimize:
\[
\sum_{k=1}^K (u_k + v_k)
\]

Subject to the constraints:
\[
y_k - c \cdot x_k^2 - b \cdot x_k - a = u_k - v_k \quad \forall \, k = 1, \ldots, K
\]
\[
u_k, v_k \geq 0 \quad \forall \, k = 1, \ldots, K
\]

\subsection*{Variables}

- \( c \): Coefficient of the quadratic term.
- \( b \): Coefficient of the linear term.
- \( a \): Constant term.
- \( u_k, v_k \): Non-negative variables representing deviations for each data point \( k \).

\end{document}
```

This LaTeX code outlines the linear programming model used to fit a quadratic curve with the objective of minimizing absolute deviations. Solving this LP will yield the coefficients \( c \), \( b \), and \( a \) for the quadratic curve that best fits the provided data points according to the specified criterion.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Quadratic Curve Fitting via Linear Programming}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we aim to fit a quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) by minimizing the sum of absolute deviations between observed and predicted values of \( y \).

\subsection*{Objective}

Minimize:
\[
\sum_{k=1}^K |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

\subsection*{Linear Programming Formulation}

Introduce non-negative variables \( u_k \) and \( v_k \) to represent the positive and negative deviations, respectively:

For each data point \( k = 1, \ldots, K \):
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = u_k - v_k
\]
\[ 
u_k, v_k \geq 0
\]

The linear programming objective is to minimize:
\[
\sum_{k=1}^K (u_k + v_k)
\]

Subject to the constraints:
\[
y_k - c \cdot x_k^2 - b \cdot x_k - a = u_k - v_k \quad \forall \, k = 1, \ldots, K
\]
\[
u_k, v_k \geq 0 \quad \forall \, k = 1, \ldots, K
\]

\subsection*{Variables}

- \( c \): Coefficient of the quadratic term.
- \( b \): Coefficient of the linear term.
- \( a \): Constant term.
- \( u_k, v_k \): Non-negative variables representing deviations for each data point \( k \).

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Number of data points
K = len(data['x'])

#### Initialize the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Decision variables
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)
u = pulp.LpVariable.dicts('u', range(K), lowBound=0)
v = pulp.LpVariable.dicts('v', range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum([u[k] + v[k] for k in range(K)])

#### Constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += y_k - (c * x_k**2 + b * x_k + a) == u[k] - v[k]

#### Solve the problem
problem.solve()

#### Print the results
print(f'c = {c.varValue}')
print(f'b = {b.varValue}')
print(f'a = {a.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


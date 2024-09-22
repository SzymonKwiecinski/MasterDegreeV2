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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Quadratic Curve Fitting via Linear Programming}

Given a set of data points $(x_k, y_k)$ for $k = 1, \ldots, K$, we aim to fit a quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

where \( c \), \( b \), and \( a \) are the coefficients representing the quadratic, linear, and constant terms respectively.

The objective is to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values \( \hat{y}_k = c x_k^2 + b x_k + a \):

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - \hat{y}_k| = \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

To formulate this as a linear programming problem, we introduce auxiliary variables \( d_k \) to represent the absolute deviations:

\[
d_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]
\[
d_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

Therefore, we can express the optimization problem as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

subject to the constraints:

\[
d_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]

\[
d_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

This formulation allows us to find the coefficients \( c \), \( b \), and \( a \) that minimize the sum of absolute deviations.

\end{document}
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

\section*{Quadratic Curve Fitting via Linear Programming}

Given a set of data points $(x_k, y_k)$ for $k = 1, \ldots, K$, we aim to fit a quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

where \( c \), \( b \), and \( a \) are the coefficients representing the quadratic, linear, and constant terms respectively.

The objective is to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values \( \hat{y}_k = c x_k^2 + b x_k + a \):

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - \hat{y}_k| = \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

To formulate this as a linear programming problem, we introduce auxiliary variables \( d_k \) to represent the absolute deviations:

\[
d_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]
\[
d_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

Therefore, we can express the optimization problem as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

subject to the constraints:

\[
d_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]

\[
d_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

This formulation allows us to find the coefficients \( c \), \( b \), and \( a \) that minimize the sum of absolute deviations.

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
y_values = data['y']
x_values = data['x']
K = len(y_values)

#### Create the LP problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Coefficients
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)

#### Auxiliary variables for absolute deviations
d = [pulp.LpVariable(f'd_{k}', lowBound=0) for k in range(K)]

#### Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(d)

#### Constraints for deviations
for k in range(K):
    predicted = c * (x_values[k] ** 2) + b * x_values[k] + a
    problem += d[k] >= y_values[k] - predicted
    problem += d[k] >= -(y_values[k] - predicted)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


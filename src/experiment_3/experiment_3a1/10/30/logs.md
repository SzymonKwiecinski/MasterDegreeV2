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

\title{Quadratic Curve Fitting using Linear Programming}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Given a set of data points $(x_k, y_k)$ for $k = 1, 2, \ldots, K$, we want to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

where \(c\), \(b\), and \(a\) are the coefficients we need to determine. The objective is to minimize the sum of absolute deviations between the observed values \(y_k\) and the predicted values \(\hat{y}_k = c \cdot x_k^2 + b \cdot x_k + a\).

\section*{Mathematical Formulation}

We introduce the variables:

\[
d_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]

for each observation \(k\). The absolute deviation can be expressed using non-negative slack variables \(u_k\) and \(v_k\):

\[
d_k = u_k - v_k
\]

with the constraints:

\[
\begin{align*}
u_k - v_k &= y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K \\
u_k, v_k &\geq 0
\end{align*}
\]

Our goal is to minimize the sum of absolute deviations:

\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

\section*{Linear Programming Formulation}

The linear programming formulation of our problem can be expressed as:

\[
\begin{align*}
\text{minimize} \quad & \sum_{k=1}^{K} (u_k + v_k) \\
\text{subject to} \quad & u_k - v_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K \\
& u_k, v_k \geq 0 \\
& c, b, a \text{ are real numbers}
\end{align*}
\]

\section*{Output Format}

The output of the optimization yields the coefficients:

\[
\begin{align*}
\text{quadratic} & : c \\
\text{linear} & : b \\
\text{constant} & : a
\end{align*}
\]

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

\title{Quadratic Curve Fitting using Linear Programming}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Given a set of data points $(x_k, y_k)$ for $k = 1, 2, \ldots, K$, we want to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

where \(c\), \(b\), and \(a\) are the coefficients we need to determine. The objective is to minimize the sum of absolute deviations between the observed values \(y_k\) and the predicted values \(\hat{y}_k = c \cdot x_k^2 + b \cdot x_k + a\).

\section*{Mathematical Formulation}

We introduce the variables:

\[
d_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]

for each observation \(k\). The absolute deviation can be expressed using non-negative slack variables \(u_k\) and \(v_k\):

\[
d_k = u_k - v_k
\]

with the constraints:

\[
\begin{align*}
u_k - v_k &= y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K \\
u_k, v_k &\geq 0
\end{align*}
\]

Our goal is to minimize the sum of absolute deviations:

\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

\section*{Linear Programming Formulation}

The linear programming formulation of our problem can be expressed as:

\[
\begin{align*}
\text{minimize} \quad & \sum_{k=1}^{K} (u_k + v_k) \\
\text{subject to} \quad & u_k - v_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K \\
& u_k, v_k \geq 0 \\
& c, b, a \text{ are real numbers}
\end{align*}
\]

\section*{Output Format}

The output of the optimization yields the coefficients:

\[
\begin{align*}
\text{quadratic} & : c \\
\text{linear} & : b \\
\text{constant} & : a
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')
y_values = data['y']
x_values = data['x']
K = len(y_values)

#### Create the LP problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Define variables
c = pulp.LpVariable("c", cat='Continuous')
b = pulp.LpVariable("b", cat='Continuous')
a = pulp.LpVariable("a", cat='Continuous')

#### Slack variables for absolute deviations
u = [pulp.LpVariable(f"u_{k}", lowBound=0) for k in range(K)]
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(u[k] + v[k] for k in range(K))

#### Constraints
for k in range(K):
    problem += u[k] - v[k] == y_values[k] - (c * x_values[k] ** 2 + b * x_values[k] + a)

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Quadratic coefficient (c): {pulp.value(c)}')
print(f'Linear coefficient (b): {pulp.value(b)}')
print(f'Constant term (a): {pulp.value(a)}')
```


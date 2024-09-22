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

\section*{Quadratic Curve Fitting Using Linear Programming}

Let us define the problem mathematically. We are given a set of values for \( y \) and \( x \) such that:

\[
y = [y_1, y_2, \ldots, y_K]
\]
\[
x = [x_1, x_2, \ldots, x_K]
\]

We aim to fit a quadratic equation of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

Where \( c \), \( b \), and \( a \) are the coefficients we want to determine.

To achieve the best fit, we will minimize the sum of absolute deviations of observed values of \( y \) from the predicted values given by the quadratic equation. The absolute deviation for each observation can be expressed as:

\[
d_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Our objective is to minimize:

\[
\sum_{k=1}^{K} d_k
\]

To convert this into a linear programming format, we introduce auxiliary variables \( z_k \) for each \( k \):

\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a))
\]

This leads to the following linear programming formulation:

\textbf{Objective Function:}
\[
\text{Minimize} \quad \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}
\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, 2, \ldots, K
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad k = 1, 2, \ldots, K
\]

The solution of this linear programming problem will provide us with the coefficients \( c \), \( b \), and \( a \) which represent:

\[
\text{Output:} \quad
\begin{align*}
\text{quadratic} & = c \\
\text{linear} & = b \\
\text{constant} & = a
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

\section*{Quadratic Curve Fitting Using Linear Programming}

Let us define the problem mathematically. We are given a set of values for \( y \) and \( x \) such that:

\[
y = [y_1, y_2, \ldots, y_K]
\]
\[
x = [x_1, x_2, \ldots, x_K]
\]

We aim to fit a quadratic equation of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

Where \( c \), \( b \), and \( a \) are the coefficients we want to determine.

To achieve the best fit, we will minimize the sum of absolute deviations of observed values of \( y \) from the predicted values given by the quadratic equation. The absolute deviation for each observation can be expressed as:

\[
d_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Our objective is to minimize:

\[
\sum_{k=1}^{K} d_k
\]

To convert this into a linear programming format, we introduce auxiliary variables \( z_k \) for each \( k \):

\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a))
\]

This leads to the following linear programming formulation:

\textbf{Objective Function:}
\[
\text{Minimize} \quad \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}
\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, 2, \ldots, K
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad k = 1, 2, \ldots, K
\]

The solution of this linear programming problem will provide us with the coefficients \( c \), \( b \), and \( a \) which represent:

\[
\text{Output:} \quad
\begin{align*}
\text{quadratic} & = c \\
\text{linear} & = b \\
\text{constant} & = a
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
data_json = "{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}"
data = json.loads(data_json.replace("'", "\""))

y = data['y']
x = data['x']
K = len(y)

#### Problem definition
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Variables
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)
z = pulp.LpVariable.dicts("z", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum(z[k] for k in range(K))

#### Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Coefficients: c={c.varValue}, b={b.varValue}, a={a.varValue}')
```


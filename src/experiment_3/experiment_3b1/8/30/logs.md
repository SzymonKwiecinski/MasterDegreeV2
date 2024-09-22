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

\section*{Quadratic Curve Fitting Problem}

Given a set of $K$ observed values of $x$ and $y$, where the $k$-th observed value of $y$ is denoted as $y_k$ corresponding to the $k$-th observed value of $x$ denoted as $x_k$, the objective is to fit the best quadratic curve defined by the equation:

\[
y = c x^2 + b x + a
\]

where $c$, $b$, and $a$ are the coefficients we aim to determine.

The goal is to minimize the sum of absolute deviations of the observed values of $y$ from the predicted values given by the quadratic relationship. This can be formulated as:

\[
\text{minimize} \quad \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

We introduce auxiliary variables $u_k$ for the absolute deviations, leading to the transformation:

\[
u_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]
\[
u_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

This provides the linearization needed for our linear programming formulation. Consequently, the complete linear programming model can be expressed as follows:

\[
\text{minimize} \quad \sum_{k=1}^{K} u_k
\]

subject to:

\[
u_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]
\[
u_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

where $u_k$ are the auxiliary variables representing the absolute deviations.

The solution to this linear programming problem will yield the optimal values of the coefficients:

\begin{itemize}
    \item quadratic term coefficient: $c$
    \item linear term coefficient: $b$
    \item constant term coefficient: $a$
\end{itemize}

The final output will be structured as:

\[
\{ "quadratic": c, "linear": b, "constant": a \}
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

\section*{Quadratic Curve Fitting Problem}

Given a set of $K$ observed values of $x$ and $y$, where the $k$-th observed value of $y$ is denoted as $y_k$ corresponding to the $k$-th observed value of $x$ denoted as $x_k$, the objective is to fit the best quadratic curve defined by the equation:

\[
y = c x^2 + b x + a
\]

where $c$, $b$, and $a$ are the coefficients we aim to determine.

The goal is to minimize the sum of absolute deviations of the observed values of $y$ from the predicted values given by the quadratic relationship. This can be formulated as:

\[
\text{minimize} \quad \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

We introduce auxiliary variables $u_k$ for the absolute deviations, leading to the transformation:

\[
u_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]
\[
u_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

This provides the linearization needed for our linear programming formulation. Consequently, the complete linear programming model can be expressed as follows:

\[
\text{minimize} \quad \sum_{k=1}^{K} u_k
\]

subject to:

\[
u_k \geq y_k - (c x_k^2 + b x_k + a) \quad \forall k
\]
\[
u_k \geq -(y_k - (c x_k^2 + b x_k + a)) \quad \forall k
\]

where $u_k$ are the auxiliary variables representing the absolute deviations.

The solution to this linear programming problem will yield the optimal values of the coefficients:

\begin{itemize}
    \item quadratic term coefficient: $c$
    \item linear term coefficient: $b$
    \item constant term coefficient: $a$
\end{itemize}

The final output will be structured as:

\[
\{ "quadratic": c, "linear": b, "constant": a \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import numpy as np

#### Data in the provided format
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Number of data points
K = len(data['y'])

#### Create the problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Coefficients
c = pulp.LpVariable('c', lowBound=None)  #### quadratic term coefficient
b = pulp.LpVariable('b', lowBound=None)  #### linear term coefficient
a = pulp.LpVariable('a', lowBound=None)  #### constant term coefficient

#### Auxiliary variables for absolute deviations
u = [pulp.LpVariable(f'u_{k}', lowBound=0) for k in range(K)]

#### Objective function: minimize the sum of auxiliary variables
problem += pulp.lpSum(u), "Minimize_Absolute_Deviation"

#### Constraints for absolute deviations
for k in range(K):
    problem += u[k] >= data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a), f"Upper_Bound_{k}"
    problem += u[k] >= -(data['y'][k] - (c * (data['x'][k] ** 2) + b * data['x'][k] + a)), f"Lower_Bound_{k}"

#### Solve the problem
problem.solve()

#### Output the results
results = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(results)
```


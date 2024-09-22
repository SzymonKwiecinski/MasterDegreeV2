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
To fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the given data, minimizing the sum of absolute deviations, we can formulate the problem as a Linear Programming problem. This involves minimizing the absolute deviations between the observed and predicted values of \( y \).

Given the data points \((x_k, y_k)\), for \(k = 1, \ldots, K\), we aim to find coefficients \(a\), \(b\), and \(c\) that minimize:

\[
\min \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

This is a linear programming problem because the absolute deviations can be linearized using auxiliary variables. Here's the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} e_k
\]

where \( e_k \) represents the absolute deviation for each data point.

\textbf{Subject to:}

For each data point \( k \), introduce constraints to linearize the absolute value:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq e_k
\]

\[
(c \cdot x_k^2 + b \cdot x_k + a) - y_k \leq e_k
\]

These constraints ensure that \( e_k \) is at least as large as the positive or negative deviation from the predicted value.

\textbf{Variables:}

- \( a \): constant term
- \( b \): linear term
- \( c \): quadratic term
- \( e_k \): absolute deviation for each data point \( k \)

\textbf{Solution:}

The solution will provide the coefficients for the quadratic function, which are:

- Quadratic coefficient (\(c\))
- Linear coefficient (\(b\))
- Constant coefficient (\(a\))

\end{document}
```

The above formulation sets up a linear program to minimize the sum of absolute deviations between the observed \( y_k \) values and those predicted by the quadratic relationship \( c \cdot x_k^2 + b \cdot x_k + a \). The auxiliary variables \( e_k \) help in handling the absolute value operation linearly.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} e_k
\]

where \( e_k \) represents the absolute deviation for each data point.

\textbf{Subject to:}

For each data point \( k \), introduce constraints to linearize the absolute value:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq e_k
\]

\[
(c \cdot x_k^2 + b \cdot x_k + a) - y_k \leq e_k
\]

These constraints ensure that \( e_k \) is at least as large as the positive or negative deviation from the predicted value.

\textbf{Variables:}

- \( a \): constant term
- \( b \): linear term
- \( c \): quadratic term
- \( e_k \): absolute deviation for each data point \( k \)

\textbf{Solution:}

The solution will provide the coefficients for the quadratic function, which are:

- Quadratic coefficient (\(c\))
- Linear coefficient (\(b\))
- Constant coefficient (\(a\))

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

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
c = pulp.LpVariable('c', cat='Continuous')
e = pulp.LpVariable.dicts('e', range(len(data['x'])), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(e)

#### Constraints
for k in range(len(data['x'])):
    x_k = data['x'][k]
    y_k = data['y'][k]
    #### Linearize absolute deviations
    problem += y_k - (c * x_k ** 2 + b * x_k + a) <= e[k]
    problem += (c * x_k ** 2 + b * x_k + a) - y_k <= e[k]

#### Solve the problem
problem.solve()

#### Print the results
print(f"(a, b, c): ({pulp.value(a)}, {pulp.value(b)}, {pulp.value(c)})")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


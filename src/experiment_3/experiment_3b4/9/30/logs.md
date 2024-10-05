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
To solve this problem, we aim to fit a quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the given data set by minimizing the sum of the absolute deviations between the observed values \( y_k \) and the values predicted by the quadratic model. This is done using Linear Programming (or a similar optimization method) which can handle absolute value minimization directly.

Here's the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Quadratic Curve Fitting using Linear Programming}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), our goal is to determine the coefficients \(c\), \(b\), and \(a\) of the quadratic function:

\[
y = c \cdot x^2 + b \cdot x + a
\]

We aim to minimize the sum of the absolute deviations \(|y_k - (c \cdot x_k^2 + b \cdot x_k + a)|\) for all \(k\).

\subsection*{Linear Programming Model}

Define \(e_k\) as the absolute deviation for each data point:

\[
e_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Since absolute values can be linearized using auxiliary variables, we introduce two non-negative variables \(e_k^+\) and \(e_k^-\) such that:

\[
e_k = e_k^+ + e_k^-
\]

with constraints:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-
\]

\[
e_k^+, e_k^- \geq 0
\]

The objective is to minimize the total deviation:

\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

Subject to the constraints:

- For each \(k = 1, \ldots, K\):

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-
\]

\[
e_k^+, e_k^- \geq 0
\]

By solving this linear programming problem, we obtain the coefficients \(c\), \(b\), and \(a\).

\end{document}
```

This model uses the concept of breaking down absolute values into linear expressions with the help of auxiliary variables, which can be effectively solved using linear programming tools.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Quadratic Curve Fitting using Linear Programming}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), our goal is to determine the coefficients \(c\), \(b\), and \(a\) of the quadratic function:

\[
y = c \cdot x^2 + b \cdot x + a
\]

We aim to minimize the sum of the absolute deviations \(|y_k - (c \cdot x_k^2 + b \cdot x_k + a)|\) for all \(k\).

\subsection*{Linear Programming Model}

Define \(e_k\) as the absolute deviation for each data point:

\[
e_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Since absolute values can be linearized using auxiliary variables, we introduce two non-negative variables \(e_k^+\) and \(e_k^-\) such that:

\[
e_k = e_k^+ + e_k^-
\]

with constraints:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-
\]

\[
e_k^+, e_k^- \geq 0
\]

The objective is to minimize the total deviation:

\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

Subject to the constraints:

- For each \(k = 1, \ldots, K\):

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-
\]

\[
e_k^+, e_k^- \geq 0
\]

By solving this linear programming problem, we obtain the coefficients \(c\), \(b\), and \(a\).

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

x_values = data['x']
y_values = data['y']
n = len(x_values)

#### Define problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Decision variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')

#### Auxiliary variables for absolute deviations
e_plus = pulp.LpVariable.dicts('e_plus', range(n), lowBound=0, cat='Continuous')
e_minus = pulp.LpVariable.dicts('e_minus', range(n), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(e_plus[k] + e_minus[k] for k in range(n))

#### Constraints
for k in range(n):
    x_k = x_values[k]
    y_k = y_values[k]
    problem += y_k - (c * x_k**2 + b * x_k + a) == e_plus[k] - e_minus[k]
    problem += e_plus[k] >= 0
    problem += e_minus[k] >= 0

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


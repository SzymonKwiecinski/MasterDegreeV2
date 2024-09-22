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

Given a set of observed values $y_k$ and corresponding values $x_k$ for $k = 1, \ldots, K$, we aim to fit a quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

to minimize the sum of absolute deviations defined as:

\[
\text{minimize} \quad \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

To model this as a linear programming problem, we introduce auxiliary variables for the absolute deviations:

\[
d_k = |y_k - (c x_k^2 + b x_k + a)| \quad \text{for } k = 1, \ldots, K
\]

The objective can then be rewritten as minimizing the sum of these deviations:

\[
\text{minimize} \quad \sum_{k=1}^{K} d_k
\]

Subject to the constraints:

\[
y_k - (c x_k^2 + b x_k + a) \leq d_k \quad \text{for } k = 1, \ldots, K
\]
\[
-(y_k - (c x_k^2 + b x_k + a)) \leq d_k \quad \text{for } k = 1, \ldots, K
\]

Thus, the linear programming formulation consists of:

\begin{align*}
\text{Variables:} & \quad c, b, a, d_k \quad \text{for } k = 1, \ldots, K \\
\text{Objective:} & \quad \text{minimize } \sum_{k=1}^{K} d_k \\
\text{Subject to:} & \quad y_k - (c x_k^2 + b x_k + a) \leq d_k \quad \forall k \\
& \quad -(y_k - (c x_k^2 + b x_k + a)) \leq d_k \quad \forall k \\
\end{align*}

The optimal solution will yield the coefficients:

\begin{align*}
\text{quadratic} & = c \\
\text{linear} & = b \\
\text{constant} & = a \\
\end{align*}

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

Given a set of observed values $y_k$ and corresponding values $x_k$ for $k = 1, \ldots, K$, we aim to fit a quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

to minimize the sum of absolute deviations defined as:

\[
\text{minimize} \quad \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

To model this as a linear programming problem, we introduce auxiliary variables for the absolute deviations:

\[
d_k = |y_k - (c x_k^2 + b x_k + a)| \quad \text{for } k = 1, \ldots, K
\]

The objective can then be rewritten as minimizing the sum of these deviations:

\[
\text{minimize} \quad \sum_{k=1}^{K} d_k
\]

Subject to the constraints:

\[
y_k - (c x_k^2 + b x_k + a) \leq d_k \quad \text{for } k = 1, \ldots, K
\]
\[
-(y_k - (c x_k^2 + b x_k + a)) \leq d_k \quad \text{for } k = 1, \ldots, K
\]

Thus, the linear programming formulation consists of:

\begin{align*}
\text{Variables:} & \quad c, b, a, d_k \quad \text{for } k = 1, \ldots, K \\
\text{Objective:} & \quad \text{minimize } \sum_{k=1}^{K} d_k \\
\text{Subject to:} & \quad y_k - (c x_k^2 + b x_k + a) \leq d_k \quad \forall k \\
& \quad -(y_k - (c x_k^2 + b x_k + a)) \leq d_k \quad \forall k \\
\end{align*}

The optimal solution will yield the coefficients:

\begin{align*}
\text{quadratic} & = c \\
\text{linear} & = b \\
\text{constant} & = a \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract x and y from data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
y_data = data['y']
x_data = data['x']
K = len(y_data)

#### Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Define variables for coefficients and deviations
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Define objective function to minimize the sum of deviations
problem += pulp.lpSum(d)

#### Add constraints for absolute deviations
for k in range(K):
    x_k = x_data[k]
    y_k = y_data[k]
    #### Add constraints for each k
    problem += y_k - (c * x_k**2 + b * x_k + a) <= d[k]
    problem += -(y_k - (c * x_k**2 + b * x_k + a)) <= d[k]

#### Solve the problem
problem.solve()

#### Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'c (quadratic coefficient): {pulp.value(c)}')
print(f'b (linear coefficient): {pulp.value(b)}')
print(f'a (constant term): {pulp.value(a)}')
```



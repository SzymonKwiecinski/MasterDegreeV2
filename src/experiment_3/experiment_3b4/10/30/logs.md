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
To formulate this problem as a Linear Programming (LP) model, we want to fit a quadratic curve of the form \( y = c \cdot x^2 + b \cdot x + a \) to a given set of data points \((x_k, y_k)\) by minimizing the sum of absolute deviations between the observed \( y_k \) and the predicted \( y_k \) values.

The provided problem requires minimizing the sum of absolute differences:

\[
\min \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

To handle the absolute values in the objective function, we introduce auxiliary variables \( z_k \) for each data point to replace the absolute values, transforming the objective into a linear form:

\[
\min \sum_{k=1}^{K} z_k
\]

subject to the constraints:

\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]
\[
z_k \geq -\left( y_k - (c \cdot x_k^2 + b \cdot x_k + a) \right)
\]

for all \( k = 1, 2, \ldots, K \).

Here's the complete LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\begin{align*}
\text{Minimize:} \quad & \sum_{k=1}^{K} z_k \\
\text{Subject to:} \quad & z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad \forall k = 1, 2, \ldots, K \\
& z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad \forall k = 1, 2, \ldots, K \\
& \text{where } z_k \geq 0, \quad \forall k = 1, 2, \ldots, K.
\end{align*}

\text{Variables:}
- $c$: the coefficient of the quadratic term.
- $b$: the coefficient of the linear term.
- $a$: the coefficient of the constant term.
- $z_k$: auxiliary variables for each data point $k$.

\end{document}
```

This LP model will provide the coefficients \( c \), \( b \), and \( a \) for the best-fitting quadratic curve based on minimizing the sum of absolute deviations from the observed data points.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\begin{align*}
\text{Minimize:} \quad & \sum_{k=1}^{K} z_k \\
\text{Subject to:} \quad & z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad \forall k = 1, 2, \ldots, K \\
& z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad \forall k = 1, 2, \ldots, K \\
& \text{where } z_k \geq 0, \quad \forall k = 1, 2, \ldots, K.
\end{align*}

\text{Variables:}
- $c$: the coefficient of the quadratic term.
- $b$: the coefficient of the linear term.
- $a$: the coefficient of the constant term.
- $z_k$: auxiliary variables for each data point $k$.

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
K = len(data['y'])

#### Problem
problem = pulp.LpProblem("Quadratic_Fitting", pulp.LpMinimize)

#### Variables
c = pulp.LpVariable('c', lowBound=-1000, upBound=1000, cat='Continuous')
b = pulp.LpVariable('b', lowBound=-1000, upBound=1000, cat='Continuous')
a = pulp.LpVariable('a', lowBound=-1000, upBound=1000, cat='Continuous')
z = [pulp.LpVariable(f'z_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective
problem += pulp.lpSum(z)

#### Constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += z[k] >= y_k - (c * x_k**2 + b * x_k + a)
    problem += z[k] >= -(y_k - (c * x_k**2 + b * x_k + a))

#### Solve
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


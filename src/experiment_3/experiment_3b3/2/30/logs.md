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

Given a set of observed values \( y_k \) and corresponding values \( x_k \) for \( k = 1, \ldots, K \), where:

\[
y = [y_1, y_2, \ldots, y_K]
\]
\[
x = [x_1, x_2, \ldots, x_K]
\]

We aim to fit the best quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

The objective is to minimize the sum of absolute deviations of each observed value of \( y \) from the value predicted by the quadratic relationship, which can be formulated as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

To accomplish our goal, we define the decision variables:

- \( c \): coefficient of the quadratic term
- \( b \): coefficient of the linear term
- \( a \): coefficient of the constant term

Thus, our optimization problem can be summarized as follows:

\[
\begin{align*}
\text{Minimize} & \quad \sum_{k=1}^{K} d_k \\
\text{subject to} & \\
d_k & \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K \\
d_k & \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad k = 1, \ldots, K \\
& \text{where } d_k \geq 0 \text{ for all } k
\end{align*}
\]

The final output will include the coefficients:

\[
\text{Output:} \quad \{ \text{"quadratic"}: c, \text{"linear"}: b, \text{"constant"}: a \}
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

Given a set of observed values \( y_k \) and corresponding values \( x_k \) for \( k = 1, \ldots, K \), where:

\[
y = [y_1, y_2, \ldots, y_K]
\]
\[
x = [x_1, x_2, \ldots, x_K]
\]

We aim to fit the best quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

The objective is to minimize the sum of absolute deviations of each observed value of \( y \) from the value predicted by the quadratic relationship, which can be formulated as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

To accomplish our goal, we define the decision variables:

- \( c \): coefficient of the quadratic term
- \( b \): coefficient of the linear term
- \( a \): coefficient of the constant term

Thus, our optimization problem can be summarized as follows:

\[
\begin{align*}
\text{Minimize} & \quad \sum_{k=1}^{K} d_k \\
\text{subject to} & \\
d_k & \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, \ldots, K \\
d_k & \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad k = 1, \ldots, K \\
& \text{where } d_k \geq 0 \text{ for all } k
\end{align*}
\]

The final output will include the coefficients:

\[
\text{Output:} \quad \{ \text{"quadratic"}: c, \text{"linear"}: b, \text{"constant"}: a \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

y = data['y']
x = data['x']
K = len(y)

#### Define the problem
problem = pulp.LpProblem('QuadraticCurveFitting', pulp.LpMinimize)

#### Define decision variables
c = pulp.LpVariable('c', lowBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(d)

#### Constraints
for k in range(K):
    predicted = c * (x[k] ** 2) + b * x[k] + a
    problem += d[k] >= y[k] - predicted
    problem += d[k] >= -(y[k] - predicted)

#### Solve the problem
problem.solve()

#### Collect results
quadratic_coefficient = pulp.value(c)
linear_coefficient = pulp.value(b)
constant_coefficient = pulp.value(a)

#### Output results
output = {
    "quadratic": quadratic_coefficient,
    "linear": linear_coefficient,
    "constant": constant_coefficient
}

#### Objective value
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


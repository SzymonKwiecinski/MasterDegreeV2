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

\section*{Quadratic Curve Fitting using Linear Programming}

Given a set of corresponding values for \(y\) and \(x\) where

\[
y = [y_{k} \text{ for } k = 1,...,K]
\]

\[
x = [x_{k} \text{ for } k = 1,...,K]
\]

our objective is to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

by minimizing the sum of absolute deviations between the observed values of \(y\) and those predicted by the model.

\subsection*{Mathematical Model}

Let \( y_k \) be the observed value at \( x_k \). We need to define our decision variables and constraints as follows:

\begin{align*}
\text{Minimize } & \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)| \\
\text{subject to } & \\
& z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \quad \text{for } k = 1, \ldots, K \\
& z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \quad \text{for } k = 1, \ldots, K \\
& z_k \geq 0 \quad \text{for } k = 1, \ldots, K
\end{align*}

where \( z_k \) represents the absolute deviation for each \( k \).

The linear programming formulation will yield the optimal coefficients \(c\), \(b\), and \(a\) that minimize the sum of the absolute deviations \( \sum_{k=1}^{K} z_k \).

\subsection*{Output Format}

The output will provide the optimal coefficients in the following format:

\[
\{
    \text{"quadratic"}: c,
    \text{"linear"}: b,
    \text{"constant"}: a
\}
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

\section*{Quadratic Curve Fitting using Linear Programming}

Given a set of corresponding values for \(y\) and \(x\) where

\[
y = [y_{k} \text{ for } k = 1,...,K]
\]

\[
x = [x_{k} \text{ for } k = 1,...,K]
\]

our objective is to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

by minimizing the sum of absolute deviations between the observed values of \(y\) and those predicted by the model.

\subsection*{Mathematical Model}

Let \( y_k \) be the observed value at \( x_k \). We need to define our decision variables and constraints as follows:

\begin{align*}
\text{Minimize } & \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)| \\
\text{subject to } & \\
& z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \quad \text{for } k = 1, \ldots, K \\
& z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \quad \text{for } k = 1, \ldots, K \\
& z_k \geq 0 \quad \text{for } k = 1, \ldots, K
\end{align*}

where \( z_k \) represents the absolute deviation for each \( k \).

The linear programming formulation will yield the optimal coefficients \(c\), \(b\), and \(a\) that minimize the sum of the absolute deviations \( \sum_{k=1}^{K} z_k \).

\subsection*{Output Format}

The output will provide the optimal coefficients in the following format:

\[
\{
    \text{"quadratic"}: c,
    \text{"linear"}: b,
    \text{"constant"}: a
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

y = data['y']
x = data['x']
K = len(y)

#### Create a linear programming problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Decision variables
c = pulp.LpVariable("c", lowBound=None)  #### Coefficient for x^2
b = pulp.LpVariable("b", lowBound=None)  #### Coefficient for x
a = pulp.LpVariable("a", lowBound=None)  #### Constant term
z = [pulp.LpVariable(f"z_{k}", lowBound=0) for k in range(K)]  #### Absolute deviations

#### Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(z)

#### Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

#### Solve the problem
problem.solve()

#### Output the results
result = {
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


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

Given a set of observed values for \( y \) and corresponding values for \( x \):

\[
y = [y_{k} \text{ for } k = 1,\ldots,K], \quad x = [x_{k} \text{ for } k = 1,\ldots,K]
\]

We want to fit the best quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

The objective is to minimize the sum of absolute deviations of each observed value of \( y \) from the value predicted by the quadratic relationship. This can be mathematically formulated as:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} |y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a)|
\]

\section*{Mathematical Model}

To handle the absolute value, we introduce auxiliary variables \( d_{k} \) for each \( k \) such that:

\[
d_{k} \geq y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a)
\]
\[
d_{k} \geq -(y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a))
\]

Thus, the linear programming formulation becomes:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} d_{k}
\]

Subject to the constraints:

\[
d_{k} \geq y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a), \quad \forall k
\]
\[
d_{k} \geq -(y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a)), \quad \forall k
\]
\[
d_{k} \geq 0, \quad \forall k
\]

\section*{Output}

The output will consist of the coefficients obtained from the optimization:

\[
\text{Output: } \{ 
\text{"quadratic"} : c, 
\text{"linear"} : b, 
\text{"constant"} : a 
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

\title{Quadratic Curve Fitting using Linear Programming}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Given a set of observed values for \( y \) and corresponding values for \( x \):

\[
y = [y_{k} \text{ for } k = 1,\ldots,K], \quad x = [x_{k} \text{ for } k = 1,\ldots,K]
\]

We want to fit the best quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

The objective is to minimize the sum of absolute deviations of each observed value of \( y \) from the value predicted by the quadratic relationship. This can be mathematically formulated as:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} |y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a)|
\]

\section*{Mathematical Model}

To handle the absolute value, we introduce auxiliary variables \( d_{k} \) for each \( k \) such that:

\[
d_{k} \geq y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a)
\]
\[
d_{k} \geq -(y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a))
\]

Thus, the linear programming formulation becomes:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} d_{k}
\]

Subject to the constraints:

\[
d_{k} \geq y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a), \quad \forall k
\]
\[
d_{k} \geq -(y_{k} - (c \cdot x_{k}^2 + b \cdot x_{k} + a)), \quad \forall k
\]
\[
d_{k} \geq 0, \quad \forall k
\]

\section*{Output}

The output will consist of the coefficients obtained from the optimization:

\[
\text{Output: } \{ 
\text{"quadratic"} : c, 
\text{"linear"} : b, 
\text{"constant"} : a 
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

#### Data in JSON format
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Extracting y and x values
y_values = data['y']
x_values = data['x']
K = len(y_values)

#### Create the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Variables for coefficients
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)

#### Auxiliary variables for absolute deviation
d = [pulp.LpVariable(f'd_{k}', lowBound=0) for k in range(K)]

#### Objective function: Minimize the sum of deviations
problem += pulp.lpSum(d)

#### Constraints for the absolute deviation
for k in range(K):
    problem += d[k] >= y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)
    problem += d[k] >= -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a))

#### Solve the problem
problem.solve()

#### Output the coefficients
output = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


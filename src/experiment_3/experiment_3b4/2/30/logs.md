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
To model this problem as a linear programming (LP) model, we need to approximate the given data points \((x_k, y_k)\) with the quadratic curve \(y = c \cdot x^2 + b \cdot x + a\) by minimizing the sum of absolute deviations of the observed values of \(y\) from the predicted values.

This can be formulated as follows:

Let the deviation for each data point be denoted as \(d_k\). We want to minimize the sum of these deviations.

######### LP Model Formulation

Objective:
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

Subject to:
\[
c \cdot x_k^2 + b \cdot x_k + a - y_k \leq d_k, \quad \forall k
\]
\[
c \cdot x_k^2 + b \cdot x_k + a - y_k \geq -d_k, \quad \forall k
\]
\[
d_k \geq 0, \quad \forall k
\]

The above constraints ensure that \(d_k\) are the absolute deviations between the observed and predicted values.

Below is the LP model in \(\LaTeX\):

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

To fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the given data points, we need to formulate the following optimization problem:

\subsection*{Objective Function}
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

\subsection*{Subject to Constraints}
\begin{align*}
& c \cdot x_k^2 + b \cdot x_k + a - y_k \leq d_k, \quad \forall k, \\
& c \cdot x_k^2 + b \cdot x_k + a - y_k \geq -d_k, \quad \forall k, \\
& d_k \geq 0, \quad \forall k.
\end{align*}

\subsection*{Variables}
- \( c \) is the coefficient of the quadratic term.
- \( b \) is the coefficient of the linear term.
- \( a \) is the coefficient of the constant term.
- \( d_k \) are the deviation (absolute differences) for each data point.

\end{document}
```

This model accurately captures the requirement to minimize the sum of absolute deviations when fitting a quadratic curve to the given data points.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

To fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the given data points, we need to formulate the following optimization problem:

\subsection*{Objective Function}
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

\subsection*{Subject to Constraints}
\begin{align*}
& c \cdot x_k^2 + b \cdot x_k + a - y_k \leq d_k, \quad \forall k, \\
& c \cdot x_k^2 + b \cdot x_k + a - y_k \geq -d_k, \quad \forall k, \\
& d_k \geq 0, \quad \forall k.
\end{align*}

\subsection*{Variables}
- \( c \) is the coefficient of the quadratic term.
- \( b \) is the coefficient of the linear term.
- \( a \) is the coefficient of the constant term.
- \( d_k \) are the deviation (absolute differences) for each data point.

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data_json = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 
                   1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
             'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 
                   5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y_data = data_json['y']
x_data = data_json['x']
num_points = len(y_data)

#### Problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(num_points)]

#### Objective Function
problem += pulp.lpSum(d)

#### Constraints
for k in range(num_points):
    problem += c * x_data[k]**2 + b * x_data[k] + a - y_data[k] <= d[k]
    problem += c * x_data[k]**2 + b * x_data[k] + a - y_data[k] >= -d[k]

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


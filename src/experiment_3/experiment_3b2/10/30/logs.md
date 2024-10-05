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
To model the given problem, we will use a linear programming formulation to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values from the quadratic equation \( y = c \cdot x^2 + b \cdot x + a \).

######### Mathematical Model

Let's denote:
- \( y_k \) as the observed value of \( y \) at data point \( k \).
- \( x_k \) as the observed value of \( x \) at data point \( k \).
- \( c \), \( b \), and \( a \) as the coefficients of the quadratic, linear, and constant terms respectively.

The problem can be modeled as follows:

Objective:
Minimize the sum of absolute deviations: \( \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)| \).

To handle the absolute value, we introduce auxiliary variables \( z_k \) which represent the absolute deviation for each data point.

Constraints:
For each data point \( k \), the deviation is represented by two linear inequalities:
1. \( z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \)
2. \( z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \)

The linear programming model in LaTeX format is:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

Objective:
\[
\text{Minimize} \quad \sum_{k=1}^{K} z_k
\]

Subject to:
\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad \forall k = 1, \ldots, K
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad \forall k = 1, \ldots, K
\]

Variables:
- \( c \): quadratic coefficient
- \( b \): linear coefficient
- \( a \): constant coefficient
- \( z_k \geq 0 \): absolute deviation for each data point

\end{document}
```

This model captures the objective of minimizing the total absolute deviation between the observed and predicted values by appropriately adjusting the coefficients \( c \), \( b \), and \( a \).

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

Objective:
\[
\text{Minimize} \quad \sum_{k=1}^{K} z_k
\]

Subject to:
\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad \forall k = 1, \ldots, K
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)), \quad \forall k = 1, \ldots, K
\]

Variables:
- \( c \): quadratic coefficient
- \( b \): linear coefficient
- \( a \): constant coefficient
- \( z_k \geq 0 \): absolute deviation for each data point

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Model data in JSON format
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

#### Parameters
y = data['y']
x = data['x']
K = len(y)
c = 1  #### Assigning some value for the quadratic coefficient
b = 1  #### Assigning some value for the linear coefficient
a = 0  #### Assigning a value for the constant coefficient

#### Create the problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

#### Variables
z = pulp.LpVariable.dicts("z", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(z[k] for k in range(K)), "Minimize Sum of z_k"

#### Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a), f"Constraint_Upper_{k}"
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a)), f"Constraint_Lower_{k}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


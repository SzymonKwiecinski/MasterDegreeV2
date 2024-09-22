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
To fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to a given set of data points by minimizing the sum of absolute deviations, we can formulate the problem as a linear program. The objective is to minimize:

\[ \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)| \]

This can be transformed into a linear programming problem by introducing auxiliary variables \( z_k \) to represent the absolute deviations:

\[ z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \]
\[ z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \]

The linear programming formulation is:

Minimize:

\[ \sum_{k=1}^{K} z_k \]

Subject to:

\[ z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \]
\[ z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \]

for \( k = 1, \ldots, K \).

Here is the corresponding LaTeX code for this linear programming problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Quadratic Curve Fitting}

Given data:

- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

Objective: Fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the data points by minimizing the sum of absolute deviations.

\subsection*{Linear Programming Formulation}

\textbf{Objective:}

Minimize:
\[
\sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}
\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \quad \text{for } k = 1, \ldots, K
\]

\textbf{Variables:}
- \( c \) : Coefficient of the quadratic term
- \( b \) : Coefficient of the linear term
- \( a \) : Constant coefficient
- \( z_k \) : Absolute deviation for each data point \( k \)

\end{document}
```

Ensure to solve this linear programming model using a suitable solver to find the values for \( c \), \( b \), and \( a \) which minimize the objective function. The solution will give you the coefficients for the quadratic curve fitting the given data points optimally in terms of the sum of absolute deviations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Quadratic Curve Fitting}

Given data:

- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

Objective: Fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to the data points by minimizing the sum of absolute deviations.

\subsection*{Linear Programming Formulation}

\textbf{Objective:}

Minimize:
\[
\sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}
\[
z_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
z_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \quad \text{for } k = 1, \ldots, K
\]

\textbf{Variables:}
- \( c \) : Coefficient of the quadratic term
- \( b \) : Coefficient of the linear term
- \( a \) : Constant coefficient
- \( z_k \) : Absolute deviation for each data point \( k \)

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

y = data['y']
x = data['x']
K = len(y)

#### Create the optimization problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Define the decision variables
c = pulp.LpVariable("c", cat="Continuous")
b = pulp.LpVariable("b", cat="Continuous")
a = pulp.LpVariable("a", cat="Continuous")
z = [pulp.LpVariable(f"z_{k}", lowBound=0, cat="Continuous") for k in range(K)]

#### Objective function
problem += pulp.lpSum(z)

#### Constraints
for k in range(K):
    problem += z[k] >= y[k] - (c * x[k]**2 + b * x[k] + a)
    problem += z[k] >= -(y[k] - (c * x[k]**2 + b * x[k] + a))

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


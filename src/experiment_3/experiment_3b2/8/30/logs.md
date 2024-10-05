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
To model this problem as a Linear Programming (LP) problem, we are tasked with fitting a quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) to a set of data points in such a way that it minimizes the sum of absolute deviations between observed and predicted values. This can be expressed as an LP problem by introducing auxiliary variables to handle absolute values.

Here's the LP model:

######### Decision Variables
- \( a \): the constant term of the quadratic equation.
- \( b \): the linear coefficient of the quadratic equation.
- \( c \): the quadratic coefficient.
- \( e_k \) and \( e_k^+ \) for \( k = 1, \ldots, K \): auxiliary variables for each data point to represent the absolute deviation, where \( e_k^+ \) is the positive deviation and \( e_k^-\) is the negative deviation.

######### Objective Function
Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

######### Constraints
For each data point \( k \):
\[
y_k = c \cdot x_k^2 + b \cdot x_k + a + e_k^+ - e_k^-
\]
\[
e_k^+, e_k^- \geq 0
\]

The full LP model in \(\LaTeX\) is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Quadratic Curve Fitting:}

\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} (e_k^+ + e_k^-) \\
\text{Subject to} \quad & y_k = c \cdot x_k^2 + b \cdot x_k + a + e_k^+ - e_k^-, \quad k = 1, \ldots, K \\
& e_k^+ \geq 0, \quad e_k^- \geq 0, \quad k = 1, \ldots, K
\end{align*}

\textbf{Where:}

\begin{itemize}
    \item \( a \) is the constant coefficient.
    \item \( b \) is the linear coefficient.
    \item \( c \) is the quadratic coefficient.
    \item \( e_k^+ \) and \( e_k^- \) are non-negative deviations for each data point \( k \).
\end{itemize}

\end{document}
```

This model provides a systematic way to determine the coefficients \( a \), \( b \), and \( c \) that best fit the given data points by minimizing the sum of absolute deviations. By introducing \( e_k^+ \) and \( e_k^- \), we can handle the absolute value in the deviations, reformulated as a linear problem suitable for LP solvers.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model for Quadratic Curve Fitting:}

\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} (e_k^+ + e_k^-) \\
\text{Subject to} \quad & y_k = c \cdot x_k^2 + b \cdot x_k + a + e_k^+ - e_k^-, \quad k = 1, \ldots, K \\
& e_k^+ \geq 0, \quad e_k^- \geq 0, \quad k = 1, \ldots, K
\end{align*}

\textbf{Where:}

\begin{itemize}
    \item \( a \) is the constant coefficient.
    \item \( b \) is the linear coefficient.
    \item \( c \) is the quadratic coefficient.
    \item \( e_k^+ \) and \( e_k^- \) are non-negative deviations for each data point \( k \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Extracting x and y values
x_values = data['x']
y_values = data['y']
K = len(x_values)

#### Create the problem variable
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Create decision variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
c = pulp.LpVariable("c", lowBound=None)
e_k_plus = [pulp.LpVariable(f"e_{k}_plus", lowBound=0) for k in range(K)]
e_k_minus = [pulp.LpVariable(f"e_{k}_minus", lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(e_k_plus[k] + e_k_minus[k] for k in range(K))

#### Constraints
for k in range(K):
    problem += y_values[k] == c * x_values[k]**2 + b * x_values[k] + a + e_k_plus[k] - e_k_minus[k]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


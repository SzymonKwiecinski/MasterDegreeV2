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


OBJECTIVE: Fit the ‘best’ straight line y = bx + a where the objective is to minimize the maximum deviation of all the observed values of y from the value predicted by the linear relationship.

OUTPUT INFO:

- \var{intercept} represents the intercept of the fitted line
- \var{slope} represents the slope of the fitted line

OUTPUT FORMAT:

{
    "intercept": intercept,
    "slope": slope
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To construct a linear programming model that minimizes the maximum deviation of all observed values of \( y \) from the predicted values based on the linear relationship \( y = bx + a \), we first need to define the objective function and constraints.

The goal is to find the line \( y = bx + a \) that minimizes the maximum absolute difference between the observed \( y_k \) and the predicted \( bx_k + a \) for each data point \( (x_k, y_k) \).

Let's define the variables and formulate the linear programming problem:

Variables:
- \( a \): the intercept of the line
- \( b \): the slope of the line
- \( d \): the maximum deviation to be minimized

Objective:
Minimize \( d \)

Constraints:
For each data point \( (x_k, y_k) \), minimize the deviation between the observed and predicted values:
\[
y_k - (bx_k + a) \leq d
\]
\[
(bx_k + a) - y_k \leq d
\]

These constraints ensure that \( d \) captures the maximum absolute deviation of the observed values from the predicted values. 

Here is the linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Minimize \( d \)

\subsection*{Constraints}
For each \( k = 1, \ldots, K \):
\begin{align*}
y_k - (bx_k + a) & \leq d \\
(bx_k + a) - y_k & \leq d
\end{align*}

\subsection*{Variables}
\begin{itemize}
    \item \( a \): intercept of the line
    \item \( b \): slope of the line
    \item \( d \): maximum deviation to be minimized
\end{itemize}

\end{document}
```

This formulation allows you to solve for the intercept \( a \) and slope \( b \) that yield the "best" line in terms of minimizing the maximum deviation from the observed data. The solution will provide values for \( a \) and \( b \), which should be returned in the following output format:

```json
{
    "intercept": a,
    "slope": b
}
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

\section*{Linear Programming Model}

\subsection*{Objective}
Minimize \( d \)

\subsection*{Constraints}
For each \( k = 1, \ldots, K \):
\begin{align*}
y_k - (bx_k + a) & \leq d \\
(bx_k + a) - y_k & \leq d
\end{align*}

\subsection*{Variables}
\begin{itemize}
    \item \( a \): intercept of the line
    \item \( b \): slope of the line
    \item \( d \): maximum deviation to be minimized
\end{itemize}

\end{document}
{
    "intercept": a,
    "slope": b
}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

#### Problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=-1e3, upBound=1e3)
b = pulp.LpVariable('b', lowBound=-1e3, upBound=1e3)
d = pulp.LpVariable('d', lowBound=0)

#### Objective
problem += d, "Objective"

#### Constraints
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    problem += (y_k - (b * x_k + a)) <= d, f"Constraint_Upper_{k}"
    problem += ((b * x_k + a) - y_k) <= d, f"Constraint_Lower_{k}"

#### Solve
problem.solve()

#### Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


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
To solve this linear programming problem of fitting the best straight line that minimizes the maximum deviation, we can use the concept of minimizing the Chebyshev norm which corresponds to minimizing the maximum absolute deviation. The mathematical model can be formulated as follows:

Given the data:

- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

We want to find the best fit line \( y = a + bx \) such that the maximum deviation \(| y_k - (a + bx_k) |\) for all \( k \) is minimized.

The linear programming formulation is:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Minimize \( z \)

\textbf{Subject to:}

\[
y_k - (a + bx_k) \leq z, \quad \text{for } k = 1, \ldots, K
\]

\[
-(y_k - (a + bx_k)) \leq z, \quad \text{for } k = 1, \ldots, K
\]

Variables:

- \( a \): intercept
- \( b \): slope
- \( z \): maximum absolute deviation, to be minimized

\end{document}
```

This linear program minimizes the variable \( z \), which represents the maximum deviation between the observed \( y \) values and the values predicted by the line \( y = a + bx \). The constraints ensure that \( z \) is at least as large as all such deviations in both directions.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Minimize \( z \)

\textbf{Subject to:}

\[
y_k - (a + bx_k) \leq z, \quad \text{for } k = 1, \ldots, K
\]

\[
-(y_k - (a + bx_k)) \leq z, \quad \text{for } k = 1, \ldots, K
\]

Variables:

- \( a \): intercept
- \( b \): slope
- \( z \): maximum absolute deviation, to be minimized

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Problem definition
problem = pulp.LpProblem("Minimize_Max_Absolute_Deviation", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
z = pulp.LpVariable("z", lowBound=0)

#### Objective Function
problem += z, "Objective"

#### Constraints
for k in range(data['NumObs']):
    problem += (data['Y'][k] - (a + b * data['X'][k])) <= z, f"Constraint_Upper_{k}"
    problem += -(data['Y'][k] - (a + b * data['X'][k])) <= z, f"Constraint_Lower_{k}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


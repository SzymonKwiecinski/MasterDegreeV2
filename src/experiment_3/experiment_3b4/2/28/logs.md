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


OBJECTIVE: Fit the ‘best’ straight line y = bx + a to this set of data points. The objective is to minimise the sum of absolute deviations of each observed value of y from the value predicted by the linear relationship.

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
To solve this problem using linear programming, we will fit a straight line \( y = bx + a \) by minimizing the sum of absolute deviations between the observed values \( y_k \) and the predicted values from the linear model. This is a linear programming problem because it involves minimizing absolute differences, which is a linear function.

Here's how the mathematical model can be formulated:

######### Linear Programming Model

Objective:
Minimize the sum of absolute deviations:

\[
\min \sum_{k=1}^{K} |y_k - (bx_k + a)|
\]

Given that absolute values complicate linear programming, we introduce non-negative auxiliary variables \( u_k \) and \( v_k \) to represent the positive and negative deviations, such that:

\[
y_k - (bx_k + a) = u_k - v_k \quad \text{where} \quad u_k, v_k \geq 0
\]

Then, the objective becomes:

\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

Subject to:

\[
y_k - (bx_k + a) = u_k - v_k, \; \text{for} \; k = 1, \ldots, K
\]

\[
u_k, v_k \geq 0, \; \text{for} \; k = 1, \ldots, K
\]

######### Conversion to LATEX

The corresponding LATEX code for the LP formulation of this problem is:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation for Fitting a Line with Minimum Absolute Deviations:}

\begin{align*}
    & \text{Minimize} \quad \sum_{k=1}^{K} (u_k + v_k) \\
    & \text{Subject to:} \\
    & y_k - (bx_k + a) = u_k - v_k, \quad \text{for } k = 1, \ldots, K \\
    & u_k \geq 0, \quad v_k \geq 0, \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}
```

This formulation will provide the values of \( a \) (intercept) and \( b \) (slope) once the linear program has been solved. These values will give the best fit line minimizing the sum of absolute deviations between the observed and predicted values of \( y \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation for Fitting a Line with Minimum Absolute Deviations:}

\begin{align*}
    & \text{Minimize} \quad \sum_{k=1}^{K} (u_k + v_k) \\
    & \text{Subject to:} \\
    & y_k - (bx_k + a) = u_k - v_k, \quad \text{for } k = 1, \ldots, K \\
    & u_k \geq 0, \quad v_k \geq 0, \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Problem
problem = pulp.LpProblem("Line_Fitting", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
u = [pulp.LpVariable(f"u_{k}", lowBound=0) for k in range(data['K'])]
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(data['K'])]

#### Objective
problem += pulp.lpSum([u[k] + v[k] for k in range(data['K'])])

#### Constraints
for k in range(data['K']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    problem += (y_k - (b * x_k + a) == u[k] - v[k], f"AbsDeviation_{k}")

#### Solve
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


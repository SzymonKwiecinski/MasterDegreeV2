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
To model this problem as a Linear Programming problem in LaTeX, we need to define our objective function and constraints. The objective is to fit the best straight line \( y = bx + a \) such that the maximum deviation of the observed values of \( y \) from the predicted values is minimized.

Let us denote:
- \( K \) as the number of data points.
- \( a \) as the intercept.
- \( b \) as the slope.
- \( y_k \) as the observed \( y \)-value for the \( k\)-th data point.
- \( x_k \) as the \( x \)-value for the \( k\)-th data point.
- \( d_k \) as the deviation for the \( k\)-th data point.

The linear programming model to minimize the maximum deviation can be represented as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize } & D \\
\text{Subject to } & d_k = |y_k - (bx_k + a)|, \quad \forall k = 1, \ldots, K \\
& d_k \leq D, \quad \forall k = 1, \ldots, K \\
& d_k \geq 0, \quad \forall k = 1, \ldots, K \\
& D \geq 0
\end{align*}

The inequality constraints can be split into two linear constraints for each data point:

\begin{align*}
\text{Subject to } & y_k - (bx_k + a) \leq d_k, \quad \forall k = 1, \ldots, K \\
& -(y_k - (bx_k + a)) \leq d_k, \quad \forall k = 1, \ldots, K \\
& d_k \leq D, \quad \forall k = 1, \ldots, K \\
& d_k \geq 0, \quad \forall k = 1, \ldots, K \\
& D \geq 0
\end{align*}

\end{document}
```

This model aims to minimize \( D \), the maximum of deviations \( d_k \), which are the absolute differences between observed and predicted values. The constraints ensure that the deviation for each data point does not exceed \( D \), and that deviations are non-negative.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\begin{align*}
\text{Minimize } & D \\
\text{Subject to } & d_k = |y_k - (bx_k + a)|, \quad \forall k = 1, \ldots, K \\
& d_k \leq D, \quad \forall k = 1, \ldots, K \\
& d_k \geq 0, \quad \forall k = 1, \ldots, K \\
& D \geq 0
\end{align*}

The inequality constraints can be split into two linear constraints for each data point:

\begin{align*}
\text{Subject to } & y_k - (bx_k + a) \leq d_k, \quad \forall k = 1, \ldots, K \\
& -(y_k - (bx_k + a)) \leq d_k, \quad \forall k = 1, \ldots, K \\
& d_k \leq D, \quad \forall k = 1, \ldots, K \\
& d_k \geq 0, \quad \forall k = 1, \ldots, K \\
& D \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Problem
problem = pulp.LpProblem("MinimizeMaxDeviation", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(data['NumObs'])]

#### Objective
problem += D, "Minimize maximum deviation"

#### Constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    
    #### y_k - (b*x_k + a) <= d_k
    problem += y_k - (b*x_k + a) <= d[k], f"Constraint_1_{k}"
    
    #### -(y_k - (b*x_k + a)) <= d_k
    problem += -(y_k - (b*x_k + a)) <= d[k], f"Constraint_2_{k}"
    
    #### d_k <= D
    problem += d[k] <= D, f"MaxDeviationConstraint_{k}"

#### Solve
problem.solve()

#### Print solution
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


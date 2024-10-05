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
To solve this linear programming problem, we aim to fit the best straight line \( y = bx + a \) by minimizing the maximum deviation of all observed values of \( y \) from those predicted by the linear relationship. This can be formulated as a linear programming problem where we introduce an auxiliary variable \( z \) to represent the maximum deviation. The optimization problem can be expressed as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the maximum deviation, \( z \).

\textbf{Constraints:}
For each \( k \) (where \( k = 1, \ldots, K \)):
\begin{align*}
y_k - (bx_k + a) &\leq z \\
(bx_k + a) - y_k &\leq z
\end{align*}

\textbf{Variables:}
\begin{itemize}
    \item \( a \): intercept of the fitted line
    \item \( b \): slope of the fitted line
    \item \( z \): maximum deviation to be minimized
\end{itemize}

The goal is to solve the linear programming problem with the objective:
\[
\min z
\]

subject to the above constraints for each pair \((x_k, y_k)\).

\end{document}
```

This linear programming model incorporates all the necessary constraints and objectives to determine the line \( y = bx + a \) that minimizes the maximum deviation across all observed data points \((x_k, y_k)\).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the maximum deviation, \( z \).

\textbf{Constraints:}
For each \( k \) (where \( k = 1, \ldots, K \)):
\begin{align*}
y_k - (bx_k + a) &\leq z \\
(bx_k + a) - y_k &\leq z
\end{align*}

\textbf{Variables:}
\begin{itemize}
    \item \( a \): intercept of the fitted line
    \item \( b \): slope of the fitted line
    \item \( z \): maximum deviation to be minimized
\end{itemize}

The goal is to solve the linear programming problem with the objective:
\[
\min z
\]

subject to the above constraints for each pair \((x_k, y_k)\).

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
z = pulp.LpVariable("z", lowBound=0)     #### maximum deviation

#### Constraints for each observation
for k in range(data['NumObs']):
    x_k = data['X'][k]
    y_k = data['Y'][k]
    
    #### y_k - (b*x_k + a) <= z
    problem += (y_k - (b * x_k + a) <= z)
    
    #### (b*x_k + a) - y_k <= z
    problem += ((b * x_k + a) - y_k <= z)

#### Objective function
problem += z  #### we want to minimize z

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


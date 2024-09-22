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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Linear Regression}

Given a set of observed values for \( x \) and \( y \):

- Let \( y_k \) be the \( k \)-th observed value of \( y \)
- Let \( x_k \) be the \( k \)-th observed value of \( x \) for \( k = 1, 2, \ldots, K \)

We want to fit the best straight line \( y = bx + a \) such that the maximum deviation of the observed values of \( y \) from the predicted values \( \hat{y_k} = bx_k + a \) is minimized.

\subsection*{Objective Function}

We define the maximum deviation as:

\[
d_k = y_k - (bx_k + a)
\]

Our goal is to minimize the maximum absolute deviation:

\[
\text{Minimize } M
\]

subject to the constraints:

\[
d_k \leq M \quad \forall k
\]
\[
-d_k \leq M \quad \forall k
\]

This leads to the following formulation:

\[
\text{Minimize } M
\]

subject to:

\[
y_k - (bx_k + a) \leq M \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq M \quad \forall k
\]

\subsection*{Linear Programming Formulation}

To summarize, the linear programming model can be expressed as follows:

\begin{align*}
\text{Minimize} & \quad M \\
\text{subject to} & \quad y_k - (bx_k + a) \leq M \quad \forall k \\
& \quad -(y_k - (bx_k + a)) \leq M \quad \forall k \\
& \quad a, b \text{ unrestricted} \\
& \quad M \geq 0
\end{align*}

\subsection*{Output}

The output will be:

\[
\{
\text{"intercept"}: a,
\text{"slope"}: b
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

\section*{Linear Programming Model for Linear Regression}

Given a set of observed values for \( x \) and \( y \):

- Let \( y_k \) be the \( k \)-th observed value of \( y \)
- Let \( x_k \) be the \( k \)-th observed value of \( x \) for \( k = 1, 2, \ldots, K \)

We want to fit the best straight line \( y = bx + a \) such that the maximum deviation of the observed values of \( y \) from the predicted values \( \hat{y_k} = bx_k + a \) is minimized.

\subsection*{Objective Function}

We define the maximum deviation as:

\[
d_k = y_k - (bx_k + a)
\]

Our goal is to minimize the maximum absolute deviation:

\[
\text{Minimize } M
\]

subject to the constraints:

\[
d_k \leq M \quad \forall k
\]
\[
-d_k \leq M \quad \forall k
\]

This leads to the following formulation:

\[
\text{Minimize } M
\]

subject to:

\[
y_k - (bx_k + a) \leq M \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq M \quad \forall k
\]

\subsection*{Linear Programming Formulation}

To summarize, the linear programming model can be expressed as follows:

\begin{align*}
\text{Minimize} & \quad M \\
\text{subject to} & \quad y_k - (bx_k + a) \leq M \quad \forall k \\
& \quad -(y_k - (bx_k + a)) \leq M \quad \forall k \\
& \quad a, b \text{ unrestricted} \\
& \quad M \geq 0
\end{align*}

\subsection*{Output}

The output will be:

\[
\{
\text{"intercept"}: a,
\text{"slope"}: b
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Create the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

#### Variables
M = pulp.LpVariable("M", lowBound=0)  #### M >= 0
a = pulp.LpVariable("a")  #### unrestricted
b = pulp.LpVariable("b")  #### unrestricted

#### Constraints and objective
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    
    problem += (y_k - (b * x_k + a) <= M, f"Constraint_Upper_{k}")
    problem += (-(y_k - (b * x_k + a)) <= M, f"Constraint_Lower_{k}")

#### Objective function
problem += M, "Objective"

#### Solve the problem
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Intercept (a): {pulp.value(a)}')
print(f'Slope (b): {pulp.value(b)}')
```


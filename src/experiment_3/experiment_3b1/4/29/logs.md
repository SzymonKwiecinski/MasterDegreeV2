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

\section*{Linear Programming Model for Line Fitting}

We aim to fit the best straight line of the form \( y = bx + a \) to a set of observed values \( (x_k, y_k) \) for \( k = 1, \ldots, K \). The objective is to minimize the maximum deviation of all observed values from the predicted values.

\subsection*{Variables}
- Let \( a \) be the intercept of the fitted line.
- Let \( b \) be the slope of the fitted line.
- Let \( d_k \) be the deviation for the \( k \)-th observation, defined as:

\[
d_k = y_k - (bx_k + a)
\]

\subsection*{Objective}
We want to minimize the maximum deviation, which can be expressed mathematically as:

\[
\text{Minimize } D
\]

subject to the constraints:

\[
d_k \leq D \quad \forall k
\]
\[
-d_k \leq D \quad \forall k
\]

This leads to the following constraints:

\[
y_k - (bx_k + a) \leq D \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq D \quad \forall k
\]

\subsection*{Linear Programming Formulation}

The complete linear programming problem can be formulated as follows:

\[
\begin{aligned}
& \text{Minimize} && D \\
& \text{Subject to} && y_k - (bx_k + a) \leq D, \quad \forall k \\
& && -(y_k - (bx_k + a)) \leq D, \quad \forall k \\
& && D \geq 0 \\
& && a \text{ and } b \text{ are real numbers.}
\end{aligned}
\]

\subsection*{Output}
The output of the model will provide the estimated values for the intercept and slope of the fitted line:

\begin{itemize}
    \item intercept: \( a \)
    \item slope: \( b \)
\end{itemize}

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

\section*{Linear Programming Model for Line Fitting}

We aim to fit the best straight line of the form \( y = bx + a \) to a set of observed values \( (x_k, y_k) \) for \( k = 1, \ldots, K \). The objective is to minimize the maximum deviation of all observed values from the predicted values.

\subsection*{Variables}
- Let \( a \) be the intercept of the fitted line.
- Let \( b \) be the slope of the fitted line.
- Let \( d_k \) be the deviation for the \( k \)-th observation, defined as:

\[
d_k = y_k - (bx_k + a)
\]

\subsection*{Objective}
We want to minimize the maximum deviation, which can be expressed mathematically as:

\[
\text{Minimize } D
\]

subject to the constraints:

\[
d_k \leq D \quad \forall k
\]
\[
-d_k \leq D \quad \forall k
\]

This leads to the following constraints:

\[
y_k - (bx_k + a) \leq D \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq D \quad \forall k
\]

\subsection*{Linear Programming Formulation}

The complete linear programming problem can be formulated as follows:

\[
\begin{aligned}
& \text{Minimize} && D \\
& \text{Subject to} && y_k - (bx_k + a) \leq D, \quad \forall k \\
& && -(y_k - (bx_k + a)) \leq D, \quad \forall k \\
& && D \geq 0 \\
& && a \text{ and } b \text{ are real numbers.}
\end{aligned}
\]

\subsection*{Output}
The output of the model will provide the estimated values for the intercept and slope of the fitted line:

\begin{itemize}
    \item intercept: \( a \)
    \item slope: \( b \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Create a linear programming problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

#### Define decision variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
D = pulp.LpVariable("D", lowBound=0)     #### maximum deviation

#### Define the constraints
for k in range(data['NumObs']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    problem += y_k - (b * x_k + a) <= D
    problem += -(y_k - (b * x_k + a)) <= D

#### Objective function
problem += D

#### Solve the problem
problem.solve()

#### Print the results
print(f'Intercept (a): {a.varValue}')
print(f'Slope (b): {b.varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Fitting a Line}

Given the data points \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we want to fit the best straight line of the form:
\[
y = bx + a
\]
Our objective is to minimize the sum of absolute deviations of each observed value of \( y \) from the value predicted by the linear relationship. This can be formulated as follows:

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( a \): Intercept of the fitted line
    \item \( b \): Slope of the fitted line
    \item \( d_k \): Absolute deviation for each observation, defined as \( d_k = |y_k - (bx_k + a)| \)
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the sum of the absolute deviations:
\[
\text{Minimize } Z = \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
For each observation \( k \):
\[
d_k \geq y_k - (bx_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
d_k \geq -(y_k - (bx_k + a)) \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Output}
The output will be in the format:
\[
\{ \text{"intercept"}: a, \text{"slope"}: b \}
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

\section*{Linear Programming Model for Fitting a Line}

Given the data points \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we want to fit the best straight line of the form:
\[
y = bx + a
\]
Our objective is to minimize the sum of absolute deviations of each observed value of \( y \) from the value predicted by the linear relationship. This can be formulated as follows:

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( a \): Intercept of the fitted line
    \item \( b \): Slope of the fitted line
    \item \( d_k \): Absolute deviation for each observation, defined as \( d_k = |y_k - (bx_k + a)| \)
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the sum of the absolute deviations:
\[
\text{Minimize } Z = \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
For each observation \( k \):
\[
d_k \geq y_k - (bx_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
d_k \geq -(y_k - (bx_k + a)) \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Output}
The output will be in the format:
\[
\{ \text{"intercept"}: a, \text{"slope"}: b \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = data['K']
X = data['X']
Y = data['Y']

#### Create a linear programming problem
problem = pulp.LpProblem("LineFitting", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", lowBound=None)  #### Intercept
b = pulp.LpVariable("b", lowBound=None)  #### Slope
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  #### Absolute deviations

#### Objective Function
problem += pulp.lpSum(d[k] for k in range(K)), "MinimizeAbsoluteDeviations"

#### Constraints
for k in range(K):
    problem += d[k] >= Y[k] - (b * X[k] + a), f"deviation_constraint_upper_{k}"
    problem += d[k] >= -(Y[k] - (b * X[k] + a)), f"deviation_constraint_lower_{k}"

#### Solve the problem
problem.solve()

#### Output intercept and slope
intercept = a.varValue
slope = b.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'{{ "intercept": {intercept}, "slope": {slope} }}')
```


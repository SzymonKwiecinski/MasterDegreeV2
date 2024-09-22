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

Given the data pairs of \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we want to fit a line described by the equation:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope. Our goal is to minimize the maximum deviation between the observed values \( y_k \) and the predicted values \( \hat{y}_k = bx_k + a \).

Let \( d_k \) represent the deviation for each observation \( k \):

\[
d_k = y_k - (bx_k + a)
\]

To minimize the maximum deviation, we introduce an auxiliary variable \( M \) such that:

\[
d_k \leq M \quad \text{and} \quad -d_k \leq M \quad \forall k
\]

This leads to the following set of inequalities:

\[
y_k - (bx_k + a) \leq M \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq M \quad \forall k
\]

The objective is to minimize \( M \).

\textbf{Objective Function:}

\[
\text{Minimize } M
\]

\textbf{Subject to:}

\[
y_k - bx_k - a \leq M \quad \forall k \in \{1, \ldots, K\}
\]
\[
-(y_k - bx_k - a) \leq M \quad \forall k \in \{1, \ldots, K\}
\]

\textbf{Variables:}
\begin{itemize}
    \item \( a \): intercept of the fitted line
    \item \( b \): slope of the fitted line
    \item \( M \): maximum deviation
\end{itemize}

This linear programming formulation allows us to determine the values of \( a \) and \( b \) that minimize the maximum deviation from the predicted line.

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

Given the data pairs of \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we want to fit a line described by the equation:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope. Our goal is to minimize the maximum deviation between the observed values \( y_k \) and the predicted values \( \hat{y}_k = bx_k + a \).

Let \( d_k \) represent the deviation for each observation \( k \):

\[
d_k = y_k - (bx_k + a)
\]

To minimize the maximum deviation, we introduce an auxiliary variable \( M \) such that:

\[
d_k \leq M \quad \text{and} \quad -d_k \leq M \quad \forall k
\]

This leads to the following set of inequalities:

\[
y_k - (bx_k + a) \leq M \quad \forall k
\]
\[
-(y_k - (bx_k + a)) \leq M \quad \forall k
\]

The objective is to minimize \( M \).

\textbf{Objective Function:}

\[
\text{Minimize } M
\]

\textbf{Subject to:}

\[
y_k - bx_k - a \leq M \quad \forall k \in \{1, \ldots, K\}
\]
\[
-(y_k - bx_k - a) \leq M \quad \forall k \in \{1, \ldots, K\}
\]

\textbf{Variables:}
\begin{itemize}
    \item \( a \): intercept of the fitted line
    \item \( b \): slope of the fitted line
    \item \( M \): maximum deviation
\end{itemize}

This linear programming formulation allows us to determine the values of \( a \) and \( b \) that minimize the maximum deviation from the predicted line.

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

#### Number of observations
K = data['NumObs']
Y = data['Y']
X = data['X']

#### Problem definition
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable("a", lowBound=None)  #### intercept
b = pulp.LpVariable("b", lowBound=None)  #### slope
M = pulp.LpVariable("M", lowBound=0)     #### maximum deviation

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= M
    problem += -(Y[k] - (b * X[k] + a)) <= M

#### Objective function
problem += M

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


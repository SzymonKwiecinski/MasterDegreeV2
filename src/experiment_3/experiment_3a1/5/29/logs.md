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

Given a set of observations $\{(x_k, y_k) \; | \; k = 1, \ldots, K\}$, we want to fit a linear model of the form:

\[
y = bx + a
\]

where $b$ is the slope and $a$ is the intercept.

\subsection*{Objective Function}
We want to minimize the maximum deviation of the observed values of $y$ from those predicted by the linear model. Therefore, we introduce non-negative slack variables $d_k$ for each observation, where:

\[
d_k \geq 0 \quad \forall k = 1, \ldots, K
\]

The objective is to minimize the maximum deviation:

\[
\min \; D
\]

subject to:

\[
y_k - (bx_k + a) \leq D \quad \forall k = 1, \ldots, K
\]

\[
(bx_k + a) - y_k \leq D \quad \forall k = 1, \ldots, K
\]

\subsection*{Constraints}
We can express the constraints in terms of the deviations:

\[
y_k - bx_k - a \leq D \quad \forall k = 1, \ldots, K
\]

\[
bx_k + a - y_k \leq D \quad \forall k = 1, \ldots, K
\]

This results in the following set of constraints that must be satisfied:

1. $y_k - bx_k - a \leq D$ for each $k$.
2. $bx_k + a - y_k \leq D$ for each $k$.
3. $D \geq 0$.

\subsection*{Final Formulation}
The complete linear programming formulation can be summarized as follows:

\[
\begin{align*}
\text{Minimize} \quad & D \\
\text{subject to} \quad & y_k - bx_k - a \leq D \quad \forall k = 1, \ldots, K \\
& bx_k + a - y_k \leq D \quad \forall k = 1, \ldots, K \\
& D \geq 0 \\
& b, a \text{ are free variables.}
\end{align*}
\]

\subsection*{Outputs}
Once the linear program is solved, the values of the intercept $a$ and slope $b$ can be extracted:

\begin{itemize}
    \item \texttt{intercept} represents the intercept of the fitted line ($a$).
    \item \texttt{slope} represents the slope of the fitted line ($b$).
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

\section*{Linear Programming Model for Linear Regression}

Given a set of observations $\{(x_k, y_k) \; | \; k = 1, \ldots, K\}$, we want to fit a linear model of the form:

\[
y = bx + a
\]

where $b$ is the slope and $a$ is the intercept.

\subsection*{Objective Function}
We want to minimize the maximum deviation of the observed values of $y$ from those predicted by the linear model. Therefore, we introduce non-negative slack variables $d_k$ for each observation, where:

\[
d_k \geq 0 \quad \forall k = 1, \ldots, K
\]

The objective is to minimize the maximum deviation:

\[
\min \; D
\]

subject to:

\[
y_k - (bx_k + a) \leq D \quad \forall k = 1, \ldots, K
\]

\[
(bx_k + a) - y_k \leq D \quad \forall k = 1, \ldots, K
\]

\subsection*{Constraints}
We can express the constraints in terms of the deviations:

\[
y_k - bx_k - a \leq D \quad \forall k = 1, \ldots, K
\]

\[
bx_k + a - y_k \leq D \quad \forall k = 1, \ldots, K
\]

This results in the following set of constraints that must be satisfied:

1. $y_k - bx_k - a \leq D$ for each $k$.
2. $bx_k + a - y_k \leq D$ for each $k$.
3. $D \geq 0$.

\subsection*{Final Formulation}
The complete linear programming formulation can be summarized as follows:

\[
\begin{align*}
\text{Minimize} \quad & D \\
\text{subject to} \quad & y_k - bx_k - a \leq D \quad \forall k = 1, \ldots, K \\
& bx_k + a - y_k \leq D \quad \forall k = 1, \ldots, K \\
& D \geq 0 \\
& b, a \text{ are free variables.}
\end{align*}
\]

\subsection*{Outputs}
Once the linear program is solved, the values of the intercept $a$ and slope $b$ can be extracted:

\begin{itemize}
    \item \texttt{intercept} represents the intercept of the fitted line ($a$).
    \item \texttt{slope} represents the slope of the fitted line ($b$).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data_json = '{"NumObs": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Number of observations
K = data['NumObs']
X = data['X']
Y = data['Y']

#### Create a linear programming problem
problem = pulp.LpProblem("Linear_Regression", pulp.LpMinimize)

#### Decision variables
b = pulp.LpVariable("b", None, None)  #### Slope
a = pulp.LpVariable("a", None, None)  #### Intercept
D = pulp.LpVariable("D", 0)            #### Maximum deviation (non-negative)

#### Objective Function
problem += D

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) <= D
    problem += (b * X[k] + a) - Y[k] <= D

#### Solve the problem
problem.solve()

#### Outputs
intercept = a.varValue
slope = b.varValue

#### Objective value
print(f'Intercept: {intercept}, Slope: {slope}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


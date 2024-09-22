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
To fit the 'best' straight line \( y = bx + a \) such that the maximum deviation of all observed values of \( y \) from the predicted values is minimized, we can formulate this problem as a Linear Programming (LP) problem. Specifically, we aim to minimize the maximum absolute deviation from the line.

The mathematical model of this problem can be constructed as follows:

Define:
- \( y_k \): the observed \( y \)-value for the \( k \)-th observation
- \( x_k \): the corresponding \( x \)-value for the \( k \)-th observation
- \( a \): the intercept of the fitted line
- \( b \): the slope of the fitted line
- \( D \): the maximum deviation

Objective:
- Minimize the maximum deviation \( D \).

Constraints:
- For each observation \( k \):
  \[
  y_k - (bx_k + a) \leq D
  \]
  \[
  (bx_k + a) - y_k \leq D
  \]

These constraints ensure that the deviation for each observed point is bounded by \( D \), and our objective is to minimize \( D \).

The mathematical model in LaTeX is given below:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective:}

Minimize \( D \)

\subsection*{Subject to:}

\begin{align*}
y_k - (bx_k + a) & \leq D, \quad \text{for } k = 1, 2, \ldots, K \\
(bx_k + a) - y_k & \leq D, \quad \text{for } k = 1, 2, \ldots, K \\
\end{align*}

\subsection*{Variables:}
\begin{itemize}
    \item \( a \): intercept of the fitted line
    \item \( b \): slope of the fitted line
    \item \( D \): maximum deviation
\end{itemize}

\end{document}
```

This formulation captures the essence of minimizing the maximum deviation of the data points from the fitted line, which is a robust approach to fitting a line in scenarios involving linear relationships.

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

\subsection*{Objective:}

Minimize \( D \)

\subsection*{Subject to:}

\begin{align*}
y_k - (bx_k + a) & \leq D, \quad \text{for } k = 1, 2, \ldots, K \\
(bx_k + a) - y_k & \leq D, \quad \text{for } k = 1, 2, \ldots, K \\
\end{align*}

\subsection*{Variables:}
\begin{itemize}
    \item \( a \): intercept of the fitted line
    \item \( b \): slope of the fitted line
    \item \( D \): maximum deviation
\end{itemize}

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
NumObs = data['NumObs']
Y = data['Y']
X = data['X']

#### Problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
D = pulp.LpVariable('D', lowBound=0, cat='Continuous')

#### Objective
problem += D, "Minimize_Max_Deviation"

#### Constraints
for k in range(NumObs):
    y_k = Y[k]
    x_k = X[k]
    problem += y_k - (b * x_k + a) <= D, f"Upper_Deviation_Constraint_{k}"
    problem += (b * x_k + a) - y_k <= D, f"Lower_Deviation_Constraint_{k}"

#### Solve
problem.solve()

#### Output
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```


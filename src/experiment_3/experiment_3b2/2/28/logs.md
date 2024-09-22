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
To fit the 'best' straight line \( y = bx + a \) to the provided set of data points, we need to construct a linear programming model that minimizes the sum of absolute deviations of each observed \( y \) value from the predicted value. This is a classic problem of fitting a line using the Least Absolute Deviations (LAD) method.

Let's denote:

- \( y_k \) as the observed values of \( y \) for \( k = 1, \ldots, K \).
- \( x_k \) as the corresponding values of \( x \) for \( k = 1, \ldots, K \).

Our goal is to find values for \( a \) (the intercept) and \( b \) (the slope) such that the sum of absolute deviations is minimized:

The objective function to minimize is:

\[
\sum_{k=1}^{K} |y_k - (bx_k + a)|
\]

This is not directly linear due to the absolute value. To linearize the problem, introduce auxiliary variables \( d_k \) such that:

\[
d_k \geq y_k - (bx_k + a)
\]
\[
d_k \geq -(y_k - (bx_k + a))
\]

The objective now becomes:

\[
\min \sum_{k=1}^{K} d_k 
\]

Here's the linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

Minimize the objective function:

\[
\min \sum_{k=1}^{K} d_k
\]

Subject to the constraints:

\[
d_k \geq y_k - (bx_k + a), \quad \forall\, k = 1, \ldots, K
\]

\[
d_k \geq -(y_k - (bx_k + a)), \quad \forall\, k = 1, \ldots, K
\]

Variables:
\begin{itemize}
    \item \( a \): Intercept of the fitted line
    \item \( b \): Slope of the fitted line
    \item \( d_k \): Deviation for each data point (auxiliary variable), \( d_k \geq 0 \)
\end{itemize}

This model finds the intercept (\( a \)) and the slope (\( b \)) that minimize the sum of absolute deviations between the observed \( y \) values and the values predicted by the linear equation \( y = bx + a \).

\end{document}
```

By solving this linear program using an appropriate solver, you will obtain the values for \( a \) (intercept) and \( b \) (slope) that minimize the sum of absolute deviations from the observed values.

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

Minimize the objective function:

\[
\min \sum_{k=1}^{K} d_k
\]

Subject to the constraints:

\[
d_k \geq y_k - (bx_k + a), \quad \forall\, k = 1, \ldots, K
\]

\[
d_k \geq -(y_k - (bx_k + a)), \quad \forall\, k = 1, \ldots, K
\]

Variables:
\begin{itemize}
    \item \( a \): Intercept of the fitted line
    \item \( b \): Slope of the fitted line
    \item \( d_k \): Deviation for each data point (auxiliary variable), \( d_k \geq 0 \)
\end{itemize}

This model finds the intercept (\( a \)) and the slope (\( b \)) that minimize the sum of absolute deviations between the observed \( y \) values and the values predicted by the linear equation \( y = bx + a \).

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

#### Define variables
a = pulp.LpVariable("a", cat='Continuous')
b = pulp.LpVariable("b", cat='Continuous')
d = [pulp.LpVariable(f"d_{k}", lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(d)

#### Constraints
for k in range(K):
    problem += d[k] >= Y[k] - (b * X[k] + a)
    problem += d[k] >= -(Y[k] - (b * X[k] + a))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


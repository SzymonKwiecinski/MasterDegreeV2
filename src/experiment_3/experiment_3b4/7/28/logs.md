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
To solve this linear programming problem, we need to fit a straight line \( y = bx + a \) to the data points by minimizing the sum of absolute deviations of the observed values of \( y \) from the predicted values. The problem can be formulated as a linear programming model.

The decision variables are the intercept \( a \), slope \( b \), and the deviations \( d_k^+ \) and \( d_k^- \) for each data point \( k \).

The objective function is to minimize the sum of these deviations. The constraints ensure that each deviation captures the absolute error: \( d_k^+ \geq y_k - (bx_k + a) \) and \( d_k^- \geq (bx_k + a) - y_k \).

Here is a LaTeX representation of the linear programming model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Best Fit Line}

Given data points \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we aim to fit a straight line \( y = bx + a \) that minimizes the sum of absolute deviations. The problem can be formulated as follows:

\subsection*{Decision Variables}
\begin{align*}
a & \quad \text{(intercept of the line)} \\
b & \quad \text{(slope of the line)} \\
d_k^+, d_k^- & \quad \text{(positive and negative deviations for each data point \( k \))}
\end{align*}

\subsection*{Objective Function}
Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} (d_k^+ + d_k^-)
\]

\subsection*{Constraints}
For each data point \( k \):
\begin{align*}
x_k b + a + d_k^+ & \geq y_k \\
x_k b + a - d_k^- & \leq y_k \\
d_k^+, d_k^- & \geq 0
\end{align*}

\subsection*{Variables Bounds}
\begin{align*}
d_k^+, d_k^- & \geq 0 \quad \text{(non-negativity constraints for deviations)}
\end{align*}

\end{document}
```

By solving this linear programming problem, you obtain the values of \( a \) (intercept) and \( b \) (slope) that yield the 'best' straight line in terms of the objective specified.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Best Fit Line}

Given data points \( (x_k, y_k) \) for \( k = 1, \ldots, K \), we aim to fit a straight line \( y = bx + a \) that minimizes the sum of absolute deviations. The problem can be formulated as follows:

\subsection*{Decision Variables}
\begin{align*}
a & \quad \text{(intercept of the line)} \\
b & \quad \text{(slope of the line)} \\
d_k^+, d_k^- & \quad \text{(positive and negative deviations for each data point \( k \))}
\end{align*}

\subsection*{Objective Function}
Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} (d_k^+ + d_k^-)
\]

\subsection*{Constraints}
For each data point \( k \):
\begin{align*}
x_k b + a + d_k^+ & \geq y_k \\
x_k b + a - d_k^- & \leq y_k \\
d_k^+, d_k^- & \geq 0
\end{align*}

\subsection*{Variables Bounds}
\begin{align*}
d_k^+, d_k^- & \geq 0 \quad \text{(non-negativity constraints for deviations)}
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

K = data['K']
Y = data['Y']
X = data['X']

#### Problem
problem = pulp.LpProblem("BestFitLine", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
d_plus = [pulp.LpVariable(f'd_plus_{k}', lowBound=0, cat='Continuous') for k in range(K)]
d_minus = [pulp.LpVariable(f'd_minus_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum([d_plus[k] + d_minus[k] for k in range(K)])

#### Constraints
for k in range(K):
    problem += (X[k] * b + a + d_plus[k] >= Y[k])
    problem += (X[k] * b + a - d_minus[k] <= Y[k])

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


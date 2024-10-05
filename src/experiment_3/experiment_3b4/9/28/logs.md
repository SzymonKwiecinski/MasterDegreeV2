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
To fit a straight line \( y = bx + a \) to a given set of data points by minimizing the sum of absolute deviations, we can formulate this problem as a linear programming problem. Below is the mathematical model in LaTeX format for this problem.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Given a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we aim to fit a line \( y = bx + a \) such that the sum of absolute deviations is minimized.

\subsection*{Decision Variables}

\begin{itemize}
    \item \(a\): Intercept of the line
    \item \(b\): Slope of the line
    \item \(e_k\): Non-negative deviation for each data point \((x_k, y_k)\)
    \item \(f_k\): Non-negative deviation for each data point \((x_k, y_k)\)
\end{itemize}

\subsection*{Objective Function}

Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} (e_k + f_k)
\]

\subsection*{Constraints}

For each data point \( k = 1, \ldots, K \), the absolute deviation \( |y_k - (bx_k + a)| \) is represented using \(e_k\) and \(f_k\):
\[
y_k - (bx_k + a) = e_k - f_k
\]
\[
e_k \geq 0, \quad f_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Summary}

The linear programming model is:

\[
\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} (e_k + f_k) \\
\text{Subject to} \quad & y_k - (bx_k + a) = e_k - f_k, \quad k = 1, \ldots, K \\
& e_k \geq 0, \quad f_k \geq 0, \quad k = 1, \ldots, K
\end{align*}
\]

\end{document}
```

This linear programming problem can be solved using any standard LP solver, which will provide the optimal values for \(a\) (intercept) and \(b\) (slope) that minimize the sum of absolute deviations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Given a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), we aim to fit a line \( y = bx + a \) such that the sum of absolute deviations is minimized.

\subsection*{Decision Variables}

\begin{itemize}
    \item \(a\): Intercept of the line
    \item \(b\): Slope of the line
    \item \(e_k\): Non-negative deviation for each data point \((x_k, y_k)\)
    \item \(f_k\): Non-negative deviation for each data point \((x_k, y_k)\)
\end{itemize}

\subsection*{Objective Function}

Minimize the sum of absolute deviations:
\[
\min \sum_{k=1}^{K} (e_k + f_k)
\]

\subsection*{Constraints}

For each data point \( k = 1, \ldots, K \), the absolute deviation \( |y_k - (bx_k + a)| \) is represented using \(e_k\) and \(f_k\):
\[
y_k - (bx_k + a) = e_k - f_k
\]
\[
e_k \geq 0, \quad f_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Summary}

The linear programming model is:

\[
\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} (e_k + f_k) \\
\text{Subject to} \quad & y_k - (bx_k + a) = e_k - f_k, \quad k = 1, \ldots, K \\
& e_k \geq 0, \quad f_k \geq 0, \quad k = 1, \ldots, K
\end{align*}
\]

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

#### Problem Definition
problem = pulp.LpProblem("Minimize_Sum_of_Absolute_Deviation", pulp.LpMinimize)

#### Decision Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]
f = [pulp.LpVariable(f'f_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum([e[k] + f[k] for k in range(K)])

#### Constraints
for k in range(K):
    problem += Y[k] - (b * X[k] + a) == e[k] - f[k]

#### Solve the problem
problem.solve()

#### Display the result
print(f'Coefficients: a = {pulp.value(a)}, b = {pulp.value(b)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```



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
To solve this linear programming problem, we aim to fit the best straight line \( y = bx + a \) to a given set of data points by minimizing the sum of absolute deviations of the observed y-values from the predicted y-values. This problem can be formulated as a linear programming model.

Given the data:
- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

The objective is to find the values of \( a \) (intercept) and \( b \) (slope) such that the sum of absolute deviations is minimized:
\[ \min \sum_{k=1}^{K} \left| y_k - (bx_k + a) \right| \]

To formulate this as a linear program, introduce non-negative variables \( u_k \) and \( v_k \) for each data point, representing the positive and negative deviations respectively:
\[ u_k - v_k = y_k - (bx_k + a) \]

The objective function becomes:
\[ \min \sum_{k=1}^{K} (u_k + v_k) \]

Constraints ensure that these deviations accurately represent the absolute values:
\[ u_k, v_k \geq 0 \]

The complete linear programming formulation in LaTeX for this problem is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\[
\text{Minimize } \sum_{k=1}^{K} (u_k + v_k)
\]

subject to:

\[
u_k - v_k = y_k - (bx_k + a) \quad \forall k = 1, 2, \ldots, K
\]

\[
u_k \geq 0, \quad v_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\textbf{Decision Variables:}

- \( a \): Intercept of the line.
- \( b \): Slope of the line.
- \( u_k, v_k \): Non-negative deviations for each data point \( k \).

\end{document}
```

This model is a standard form of a linear programming problem, which can be solved using any LP solver to find the optimal intercept \( a \) and slope \( b \). The solver will return the values of the intercept and slope that minimize the sum of absolute deviations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model:}

\[
\text{Minimize } \sum_{k=1}^{K} (u_k + v_k)
\]

subject to:

\[
u_k - v_k = y_k - (bx_k + a) \quad \forall k = 1, 2, \ldots, K
\]

\[
u_k \geq 0, \quad v_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\textbf{Decision Variables:}

- \( a \): Intercept of the line.
- \( b \): Slope of the line.
- \( u_k, v_k \): Non-negative deviations for each data point \( k \).

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
data = {'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}
K = data['K']
Y = data['Y']
X = data['X']

#### Define a linear programming problem
problem = pulp.LpProblem("Linear_Regression_Minimization", pulp.LpMinimize)

#### Define decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
u = pulp.LpVariable.dicts('u', range(K), lowBound=0, cat='Continuous')
v = pulp.LpVariable.dicts('v', range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum([u[k] + v[k] for k in range(K)])

#### Constraints
for k in range(K):
    problem += u[k] - v[k] == Y[k] - (b * X[k] + a)

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


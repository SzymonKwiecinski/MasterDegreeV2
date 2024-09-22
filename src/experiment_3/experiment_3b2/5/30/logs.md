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


OBJECTIVE: Fit the ‘best’ quadratic curve y = c * x^2 + b * x + a to this set of data points. The objective is to minimize the sum of absolute deviations of each observed value of y from the value predicted by the quadratic relationship.

OUTPUT INFO:

- \var{quadratic} represents the coefficient of quadratic term
- \var{linear} represents the coefficient of linear term
- \var{constant} represents the coefficient of constant

OUTPUT FORMAT:

{
    "quadratic": quadratic,
    "linear": linear,
    "constant": constant
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To fit the best quadratic curve \( y = c \cdot x^2 + b \cdot x + a \) that minimizes the sum of absolute deviations, we will formulate a linear programming model. This model will involve minimizing the objective function subject to constraints for each data point.

Here's how the model is set up:

1. **Objective Function**: Minimize the sum of absolute deviations. For each data point \((x_k, y_k)\), we introduce a variable \( d_k \) representing the absolute deviation:
   \[
   \text{Minimize} \quad \sum_{k=1}^{K} d_k
   \]

2. **Constraints**: For each data point \((x_k, y_k)\), we ensure that the deviation \( d_k \) represents the absolute difference between the observed \( y_k \) and the predicted value \( c \cdot x_k^2 + b \cdot x_k + a \). This leads to the following constraints:
   \[
   y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq d_k
   \]
   \[
   (c \cdot x_k^2 + b \cdot x_k + a) - y_k \leq d_k
   \]

Using these components, let's write the complete linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model to Fit a Quadratic Curve}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), our objective is to minimize the sum of absolute deviations between observed and predicted values using the quadratic model \(y = c \cdot x^2 + b \cdot x + a\).

\subsection*{Objective Function}
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
For each data point \(k = 1, \ldots, K\):
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq d_k 
\]
\[
(c \cdot x_k^2 + b \cdot x_k + a) - y_k \leq d_k 
\]

\subsection*{Variables}
- \(c\): Coefficient of the quadratic term
- \(b\): Coefficient of the linear term
- \(a\): Constant term
- \(d_k\): Absolute deviation for each data point

\subsection*{Solution}
Solve the above linear programming model to obtain the optimal values for \(c\), \(b\), and \(a\).

\end{document}
```

This formulation sets up a linear programming problem that can be solved using any LP solver to yield the best-fitting quadratic coefficients.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model to Fit a Quadratic Curve}

Given data points \((x_k, y_k)\) for \(k = 1, \ldots, K\), our objective is to minimize the sum of absolute deviations between observed and predicted values using the quadratic model \(y = c \cdot x^2 + b \cdot x + a\).

\subsection*{Objective Function}
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
For each data point \(k = 1, \ldots, K\):
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq d_k 
\]
\[
(c \cdot x_k^2 + b \cdot x_k + a) - y_k \leq d_k 
\]

\subsection*{Variables}
- \(c\): Coefficient of the quadratic term
- \(b\): Coefficient of the linear term
- \(a\): Constant term
- \(d_k\): Absolute deviation for each data point

\subsection*{Solution}
Solve the above linear programming model to obtain the optimal values for \(c\), \(b\), and \(a\).

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Create the linear programming problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)  #### Coefficient of x^2
b = pulp.LpVariable("b", lowBound=None)  #### Coefficient of x
a = pulp.LpVariable("a", lowBound=None)  #### Constant term

#### Variables for absolute deviations
K = len(data['y'])
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]  #### Absolute deviation

#### Objective function: minimize the sum of absolute deviations
problem += pulp.lpSum(d), "TotalAbsoluteDeviation"

#### Constraints for each data point
for k in range(K):
    problem += data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a) <= d[k], f"UpperBoundConstraint_{k}"
    problem += (c * data['x'][k]**2 + b * data['x'][k] + a) - data['y'][k] <= d[k], f"LowerBoundConstraint_{k}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


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
To formulate the given problem as a linear programming problem, we want to minimize the sum of absolute deviations between the observed values and the predicted values from a quadratic model. Here, the objective is to determine the coefficients \(a\), \(b\), and \(c\) of the quadratic equation \(y = c \cdot x^2 + b \cdot x + a\) that best fits the data in terms of minimizing the absolute deviations.

We will introduce auxiliary variables \(z_k^+\) and \(z_k^-\) to handle the absolute deviations for each data point. The objective can be expressed as:

\[
\min \sum_{k=1}^{K} (z_k^+ + z_k^-)
\]

Subject to the following constraints for each data point \(k\):

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = z_k^+ - z_k^-
\]

Additionally, we impose:

\[
z_k^+, z_k^- \geq 0
\]

Below is the linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

Given the data set with corresponding values for \(x\) and \(y\) as provided, we aim to fit a quadratic curve to minimize the sum of absolute deviations.

\subsection*{Variables}
\begin{align*}
c & : \text{Coefficient of the quadratic term} \\
b & : \text{Coefficient of the linear term} \\
a & : \text{Coefficient of the constant term} \\
z_k^+ & : \text{Positive deviation for the } k\text{-th observation} \\
z_k^- & : \text{Negative deviation for the } k\text{-th observation}
\end{align*}

\subsection*{Objective Function}
Minimize the total absolute deviation:
\[
\min \sum_{k=1}^{K} (z_k^+ + z_k^-)
\]

\subsection*{Constraints}
For each observation \(k\):
\begin{align*}
y_k - (c \cdot x_k^2 + b \cdot x_k + a) &= z_k^+ - z_k^- \\
z_k^+, z_k^- & \geq 0
\end{align*}

\end{document}
```

This formulation will enable you to solve for the coefficients \(a\), \(b\), and \(c\) that minimize the deviation of the observed values from the quadratic fit.

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

Given the data set with corresponding values for \(x\) and \(y\) as provided, we aim to fit a quadratic curve to minimize the sum of absolute deviations.

\subsection*{Variables}
\begin{align*}
c & : \text{Coefficient of the quadratic term} \\
b & : \text{Coefficient of the linear term} \\
a & : \text{Coefficient of the constant term} \\
z_k^+ & : \text{Positive deviation for the } k\text{-th observation} \\
z_k^- & : \text{Negative deviation for the } k\text{-th observation}
\end{align*}

\subsection*{Objective Function}
Minimize the total absolute deviation:
\[
\min \sum_{k=1}^{K} (z_k^+ + z_k^-)
\]

\subsection*{Constraints}
For each observation \(k\):
\begin{align*}
y_k - (c \cdot x_k^2 + b \cdot x_k + a) &= z_k^+ - z_k^- \\
z_k^+, z_k^- & \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

#### Problem
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Decision Variables
c = pulp.LpVariable('c', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')

z_plus = pulp.LpVariable.dicts('z_plus', range(K), lowBound=0, cat='Continuous')
z_minus = pulp.LpVariable.dicts('z_minus', range(K), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(z_plus[k] + z_minus[k] for k in range(K))

#### Constraints
for k in range(K):
    problem += y[k] - (c * (x[k] ** 2) + b * x[k] + a) == z_plus[k] - z_minus[k]

#### Solve
problem.solve()

#### Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


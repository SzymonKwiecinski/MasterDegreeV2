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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Quadratic Curve Fitting}

Given a set of data points represented as $(x_k, y_k)$ for $k = 1, \ldots, K$, we aim to fit the best quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

We will minimize the sum of absolute deviations between the observed values and the predicted values of $y$. Define the deviation for each observation as:

\[
d_k = y_k - (c x_k^2 + b x_k + a)
\]

The objective function is to minimize the sum of absolute deviations:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} |d_k|
\]

To handle the absolute values, we introduce slack variables $d_k^+$ and $d_k^-$ such that:

\[
d_k = d_k^+ - d_k^-
\]

and impose the constraints:

\[
d_k^+ \geq d_k
\]
\[
d_k^- \geq -d_k
\]

Substituting $d_k = y_k - (c x_k^2 + b x_k + a)$ gives us the following constraints:

\[
d_k^+ \geq y_k - (c x_k^2 + b x_k + a)
\]
\[
d_k^- \geq -(y_k - (c x_k^2 + b x_k + a))
\]

Then the objective function can be rewritten as:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} (d_k^+ + d_k^-)
\]

The complete linear programming formulation then becomes:

\[
\begin{aligned}
& \text{Minimize} && Z = \sum_{k=1}^{K} (d_k^+ + d_k^-) \\
& \text{subject to} \\
& && d_k^+ \geq y_k - (c x_k^2 + b x_k + a) && \text{for } k = 1, \ldots, K \\
& && d_k^- \geq - (y_k - (c x_k^2 + b x_k + a)) && \text{for } k = 1, \ldots, K \\
& && d_k^+ \geq 0, \quad d_k^- \geq 0 && \text{for } k = 1, \ldots, K \\
\end{aligned}
\]

The solution of this linear programming problem will yield the values for the coefficients:

\[
\text{quadratic} = c, \quad \text{linear} = b, \quad \text{constant} = a
\]

These coefficients will provide the best fit quadratic curve for the given data.

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

\section*{Linear Programming Model for Quadratic Curve Fitting}

Given a set of data points represented as $(x_k, y_k)$ for $k = 1, \ldots, K$, we aim to fit the best quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

We will minimize the sum of absolute deviations between the observed values and the predicted values of $y$. Define the deviation for each observation as:

\[
d_k = y_k - (c x_k^2 + b x_k + a)
\]

The objective function is to minimize the sum of absolute deviations:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} |d_k|
\]

To handle the absolute values, we introduce slack variables $d_k^+$ and $d_k^-$ such that:

\[
d_k = d_k^+ - d_k^-
\]

and impose the constraints:

\[
d_k^+ \geq d_k
\]
\[
d_k^- \geq -d_k
\]

Substituting $d_k = y_k - (c x_k^2 + b x_k + a)$ gives us the following constraints:

\[
d_k^+ \geq y_k - (c x_k^2 + b x_k + a)
\]
\[
d_k^- \geq -(y_k - (c x_k^2 + b x_k + a))
\]

Then the objective function can be rewritten as:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} (d_k^+ + d_k^-)
\]

The complete linear programming formulation then becomes:

\[
\begin{aligned}
& \text{Minimize} && Z = \sum_{k=1}^{K} (d_k^+ + d_k^-) \\
& \text{subject to} \\
& && d_k^+ \geq y_k - (c x_k^2 + b x_k + a) && \text{for } k = 1, \ldots, K \\
& && d_k^- \geq - (y_k - (c x_k^2 + b x_k + a)) && \text{for } k = 1, \ldots, K \\
& && d_k^+ \geq 0, \quad d_k^- \geq 0 && \text{for } k = 1, \ldots, K \\
\end{aligned}
\]

The solution of this linear programming problem will yield the values for the coefficients:

\[
\text{quadratic} = c, \quad \text{linear} = b, \quad \text{constant} = a
\]

These coefficients will provide the best fit quadratic curve for the given data.

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Create the problem variable
problem = pulp.LpProblem("QuadraticCurveFitting", pulp.LpMinimize)

#### Variables for the coefficients of the quadratic function
c = pulp.LpVariable("c", lowBound=None)  #### Coefficient of x^2
b = pulp.LpVariable("b", lowBound=None)  #### Coefficient of x
a = pulp.LpVariable("a", lowBound=None)  #### Constant term

#### Number of data points
K = len(data['y'])

#### Slack variables for deviations
d_plus = [pulp.LpVariable(f"d_plus_{k}", lowBound=0) for k in range(K)]
d_minus = [pulp.LpVariable(f"d_minus_{k}", lowBound=0) for k in range(K)]

#### Objective function: Minimize the sum of deviations
problem += pulp.lpSum(d_plus[k] + d_minus[k] for k in range(K)), "Minimize_Absolute_Deviation"

#### Constraints for each data point
for k in range(K):
    problem += d_plus[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a), f"Pos_Dev_Constraint_{k}"
    problem += d_minus[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)), f"Neg_Dev_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


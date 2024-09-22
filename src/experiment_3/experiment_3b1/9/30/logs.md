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

\section*{Quadratic Curve Fitting Problem}

We want to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

to a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\). The objective is to minimize the sum of absolute deviations between the observed values of \(y\) and the values predicted by the quadratic relationship.

Let:

\[
d_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Our objective function can be expressed as:

\[
\min \sum_{k=1}^{K} d_k
\]

To enforce the absolute value in our optimization problem, we can introduce non-negative slack variables \(t_k\) such that:

\[
d_k = t_k
\]

and

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq t_k,
\]

\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq t_k.
\]

This leads us to the following constraints:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq t_k \quad \forall k
\]

\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq t_k \quad \forall k
\]

The complete linear programming formulation can be summarized as follows:

\begin{align*}
\text{Minimize} & \quad \sum_{k=1}^{K} t_k \\
\text{Subject to} & \quad y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq t_k \quad \forall k \\
& \quad -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq t_k \quad \forall k \\
& \quad t_k \geq 0 \quad \forall k \\
\end{align*}

\noindent where:

\begin{itemize}
    \item \(c\) represents the coefficient of the quadratic term,
    \item \(b\) represents the coefficient of the linear term,
    \item \(a\) represents the coefficient of the constant term.
\end{itemize}

The solution will yield the values of \(c\), \(b\), and \(a\) that minimize the sum of absolute deviations.

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

\section*{Quadratic Curve Fitting Problem}

We want to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

to a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\). The objective is to minimize the sum of absolute deviations between the observed values of \(y\) and the values predicted by the quadratic relationship.

Let:

\[
d_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Our objective function can be expressed as:

\[
\min \sum_{k=1}^{K} d_k
\]

To enforce the absolute value in our optimization problem, we can introduce non-negative slack variables \(t_k\) such that:

\[
d_k = t_k
\]

and

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq t_k,
\]

\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq t_k.
\]

This leads us to the following constraints:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq t_k \quad \forall k
\]

\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq t_k \quad \forall k
\]

The complete linear programming formulation can be summarized as follows:

\begin{align*}
\text{Minimize} & \quad \sum_{k=1}^{K} t_k \\
\text{Subject to} & \quad y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq t_k \quad \forall k \\
& \quad -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq t_k \quad \forall k \\
& \quad t_k \geq 0 \quad \forall k \\
\end{align*}

\noindent where:

\begin{itemize}
    \item \(c\) represents the coefficient of the quadratic term,
    \item \(b\) represents the coefficient of the linear term,
    \item \(a\) represents the coefficient of the constant term.
\end{itemize}

The solution will yield the values of \(c\), \(b\), and \(a\) that minimize the sum of absolute deviations.

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

#### Extracting x and y values
x_values = data['x']
y_values = data['y']
K = len(x_values)

#### Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Decision variables
c = pulp.LpVariable('c', lowBound=None)  #### Coefficient of x^2
b = pulp.LpVariable('b', lowBound=None)  #### Coefficient of x
a = pulp.LpVariable('a', lowBound=None)  #### Constant term
t = pulp.LpVariable.dicts('t', range(K), lowBound=0)  #### Slack variables

#### Objective function
problem += pulp.lpSum(t[k] for k in range(K)), "Total_Absolute_Deviation"

#### Constraints
for k in range(K):
    problem += y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a) <= t[k], f"Upper_Bound_Constraint_{k}"
    problem += -(y_values[k] - (c * x_values[k]**2 + b * x_values[k] + a)) <= t[k], f"Lower_Bound_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f' Coefficients: a = {a.varValue}, b = {b.varValue}, c = {c.varValue}')
```


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

\section*{Quadratic Curve Fitting using Linear Programming}

We want to fit a quadratic curve of the form 

\[
y = c \cdot x^2 + b \cdot x + a
\]

to a set of data points \((x_k, y_k)\) for \(k = 1, 2, \ldots, K\). The objective is to minimize the sum of absolute deviations between the observed values of \(y\) and the predicted values based on the quadratic relationship.

Let \(y_k\) be the observed value and \(\hat{y_k} = c \cdot x_k^2 + b \cdot x_k + a\) be the predicted value. The absolute deviation can be expressed as 

\[
d_k = |y_k - \hat{y_k}|
\]

We aim to minimize the total absolute deviation:

\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

We introduce auxiliary variables \(u_k\) and \(v_k\) to represent the positive and negative deviations:

\[
y_k - \hat{y_k} = u_k - v_k
\]

with the constraints:

\[
d_k = u_k + v_k
\]

Thus, we can rewrite our objective function as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} (u_k + v_k)
\]

The complete optimization problem can be formulated as:

\[
\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} (u_k + v_k) \\
\text{Subject to} \quad & u_k - v_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, 2, \ldots, K \\
& u_k \geq 0, \quad v_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}
\]

After solving the above linear programming problem, we can extract the coefficients:

\[
\begin{align*}
\text{quadratic} & : c \\
\text{linear} & : b \\
\text{constant} & : a
\end{align*}
\]

The final output format will be:

\[
\{
    "quadratic": c,
    "linear": b,
    "constant": a
\}
\]

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

\section*{Quadratic Curve Fitting using Linear Programming}

We want to fit a quadratic curve of the form 

\[
y = c \cdot x^2 + b \cdot x + a
\]

to a set of data points \((x_k, y_k)\) for \(k = 1, 2, \ldots, K\). The objective is to minimize the sum of absolute deviations between the observed values of \(y\) and the predicted values based on the quadratic relationship.

Let \(y_k\) be the observed value and \(\hat{y_k} = c \cdot x_k^2 + b \cdot x_k + a\) be the predicted value. The absolute deviation can be expressed as 

\[
d_k = |y_k - \hat{y_k}|
\]

We aim to minimize the total absolute deviation:

\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

We introduce auxiliary variables \(u_k\) and \(v_k\) to represent the positive and negative deviations:

\[
y_k - \hat{y_k} = u_k - v_k
\]

with the constraints:

\[
d_k = u_k + v_k
\]

Thus, we can rewrite our objective function as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} (u_k + v_k)
\]

The complete optimization problem can be formulated as:

\[
\begin{align*}
\text{Minimize} \quad & \sum_{k=1}^{K} (u_k + v_k) \\
\text{Subject to} \quad & u_k - v_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a), \quad k = 1, 2, \ldots, K \\
& u_k \geq 0, \quad v_k \geq 0, \quad k = 1, 2, \ldots, K
\end{align*}
\]

After solving the above linear programming problem, we can extract the coefficients:

\[
\begin{align*}
\text{quadratic} & : c \\
\text{linear} & : b \\
\text{constant} & : a
\end{align*}
\]

The final output format will be:

\[
\{
    "quadratic": c,
    "linear": b,
    "constant": a
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

#### Set up the problem
K = len(data['y'])
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Decision variables
c = pulp.LpVariable("c", cat='Real')
b = pulp.LpVariable("b", cat='Real')
a = pulp.LpVariable("a", cat='Real')
u = [pulp.LpVariable(f'u_{k}', lowBound=0) for k in range(K)]
v = [pulp.LpVariable(f'v_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(u[k] + v[k] for k in range(K)), "Minimize_Total_Deviation"

#### Constraints
for k in range(K):
    problem += u[k] - v[k] == data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a), f"Deviations_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Output results
results = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


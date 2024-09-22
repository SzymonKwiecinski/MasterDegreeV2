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

We aim to fit a quadratic curve of the form:
\[
y = c \cdot x^2 + b \cdot x + a
\]
to a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\). The objective is to minimize the sum of absolute deviations between the observed values \(y_k\) and the predicted values from the quadratic model.

\subsection*{Variable Definitions}
Let:
\begin{itemize}
    \item \(y_k\) be the observed values, where \(k = 1, 2, \ldots, K\),
    \item \(x_k\) be the corresponding independent variable values,
    \item \(a\) be the constant coefficient,
    \item \(b\) be the linear coefficient,
    \item \(c\) be the quadratic coefficient,
    \item \(d_k\) be the absolute deviation defined as \(d_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a)\).
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total absolute deviation:
\[
\min \sum_{k=1}^{K} |d_k|
\]

This can be reformulated using auxiliary variables \(u_k\) and \(v_k\) such that:
\[
d_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]
We express the absolute deviations using these variables:
\[
d_k \leq u_k, \quad -d_k \leq v_k, \quad u_k, v_k \geq 0
\]
Thus, our optimization problem can be reformulated as:
\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

\subsection*{Linear Constraints}
The linear constraints can be written as:
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq u_k \quad \text{for } k = 1, \ldots, K
\]
\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq v_k \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Output Format}
After solving the linear programming problem, the output will be given in the following format:
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

We aim to fit a quadratic curve of the form:
\[
y = c \cdot x^2 + b \cdot x + a
\]
to a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\). The objective is to minimize the sum of absolute deviations between the observed values \(y_k\) and the predicted values from the quadratic model.

\subsection*{Variable Definitions}
Let:
\begin{itemize}
    \item \(y_k\) be the observed values, where \(k = 1, 2, \ldots, K\),
    \item \(x_k\) be the corresponding independent variable values,
    \item \(a\) be the constant coefficient,
    \item \(b\) be the linear coefficient,
    \item \(c\) be the quadratic coefficient,
    \item \(d_k\) be the absolute deviation defined as \(d_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a)\).
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total absolute deviation:
\[
\min \sum_{k=1}^{K} |d_k|
\]

This can be reformulated using auxiliary variables \(u_k\) and \(v_k\) such that:
\[
d_k = y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]
We express the absolute deviations using these variables:
\[
d_k \leq u_k, \quad -d_k \leq v_k, \quad u_k, v_k \geq 0
\]
Thus, our optimization problem can be reformulated as:
\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

\subsection*{Linear Constraints}
The linear constraints can be written as:
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq u_k \quad \text{for } k = 1, \ldots, K
\]
\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq v_k \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Output Format}
After solving the linear programming problem, the output will be given in the following format:
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

#### Sample data
data_json = """{
    "y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}"""
data = json.loads(data_json)

#### Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable("a", cat="Continuous")
b = pulp.LpVariable("b", cat="Continuous")
c = pulp.LpVariable("c", cat="Continuous")

#### Deviations
K = len(data['y'])
u = [pulp.LpVariable(f"u_{k}", lowBound=0) for k in range(K)]
v = [pulp.LpVariable(f"v_{k}", lowBound=0) for k in range(K)]

#### Objective function: minimize the sum of u_k and v_k
problem += pulp.lpSum(u[k] + v[k] for k in range(K))

#### Adding constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    problem += y_k - (c * x_k**2 + b * x_k + a) <= u[k]
    problem += -(y_k - (c * x_k**2 + b * x_k + a)) <= v[k]

#### Solve the problem
problem.solve()

#### Print the objective value and the coefficients
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps({
    "quadratic": pulp.value(c),
    "linear": pulp.value(b),
    "constant": pulp.value(a)
}))
```


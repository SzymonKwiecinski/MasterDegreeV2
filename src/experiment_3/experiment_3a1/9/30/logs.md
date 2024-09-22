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

Given a set of data points represented by \( K \) observations of \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \), we aim to fit the quadratic curve defined by:

\[
y = c \cdot x^2 + b \cdot x + a
\]

where \( c \) is the coefficient of the quadratic term, \( b \) is the coefficient of the linear term, and \( a \) is the constant term.

\subsection*{Objective Function}
The objective is to minimize the sum of absolute deviations between the observed \( y \) values and the predicted \( y \) values from the quadratic equation:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

To handle the absolute values, we introduce auxiliary variables \( d_k \):

\[
d_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
d_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \quad \text{for } k = 1, \ldots, K
\]

Thus, we can rewrite the objective function as:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
The problem leads to the following constraints based on the introduced variables:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq d_k \quad \text{for } k = 1, \ldots, K
\]

\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq d_k \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Variables}
The variables in this linear programming model are:

\begin{itemize}
    \item \( c \): coefficient of the quadratic term
    \item \( b \): coefficient of the linear term
    \item \( a \): constant term
    \item \( d_k \): auxiliary variables for \( k = 1, \ldots, K \)
\end{itemize}

\subsection*{Output Format}
The output format of the coefficients is as follows:

\[
\{
    \text{"quadratic"}: c,
    \text{"linear"}: b,
    \text{"constant"}: a
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

\section*{Linear Programming Model for Quadratic Curve Fitting}

Given a set of data points represented by \( K \) observations of \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \), we aim to fit the quadratic curve defined by:

\[
y = c \cdot x^2 + b \cdot x + a
\]

where \( c \) is the coefficient of the quadratic term, \( b \) is the coefficient of the linear term, and \( a \) is the constant term.

\subsection*{Objective Function}
The objective is to minimize the sum of absolute deviations between the observed \( y \) values and the predicted \( y \) values from the quadratic equation:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

To handle the absolute values, we introduce auxiliary variables \( d_k \):

\[
d_k \geq y_k - (c \cdot x_k^2 + b \cdot x_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
d_k \geq -(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \quad \text{for } k = 1, \ldots, K
\]

Thus, we can rewrite the objective function as:

\[
\text{Minimize} \quad Z = \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
The problem leads to the following constraints based on the introduced variables:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq d_k \quad \text{for } k = 1, \ldots, K
\]

\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq d_k \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Variables}
The variables in this linear programming model are:

\begin{itemize}
    \item \( c \): coefficient of the quadratic term
    \item \( b \): coefficient of the linear term
    \item \( a \): constant term
    \item \( d_k \): auxiliary variables for \( k = 1, \ldots, K \)
\end{itemize}

\subsection*{Output Format}
The output format of the coefficients is as follows:

\[
\{
    \text{"quadratic"}: c,
    \text{"linear"}: b,
    \text{"constant"}: a
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

#### Data input
data = json.loads("{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}")

x = data['x']
y = data['y']
K = len(x)

#### Create the linear programming problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)  #### Coefficient for x^2
b = pulp.LpVariable("b", lowBound=None)  #### Coefficient for x
a = pulp.LpVariable("a", lowBound=None)  #### Constant term

#### Auxiliary variables for absolute deviations
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(d[k] for k in range(K)), "Minimize_Absolute_Deviations"

#### Constraints for auxiliary variables
for k in range(K):
    problem += y[k] - (c * x[k]**2 + b * x[k] + a) <= d[k], f"Upper_Bound_Constraint_{k}"
    problem += -(y[k] - (c * x[k]**2 + b * x[k] + a)) <= d[k], f"Lower_Bound_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Output the coefficients
coefficients = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(coefficients)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


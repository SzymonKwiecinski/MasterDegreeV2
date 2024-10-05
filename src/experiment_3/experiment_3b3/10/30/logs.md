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

Given a set of corresponding values for \( x \) and \( y \):

\[
y = \{ y_k \,|\, k = 1, 2, \ldots, K \}
\]
\[
x = \{ x_k \,|\, k = 1, 2, \ldots, K \}
\]

We aim to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

where:
- \( c \) is the coefficient of the quadratic term,
- \( b \) is the coefficient of the linear term,
- \( a \) is the constant term.

The goal is to minimize the sum of absolute deviations of each observed value of \( y \) from the predicted value given by the quadratic relationship. This can be mathematically expressed as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Subject to:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq e_k, \quad \forall k
\]
\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq e_k, \quad \forall k
\]

where \( e_k \geq 0 \) are the new variables representing the absolute deviations.

This forms a linear programming problem where our output will be:

\[
\text{Output Format:} \quad \{ \text{quadratic}: c, \text{linear}: b, \text{constant}: a \}
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

\section*{Quadratic Curve Fitting Problem}

Given a set of corresponding values for \( x \) and \( y \):

\[
y = \{ y_k \,|\, k = 1, 2, \ldots, K \}
\]
\[
x = \{ x_k \,|\, k = 1, 2, \ldots, K \}
\]

We aim to fit a quadratic curve of the form:

\[
y = c \cdot x^2 + b \cdot x + a
\]

where:
- \( c \) is the coefficient of the quadratic term,
- \( b \) is the coefficient of the linear term,
- \( a \) is the constant term.

The goal is to minimize the sum of absolute deviations of each observed value of \( y \) from the predicted value given by the quadratic relationship. This can be mathematically expressed as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|
\]

Subject to:

\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) \leq e_k, \quad \forall k
\]
\[
-(y_k - (c \cdot x_k^2 + b \cdot x_k + a)) \leq e_k, \quad \forall k
\]

where \( e_k \geq 0 \) are the new variables representing the absolute deviations.

This forms a linear programming problem where our output will be:

\[
\text{Output Format:} \quad \{ \text{quadratic}: c, \text{linear}: b, \text{constant}: a \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON input
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Extract y and x values
y_values = data['y']
x_values = data['x']
K = len(y_values)

#### Define the LP problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Define variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
e = [pulp.LpVariable(f'e_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function: Minimize sum of absolute deviations
problem += pulp.lpSum(e)

#### Constraints for each data point
for k in range(K):
    x_k = x_values[k]
    y_k = y_values[k]
    #### y_k - (c * x_k^2 + b * x_k + a) <= e_k
    problem += y_k - (c * (x_k ** 2) + b * x_k + a) <= e[k]
    #### -(y_k - (c * x_k^2 + b * x_k + a)) <= e_k
    problem += -(y_k - (c * (x_k ** 2) + b * x_k + a)) <= e[k]

#### Solve the problem
problem.solve()

#### Output results
c_value = pulp.value(c)
b_value = pulp.value(b)
a_value = pulp.value(a)

print(f'(Quadratic): {c_value}, (Linear): {b_value}, (Constant): {a_value}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


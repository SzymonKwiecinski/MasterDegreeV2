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

Given a set of observed values \( y_k \) corresponding to values \( x_k \) for \( k = 1, \ldots, K \), the goal is to fit a quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

where:
- \( c \) is the coefficient of the quadratic term,
- \( b \) is the coefficient of the linear term,
- \( a \) is the constant term.

We aim to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values from the quadratic equation, which can be expressed mathematically as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

To formulate this as a Linear Programming (LP) problem, we can introduce auxiliary variables \( z_k \) such that:

\[
z_k \geq y_k - (c x_k^2 + b x_k + a) \quad \text{and} \quad z_k \geq -(y_k - (c x_k^2 + b x_k + a))
\]

The problem can then be rephrased as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} z_k
\]

subject to:

\[
z_k \geq y_k - (c x_k^2 + b x_k + a), \quad k = 1, \ldots, K
\]
\[
z_k \geq -(y_k - (c x_k^2 + b x_k + a)), \quad k = 1, \ldots, K
\]

The output coefficients will be represented as follows:

\[
\begin{align*}
\text{quadratic} & : c \\
\text{linear} & : b \\
\text{constant} & : a
\end{align*}
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

Given a set of observed values \( y_k \) corresponding to values \( x_k \) for \( k = 1, \ldots, K \), the goal is to fit a quadratic curve of the form:

\[
y = c x^2 + b x + a
\]

where:
- \( c \) is the coefficient of the quadratic term,
- \( b \) is the coefficient of the linear term,
- \( a \) is the constant term.

We aim to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values from the quadratic equation, which can be expressed mathematically as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} |y_k - (c x_k^2 + b x_k + a)|
\]

To formulate this as a Linear Programming (LP) problem, we can introduce auxiliary variables \( z_k \) such that:

\[
z_k \geq y_k - (c x_k^2 + b x_k + a) \quad \text{and} \quad z_k \geq -(y_k - (c x_k^2 + b x_k + a))
\]

The problem can then be rephrased as:

\[
\text{Minimize} \quad \sum_{k=1}^{K} z_k
\]

subject to:

\[
z_k \geq y_k - (c x_k^2 + b x_k + a), \quad k = 1, \ldots, K
\]
\[
z_k \geq -(y_k - (c x_k^2 + b x_k + a)), \quad k = 1, \ldots, K
\]

The output coefficients will be represented as follows:

\[
\begin{align*}
\text{quadratic} & : c \\
\text{linear} & : b \\
\text{constant} & : a
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = len(data['y'])

#### Create a problem variable
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)

#### Auxiliary variables for absolute deviations
z = [pulp.LpVariable(f"z_{k}", lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(z)

#### Constraints for the auxiliary variables
for k in range(K):
    problem += z[k] >= data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a)
    problem += z[k] >= -(data['y'][k] - (c * data['x'][k]**2 + b * data['x'][k] + a))

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f' Coefficient c: {c.varValue}')
print(f' Coefficient b: {b.varValue}')
print(f' Coefficient a: {a.varValue}')
```


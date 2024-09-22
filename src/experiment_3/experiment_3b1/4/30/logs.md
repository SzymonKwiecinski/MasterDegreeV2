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

We aim to fit the best quadratic curve of the form 
\[
y = c \cdot x^2 + b \cdot x + a
\]
to a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\). The objective is to minimize the sum of absolute deviations of each observed value of \(y\) from the predicted value of \(y\) given by the quadratic function.

\subsection*{Inputs}
The values of \(y\) and \(x\) are provided as follows:
\begin{align*}
y & = [y_{1}, y_{2}, \ldots, y_{K}] \\
x & = [x_{1}, x_{2}, \ldots, x_{K}]
\end{align*}

\subsection*{Objective Function}
We define the absolute deviations for each data point as follows:
\[
d_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|, \quad \text{for } k = 1, 2, \ldots, K
\]
The objective is to minimize the sum of these absolute deviations:
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

\subsection*{Variables}
The coefficients \(c\), \(b\), and \(a\) are the variables we need to determine:
\begin{align*}
\text{Let } & c \text{ be the coefficient of the quadratic term,} \\
& b \text{ be the coefficient of the linear term,} \\
& a \text{ be the constant term.}
\end{align*}

\subsection*{Output}
The output will specify the values of the coefficients:
\begin{verbatim}
{
    "quadratic": c,
    "linear": b,
    "constant": a
}
\end{verbatim}

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

We aim to fit the best quadratic curve of the form 
\[
y = c \cdot x^2 + b \cdot x + a
\]
to a set of data points \((x_k, y_k)\) for \(k = 1, \ldots, K\). The objective is to minimize the sum of absolute deviations of each observed value of \(y\) from the predicted value of \(y\) given by the quadratic function.

\subsection*{Inputs}
The values of \(y\) and \(x\) are provided as follows:
\begin{align*}
y & = [y_{1}, y_{2}, \ldots, y_{K}] \\
x & = [x_{1}, x_{2}, \ldots, x_{K}]
\end{align*}

\subsection*{Objective Function}
We define the absolute deviations for each data point as follows:
\[
d_k = |y_k - (c \cdot x_k^2 + b \cdot x_k + a)|, \quad \text{for } k = 1, 2, \ldots, K
\]
The objective is to minimize the sum of these absolute deviations:
\[
\text{Minimize} \quad \sum_{k=1}^{K} d_k
\]

\subsection*{Variables}
The coefficients \(c\), \(b\), and \(a\) are the variables we need to determine:
\begin{align*}
\text{Let } & c \text{ be the coefficient of the quadratic term,} \\
& b \text{ be the coefficient of the linear term,} \\
& a \text{ be the constant term.}
\end{align*}

\subsection*{Output}
The output will specify the values of the coefficients:
\begin{verbatim}
{
    "quadratic": c,
    "linear": b,
    "constant": a
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

#### Extract x and y values
y_values = data['y']
x_values = data['x']
K = len(y_values)

#### Create the problem
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Variables for coefficients
c = pulp.LpVariable("c", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
a = pulp.LpVariable("a", lowBound=None)

#### Variables for absolute deviations
d = [pulp.LpVariable(f"d_{k}", lowBound=0) for k in range(K)]

#### Objective Function: Minimize the sum of absolute deviations
problem += pulp.lpSum(d)

#### Constraints for absolute deviations
for k in range(K):
    problem += d[k] >= y_values[k] - (c * x_values[k] ** 2 + b * x_values[k] + a)
    problem += d[k] >= -(y_values[k] - (c * x_values[k] ** 2 + b * x_values[k] + a))

#### Solve the problem
problem.solve()

#### Output the results
results = {
    "quadratic": c.varValue,
    "linear": b.varValue,
    "constant": a.varValue
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(results, indent=4))
```


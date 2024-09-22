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
To model this problem as a linear programming problem using the given input and output format, we need to set up an optimization problem where the objective is to minimize the sum of the absolute deviations between the observed \(y\) values and those predicted by the quadratic model \(y = c \cdot x^2 + b \cdot x + a\).

In linear programming, absolute deviations can be handled by introducing auxiliary variables to replace the absolute terms. We'll use variables \(e_k^+\) and \(e_k^-\) to represent the positive and negative deviations, respectively, ensuring that \(e_k^+ - e_k^-\) approximates the deviation \(y_k - (c \cdot x_k^2 + b \cdot x_k + a)\).

Here's the linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation for Quadratic Curve Fitting}

Given the input data:

- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

We aim to find the coefficients \(a\), \(b\), and \(c\) for the quadratic equation \(y = c \cdot x^2 + b \cdot x + a\) such that the sum of the absolute deviations is minimized.

\[
\text{Minimize } \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

Subject to the constraints for each \(k = 1, \ldots, K\):

\[
e_k^+ - e_k^- = y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]

\[
e_k^+ \geq 0, \quad e_k^- \geq 0
\]

where:
- \(c\) is the coefficient of the quadratic term,
- \(b\) is the coefficient of the linear term,
- \(a\) is the constant term.

\end{document}
```

In this formulation, the decision variables are \(c\), \(b\), \(a\), \(e_k^+\), and \(e_k^-\) for all \(k = 1, \ldots, K\). The constraints ensure that the deviation between the observed and predicted values is represented by \(e_k^+ - e_k^-\), while the objective function minimizes the sum of these deviations. Solving this linear programming problem will yield the coefficients for the quadratic curve that best fits the provided data in terms of minimizing absolute deviations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation for Quadratic Curve Fitting}

Given the input data:

- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

We aim to find the coefficients \(a\), \(b\), and \(c\) for the quadratic equation \(y = c \cdot x^2 + b \cdot x + a\) such that the sum of the absolute deviations is minimized.

\[
\text{Minimize } \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

Subject to the constraints for each \(k = 1, \ldots, K\):

\[
e_k^+ - e_k^- = y_k - (c \cdot x_k^2 + b \cdot x_k + a)
\]

\[
e_k^+ \geq 0, \quad e_k^- \geq 0
\]

where:
- \(c\) is the coefficient of the quadratic term,
- \(b\) is the coefficient of the linear term,
- \(a\) is the constant term.

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data_json = '{"y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "x": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}'
data = json.loads(data_json)

#### Extracting y and x values
y = data['y']
x = data['x']
K = len(y)

#### Create the problem variable
problem = pulp.LpProblem("Quadratic_Curve_Fitting", pulp.LpMinimize)

#### Define decision variables
a = pulp.LpVariable("a", lowBound=None)
b = pulp.LpVariable("b", lowBound=None)
c = pulp.LpVariable("c", lowBound=None)
e_plus = [pulp.LpVariable(f"e_k_plus_{k}", lowBound=0) for k in range(K)]
e_minus = [pulp.LpVariable(f"e_k_minus_{k}", lowBound=0) for k in range(K)]

#### Objective function: Minimize the sum of absolute deviations
problem += pulp.lpSum(e_plus[k] + e_minus[k] for k in range(K))

#### Constraints
for k in range(K):
    problem += e_plus[k] - e_minus[k] == y[k] - (c * x[k]**2 + b * x[k] + a)

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


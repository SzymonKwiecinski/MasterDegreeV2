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
To solve the given problem, we need to fit a quadratic function to the data points while minimizing the sum of absolute deviations. This can be formulated as a linear programming problem. Let's define the objective and constraints for this LP model.

Given:
- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

We want to fit the curve \( y = c \cdot x^2 + b \cdot x + a \).

The objective is to minimize:
\[ \sum_{k=1}^{K} |y_k - (c \cdot x_k^2 + b \cdot x_k + a)| \]

This can be transformed into a linear programming problem by introducing auxiliary variables \( e_k^+ \) and \( e_k^- \) for the positive and negative deviations respectively. The objective then becomes:
\[ \min \sum_{k=1}^{K} (e_k^+ + e_k^-) \]

Subject to:
\[ y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^- \]
\[ e_k^+, e_k^- \geq 0 \]

This formulation ensures that we are minimizing the absolute deviations by using non-negative slack variables to represent deviations.

Here's the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Quadratic Fit}

\textbf{Objective:}
\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

\textbf{Subject to:}
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-, \quad \forall k = 1, 2, \ldots, K
\]
\[
e_k^+, e_k^- \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

Where:
- \( c \) is the coefficient of the quadratic term.
- \( b \) is the coefficient of the linear term.
- \( a \) is the constant term.
- \( e_k^+ \) and \( e_k^- \) are auxiliary variables representing deviations.

\end{document}
```

This linear programming formulation allows the quadratic function to be fitted to the data points by minimizing the sum of absolute deviations from the observed values. The solution will provide the values for the coefficients \( c, b, \) and \( a \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Quadratic Fit}

\textbf{Objective:}
\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

\textbf{Subject to:}
\[
y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-, \quad \forall k = 1, 2, \ldots, K
\]
\[
e_k^+, e_k^- \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

Where:
- \( c \) is the coefficient of the quadratic term.
- \( b \) is the coefficient of the linear term.
- \( a \) is the constant term.
- \( e_k^+ \) and \( e_k^- \) are auxiliary variables representing deviations.

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

#### Number of data points
K = len(data['y'])

#### Initialize the problem
problem = pulp.LpProblem("Quadratic_Fit", pulp.LpMinimize)

#### Decision Variables
c = pulp.LpVariable('c', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
a = pulp.LpVariable('a', lowBound=None)

e_plus = [pulp.LpVariable(f'e_plus_{k}', lowBound=0) for k in range(K)]
e_minus = [pulp.LpVariable(f'e_minus_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum([e_plus[k] + e_minus[k] for k in range(K)])

#### Constraints
for k in range(K):
    y_k = data['y'][k]
    x_k = data['x'][k]
    
    problem += y_k - (c * x_k**2 + b * x_k + a) == e_plus[k] - e_minus[k], f"error_constraint_{k}"

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


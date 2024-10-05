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
To solve this problem using Linear Programming, we need to formulate the problem to minimize the sum of absolute deviations between the observed values \( y_k \) and the predicted values given by the quadratic equation \( y = c \cdot x^2 + b \cdot x + a \).

We'll assume a linear programming approach using these steps:

1. Define variables:
   - \( c \): Coefficient of the quadratic term
   - \( b \): Coefficient of the linear term
   - \( a \): Constant term
   - \( e_k^+ \) and \( e_k^- \): Positive and negative deviations for each data point \( k \)

2. Objective Function:
   - Minimize the sum of absolute deviations: \( \sum_{k=1}^{K} (e_k^+ + e_k^-) \)

3. Constraints:
   - For each data point \( (x_k, y_k) \), the following constraints need to be established:
     - \( y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^- \)
     - \( e_k^+ \geq 0 \), \( e_k^- \geq 0 \)

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model}

\begin{align*}
\text{Minimize:} \quad & \sum_{k=1}^{K} (e_k^+ + e_k^-) \\
\text{Subject to:} \quad & y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-, \quad \forall k \\
& e_k^+ \geq 0, \quad e_k^- \geq 0, \quad \forall k
\end{align*}

\textbf{Where:}
\begin{itemize}
    \item \( c \) is the coefficient of the quadratic term.
    \item \( b \) is the coefficient of the linear term.
    \item \( a \) is the coefficient of the constant term.
    \item \( e_k^+ \) and \( e_k^- \) are non-negative variables representing the positive and negative deviations for data point \( k \).
\end{itemize}

\end{document}
```

This linear programming model can be solved using an LP solver to find the optimal values for \( c \), \( b \), and \( a \) that minimize the sum of absolute deviations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Mathematical Model}

\begin{align*}
\text{Minimize:} \quad & \sum_{k=1}^{K} (e_k^+ + e_k^-) \\
\text{Subject to:} \quad & y_k - (c \cdot x_k^2 + b \cdot x_k + a) = e_k^+ - e_k^-, \quad \forall k \\
& e_k^+ \geq 0, \quad e_k^- \geq 0, \quad \forall k
\end{align*}

\textbf{Where:}
\begin{itemize}
    \item \( c \) is the coefficient of the quadratic term.
    \item \( b \) is the coefficient of the linear term.
    \item \( a \) is the coefficient of the constant term.
    \item \( e_k^+ \) and \( e_k^- \) are non-negative variables representing the positive and negative deviations for data point \( k \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
        'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}

y = data['y']
x = data['x']
K = len(y)

#### Create a Linear Programming problem
problem = pulp.LpProblem("Quadratic_Fit_Error_Minimization", pulp.LpMinimize)

#### Decision Variables
e_plus = [pulp.LpVariable(f'e_plus_{k}', lowBound=0) for k in range(K)]
e_minus = [pulp.LpVariable(f'e_minus_{k}', lowBound=0) for k in range(K)]
c = pulp.LpVariable('c')
b = pulp.LpVariable('b')
a = pulp.LpVariable('a')

#### Objective Function
problem += pulp.lpSum([e_plus[k] + e_minus[k] for k in range(K)])

#### Constraints
for k in range(K):
    problem += y[k] - (c * x[k]**2 + b * x[k] + a) == e_plus[k] - e_minus[k]

#### Solve the problem
problem.solve()

#### Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


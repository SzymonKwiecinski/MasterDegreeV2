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
To solve this problem using linear programming, we need to fit a quadratic curve \(y = c \cdot x^2 + b \cdot x + a\) that minimizes the sum of absolute deviations between the observed and predicted values of \(y\). This can be formulated as a linear programming problem by introducing auxiliary variables to handle absolute values.

Let's set up the linear programming model:

######### Decision Variables
- \(a\): coefficient of the constant term.
- \(b\): coefficient of the linear term.
- \(c\): coefficient of the quadratic term.
- \(e_k^+\): positive deviation for each data point \(k\).
- \(e_k^-\): negative deviation for each data point \(k\).

######### Objective Function
Minimize the sum of deviations:
\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

######### Constraints
For each data point \(k\), the deviation between the observed and predicted value is given by:
\[
y_k = c \cdot x_k^2 + b \cdot x_k + a + e_k^+ - e_k^-
\]
Where:
- \(e_k^+ \geq 0\) and \(e_k^- \geq 0\).

These constraints ensure that \(e_k^+\) and \(e_k^-\) capture any positive or negative deviation, thus handling absolute values.

Now, the Linear Programming model in LaTeX format is given below:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

\textbf{Subject to:}

\[
y_k = c \cdot x_k^2 + b \cdot x_k + a + e_k^+ - e_k^-, \quad \forall k = 1, \ldots, K
\]

\[
e_k^+ \geq 0, \quad e_k^- \geq 0, \quad \forall k = 1, \ldots, K
\]

\textbf{Variables:}

\[
a, b, c, e_k^+, e_k^- \quad \text{(for } k = 1, \ldots, K\text{)}
\]

\end{document}
```

With this formulation, you can use any LP solver to find the values of \(a\), \(b\), and \(c\) that minimize the sum of absolute deviations, representing the coefficients for the quadratic, linear, and constant terms in the fitted quadratic curve.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\min \sum_{k=1}^{K} (e_k^+ + e_k^-)
\]

\textbf{Subject to:}

\[
y_k = c \cdot x_k^2 + b \cdot x_k + a + e_k^+ - e_k^-, \quad \forall k = 1, \ldots, K
\]

\[
e_k^+ \geq 0, \quad e_k^- \geq 0, \quad \forall k = 1, \ldots, K
\]

\textbf{Variables:}

\[
a, b, c, e_k^+, e_k^- \quad \text{(for } k = 1, \ldots, K\text{)}
\]

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

K = len(data['y'])
y = data['y']
x = data['x']

#### Create a LP Minimization problem
problem = pulp.LpProblem("Minimize_Error_Sum", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None)  #### a can be any real number
b = pulp.LpVariable('b', lowBound=None)  #### b can be any real number
c = pulp.LpVariable('c', lowBound=None)  #### c can be any real number
e_plus = pulp.LpVariable.dicts("e_plus", range(K), lowBound=0)
e_minus = pulp.LpVariable.dicts("e_minus", range(K), lowBound=0)

#### Objective Function
problem += pulp.lpSum([e_plus[k] + e_minus[k] for k in range(K)])

#### Constraints
for k in range(K):
    problem += y[k] == c * x[k]**2 + b * x[k] + a + e_plus[k] - e_minus[k], f"constraint_{k}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


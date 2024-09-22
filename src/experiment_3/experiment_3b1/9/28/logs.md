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


OBJECTIVE: Fit the ‘best’ straight line y = bx + a to this set of data points. The objective is to minimise the sum of absolute deviations of each observed value of y from the value predicted by the linear relationship.

OUTPUT INFO:

- \var{intercept} represents the intercept of the fitted line
- \var{slope} represents the slope of the fitted line

OUTPUT FORMAT:

{
    "intercept": intercept,
    "slope": slope
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Fitting a Line}

We want to fit the best straight line \( y = bx + a \) to a given dataset consisting of pairs \( (x_k, y_k) \) for \( k = 1, \ldots, K \).

\subsection*{Data}
Let:
\[
y = [y_{1}, y_{2}, \ldots, y_{K}]
\]
\[
x = [x_{1}, x_{2}, \ldots, x_{K}]
\]

\subsection*{Objective}
The objective is to minimize the sum of absolute deviations:
\[
\text{Minimize } Z = \sum_{k=1}^{K} |y_{k} - (bx_{k} + a)|
\]

We introduce auxiliary variables \( d_k \) for each \( k \) to handle the absolute values:
\[
d_k \geq y_{k} - (bx_{k} + a) \quad \forall k
\]
\[
d_k \geq -(y_{k} - (bx_{k} + a)) \quad \forall k
\]

Thus, we can reformulate the objective function to minimize:
\[
Z = \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
We have the following constraints:
\[
y_k - bx_k - a \leq d_k \quad \forall k
\]
\[
-(y_k - bx_k - a) \leq d_k \quad \forall k
\]
which can be simplified to:
\[
bx_k + a + d_k \geq y_k \quad \forall k
\]
\[
bx_k + a - d_k \leq y_k \quad \forall k
\]

\subsection*{Variables}
The decision variables are:
- \( a \): the intercept of the fitted line.
- \( b \): the slope of the fitted line.
- \( d_k \): the absolute deviation for each \( k \).

\subsection*{Final Linear Programming Formulation}
The complete linear programming model can be formulated as:
\[
\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^{K} d_k \\
\text{subject to: } & bx_k + a + d_k \geq y_k \quad \forall k \\
& bx_k + a - d_k \leq y_k \quad \forall k \\
& d_k \geq 0 \quad \forall k \\
& a \text{ is unrestricted} \\
& b \text{ is unrestricted}
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

\section*{Linear Programming Model for Fitting a Line}

We want to fit the best straight line \( y = bx + a \) to a given dataset consisting of pairs \( (x_k, y_k) \) for \( k = 1, \ldots, K \).

\subsection*{Data}
Let:
\[
y = [y_{1}, y_{2}, \ldots, y_{K}]
\]
\[
x = [x_{1}, x_{2}, \ldots, x_{K}]
\]

\subsection*{Objective}
The objective is to minimize the sum of absolute deviations:
\[
\text{Minimize } Z = \sum_{k=1}^{K} |y_{k} - (bx_{k} + a)|
\]

We introduce auxiliary variables \( d_k \) for each \( k \) to handle the absolute values:
\[
d_k \geq y_{k} - (bx_{k} + a) \quad \forall k
\]
\[
d_k \geq -(y_{k} - (bx_{k} + a)) \quad \forall k
\]

Thus, we can reformulate the objective function to minimize:
\[
Z = \sum_{k=1}^{K} d_k
\]

\subsection*{Constraints}
We have the following constraints:
\[
y_k - bx_k - a \leq d_k \quad \forall k
\]
\[
-(y_k - bx_k - a) \leq d_k \quad \forall k
\]
which can be simplified to:
\[
bx_k + a + d_k \geq y_k \quad \forall k
\]
\[
bx_k + a - d_k \leq y_k \quad \forall k
\]

\subsection*{Variables}
The decision variables are:
- \( a \): the intercept of the fitted line.
- \( b \): the slope of the fitted line.
- \( d_k \): the absolute deviation for each \( k \).

\subsection*{Final Linear Programming Formulation}
The complete linear programming model can be formulated as:
\[
\begin{align*}
\text{Minimize } & Z = \sum_{k=1}^{K} d_k \\
\text{subject to: } & bx_k + a + d_k \geq y_k \quad \forall k \\
& bx_k + a - d_k \leq y_k \quad \forall k \\
& d_k \geq 0 \quad \forall k \\
& a \text{ is unrestricted} \\
& b \text{ is unrestricted}
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"K": 19, "Y": [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], "X": [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}')

K = data['K']
Y = data['Y']
X = data['X']

#### Create the optimization problem
problem = pulp.LpProblem("FitLine", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable('a', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
d = [pulp.LpVariable(f'd_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(d[k] for k in range(K)), "Total_Absolute_Deviation"

#### Constraints
for k in range(K):
    problem += (b * X[k] + a + d[k] >= Y[k]), f"Upper_Bound_Constraint_{k}"
    problem += (b * X[k] + a - d[k] <= Y[k]), f"Lower_Bound_Constraint_{k}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


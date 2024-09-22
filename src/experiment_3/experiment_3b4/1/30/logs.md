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
To solve this problem, we need to fit a quadratic curve \( y = cx^2 + bx + a \) to the given data points by minimizing the sum of the absolute deviations of each observed value of \( y \) from the predicted value. This can be formulated as a Linear Programming problem.

######### Problem Formulation

To formulate this as a linear programming problem, let's denote:
- \( y_k \) as the observed value of \( y \) for the \( k \)-th data point.
- \( x_k \) as the observed value of \( x \) for the \( k \)-th data point.
- \( \hat{y}_k = c x_k^2 + b x_k + a \) as the predicted value of \( y \) for the \( k \)-th data point.

The objective is to minimize the sum of absolute deviations \(\sum_{k=1}^{K} |y_k - \hat{y}_k|\).

We can introduce auxiliary variables \( z_k \) to represent the absolute deviation, i.e., \( z_k = |y_k - \hat{y}_k| \).

Thus, the linear programming problem can be written as:

########## Objective:
\[
\text{Minimize } \sum_{k=1}^{K} z_k
\]

########## Subject to:
\[
y_k - (c x_k^2 + b x_k + a) \leq z_k \quad \text{for all } k
\]
\[
(c x_k^2 + b x_k + a) - y_k \leq z_k \quad \text{for all } k
\]

######### Linear Programming Model in LaTeX

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize } \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}
\[
y_k - (c x_k^2 + b x_k + a) \leq z_k \quad \text{for all } k
\]
\[
(c x_k^2 + b x_k + a) - y_k \leq z_k \quad \text{for all } k
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( c \): coefficient of the quadratic term
    \item \( b \): coefficient of the linear term
    \item \( a \): constant coefficient
    \item \( z_k \): auxiliary variable representing the absolute deviation for each data point
\end{itemize}

\end{document}
```

This LP problem can be solved using any LP solver to obtain the values of \(c\), \(b\), and \(a\) which minimize the sum of absolute deviations, fitting the best quadratic curve to the data.

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
\text{Minimize } \sum_{k=1}^{K} z_k
\]

\textbf{Subject to:}
\[
y_k - (c x_k^2 + b x_k + a) \leq z_k \quad \text{for all } k
\]
\[
(c x_k^2 + b x_k + a) - y_k \leq z_k \quad \text{for all } k
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( c \): coefficient of the quadratic term
    \item \( b \): coefficient of the linear term
    \item \( a \): constant coefficient
    \item \( z_k \): auxiliary variable representing the absolute deviation for each data point
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from JSON-like input
data = {
    'y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'x': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Initialize the linear programming problem
problem = pulp.LpProblem("Quadratic_Regression", pulp.LpMinimize)

#### Number of data points
K = len(data['x'])

#### Decision Variables
c = pulp.LpVariable('c', cat='Continuous')
b = pulp.LpVariable('b', cat='Continuous')
a = pulp.LpVariable('a', cat='Continuous')
z = [pulp.LpVariable(f'z_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(z), "Minimize Sum of Absolute Deviation"

#### Constraints
for k in range(K):
    x_k = data['x'][k]
    y_k = data['y'][k]
    
    #### |y_k - (c*x_k^2 + b*x_k + a)| <= z_k
    problem += y_k - (c*x_k**2 + b*x_k + a) <= z[k]
    problem += (c*x_k**2 + b*x_k + a) - y_k <= z[k]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


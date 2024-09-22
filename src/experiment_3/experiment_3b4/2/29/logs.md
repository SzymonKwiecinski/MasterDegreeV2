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


OBJECTIVE: Fit the ‘best’ straight line y = bx + a where the objective is to minimize the maximum deviation of all the observed values of y from the value predicted by the linear relationship.

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
To solve this problem using Linear Programming, we aim to find the line \( y = bx + a \) that minimizes the maximum deviation between observed values \( y_k \) and predicted values \( \hat{y}_k \) (where \( \hat{y}_k = bx_k + a \)).

The linear programming model can be formulated as follows:

Objective: Minimize the maximum deviation \( d \).

Subject to:

\[ 
d \geq y_k - (bx_k + a) \quad \text{for each } k
\]
\[ 
d \geq (bx_k + a) - y_k \quad \text{for each } k
\]

The decision variables are \( a \), \( b \), and \( d \). The constraints ensure that \( d \) represents the maximum deviation between observed and predicted values.

Here's the corresponding LaTeX code for the mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize } d
\]

\textbf{Subject to the constraints:}
\[
d \geq y_k - (bx_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
d \geq (bx_k + a) - y_k \quad \text{for } k = 1, \ldots, K
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( a \): Intercept of the fitted line
    \item \( b \): Slope of the fitted line
    \item \( d \): Maximum deviation
\end{itemize}

\end{document}
```

This formulation captures the essence of minimizing the maximum absolute deviation which is a classic use-case for linear programming. The solution to this problem will yield the intercept \( a \) and the slope \( b \) of the line that best fits the data in the sense of minimizing the maximum deviation.

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
\text{Minimize } d
\]

\textbf{Subject to the constraints:}
\[
d \geq y_k - (bx_k + a) \quad \text{for } k = 1, \ldots, K
\]
\[
d \geq (bx_k + a) - y_k \quad \text{for } k = 1, \ldots, K
\]

\textbf{Decision Variables:}
\begin{itemize}
    \item \( a \): Intercept of the fitted line
    \item \( b \): Slope of the fitted line
    \item \( d \): Maximum deviation
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Max_Deviation", pulp.LpMinimize)

#### Decision variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')
d = pulp.LpVariable('d', lowBound=0, upBound=None, cat='Continuous')

#### Objective function
problem += d, "Minimize maximum deviation"

#### Constraints
for k in range(data['NumObs']):
    xk = data['X'][k]
    yk = data['Y'][k]
    problem += d >= yk - (b * xk + a), f"Constraint_upper_bound_{k}"
    problem += d >= (b * xk + a) - yk, f"Constraint_lower_bound_{k}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


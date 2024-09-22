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
To solve this problem, we need to fit a line \( y = bx + a \) to the given data points such that the sum of absolute deviations is minimized. This is a linear programming problem.

Given:
- \( y = [y_1, y_2, \ldots, y_K] \)
- \( x = [x_1, x_2, \ldots, x_K] \)

Objective:
- Minimize: \(\sum_{k=1}^{K} |y_k - (bx_k + a)|\)

This can be modeled using the linear programming by introducing non-negative deviation variables \( u_k \) and \( v_k \) for each data point, and minimizing their sum, where \( u_k \) and \( v_k \) represent the positive and negative deviations respectively.

Let's write the linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation:}

Given data points \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \).

\textbf{Objective:}
\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

\textbf{Subject to:}
\[
y_k = bx_k + a + u_k - v_k, \quad \forall k = 1, 2, \ldots, K
\]
\[
u_k \geq 0, \quad v_k \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\textbf{Variables:}
- \( a \): Intercept of the line
- \( b \): Slope of the line
- \( u_k, v_k \): Non-negative deviation variables for each data point

\end{document}
```

This linear program can be solved using an LP solver, and it will provide the values of \( a \) and \( b \) which are the intercept and slope of the best fit line, respectively. The sum of the variables \( u_k \) and \( v_k \) captures the absolute deviations from each data point to the fitted line.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation:}

Given data points \( (x_k, y_k) \) for \( k = 1, 2, \ldots, K \).

\textbf{Objective:}
\[
\min \sum_{k=1}^{K} (u_k + v_k)
\]

\textbf{Subject to:}
\[
y_k = bx_k + a + u_k - v_k, \quad \forall k = 1, 2, \ldots, K
\]
\[
u_k \geq 0, \quad v_k \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\textbf{Variables:}
- \( a \): Intercept of the line
- \( b \): Slope of the line
- \( u_k, v_k \): Non-negative deviation variables for each data point

\end{document}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Problem
problem = pulp.LpProblem("Best_Fit_Line", pulp.LpMinimize)

#### Variables
a = pulp.LpVariable('a', lowBound=None, upBound=None, cat='Continuous')  #### Intercept
b = pulp.LpVariable('b', lowBound=None, upBound=None, cat='Continuous')  #### Slope

u_vars = [pulp.LpVariable(f'u_{k}', lowBound=0, cat='Continuous') for k in range(data['K'])]
v_vars = [pulp.LpVariable(f'v_{k}', lowBound=0, cat='Continuous') for k in range(data['K'])]

#### Objective function
problem += pulp.lpSum([u_vars[k] + v_vars[k] for k in range(data['K'])])

#### Constraints
for k in range(data['K']):
    problem += data['Y'][k] == b * data['X'][k] + a + u_vars[k] - v_vars[k]

#### Solve the problem
problem.solve()

#### Print the results
print(f'Optimal value of a (Intercept): {pulp.value(a)}')
print(f'Optimal value of b (Slope): {pulp.value(b)}')
print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


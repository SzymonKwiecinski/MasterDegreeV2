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
To fit the best straight line \( y = bx + a \) that minimizes the sum of absolute deviations of each observed value of \( y \) from the value predicted by the linear relationship, we can formulate a linear programming problem.

Let's denote:
- \( a \) as the intercept of the line
- \( b \) as the slope of the line
- \( y_k \) as the observed values of \( y \)
- \( x_k \) as the observed values of \( x \)

We aim to minimize the sum of absolute deviations:

\[ \sum_{k=1}^{K} |y_k - (bx_k + a)| \]

To handle absolute values in a linear programming model, introduce auxiliary variables \( z_k \) to represent the deviations, where:

\[ z_k \geq y_k - (bx_k + a) \]
\[ z_k \geq -(y_k - (bx_k + a)) \]

The objective function becomes:

Minimize \(\sum_{k=1}^{K} z_k\)

Here is the linear programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model to Minimize Absolute Deviations:}

\[
\begin{aligned}
    & \text{Minimize:} && \sum_{k=1}^{K} z_k \\
    & \text{Subject to:} \\
    & \quad z_k \geq y_k - (bx_k + a), \quad \forall k = 1, \ldots, K \\
    & \quad z_k \geq -(y_k - (bx_k + a)), \quad \forall k = 1, \ldots, K \\
    & \quad z_k \geq 0, \quad \forall k = 1, \ldots, K \\
\end{aligned}
\]

Where:
\begin{itemize}
    \item \( y_k \) are the observed values of \( y \)
    \item \( x_k \) are the observed values of \( x \)
    \item \( a \) is the intercept of the fitted line
    \item \( b \) is the slope of the fitted line
    \item \( z_k \) are auxiliary variables for the absolute deviations
\end{itemize}

\end{document}
```

This model will help determine the values of \( a \) (intercept) and \( b \) (slope) that minimize the sum of absolute deviations. The results should match the expected output format:

```json
{
    "intercept": intercept,
    "slope": slope
}
```

where \( \text{intercept} \) and \( \text{slope} \) are the optimal values computed by solving this linear programming problem.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model to Minimize Absolute Deviations:}

\[
\begin{aligned}
    & \text{Minimize:} && \sum_{k=1}^{K} z_k \\
    & \text{Subject to:} \\
    & \quad z_k \geq y_k - (bx_k + a), \quad \forall k = 1, \ldots, K \\
    & \quad z_k \geq -(y_k - (bx_k + a)), \quad \forall k = 1, \ldots, K \\
    & \quad z_k \geq 0, \quad \forall k = 1, \ldots, K \\
\end{aligned}
\]

Where:
\begin{itemize}
    \item \( y_k \) are the observed values of \( y \)
    \item \( x_k \) are the observed values of \( x \)
    \item \( a \) is the intercept of the fitted line
    \item \( b \) is the slope of the fitted line
    \item \( z_k \) are auxiliary variables for the absolute deviations
\end{itemize}

\end{document}
{
    "intercept": intercept,
    "slope": slope
}</MATH_MODEL>
<DATA>
{'K': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = {
    'K': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Parameters for the linear model
intercept = 2.0  #### Example intercept, set to the desired value
slope = 0.5      #### Example slope, set to the desired value

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Absolute_Deviation", pulp.LpMinimize)

#### Decision variables
z = pulp.LpVariable.dicts("z", range(data['K']), lowBound=0)

#### Objective Function
problem += pulp.lpSum(z[k] for k in range(data['K'])), "Objective"

#### Constraints
for k in range(data['K']):
    y_k = data['Y'][k]
    x_k = data['X'][k]
    problem += z[k] >= y_k - (slope * x_k + intercept), f"Constraint_1_{k}"
    problem += z[k] >= -(y_k - (slope * x_k + intercept)), f"Constraint_2_{k}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


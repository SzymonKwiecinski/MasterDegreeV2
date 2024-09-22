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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Line Fitting}

Given a set of observed values of \( y \) and corresponding values of \( x \), we aim to find the best fitting line of the form:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope. 

Let the observed values be defined as follows:

\[
\begin{align*}
y_k & \text{ for } k = 1, \ldots, K \\
x_k & \text{ for } k = 1, \ldots, K
\end{align*}
\]

We define the deviations from the predicted values as:

\[
d_k = y_k - (bx_k + a) \quad \text{for } k = 1, \ldots, K
\]

Our objective is to minimize the maximum deviation, which can be formulated as:

\[
\min \quad t
\]

subject to the constraints:

\[
\begin{align*}
y_k - (bx_k + a) & \leq t \quad \text{for } k = 1, \ldots, K \\
-(y_k - (bx_k + a)) & \leq t \quad \text{for } k = 1, \ldots, K \\
t & \geq 0
\end{align*}
\]

The above constraints ensure that \( t \) is at least as large as the maximum positive and negative deviations.

Thus, the complete formulation in a linear programming format is:

\[
\begin{align*}
\text{Minimize} \quad & t \\
\text{subject to} \quad & y_k - bx_k - a \leq t, \quad k = 1, \ldots, K \\
& -y_k + bx_k + a \leq t, \quad k = 1, \ldots, K \\
& t \geq 0
\end{align*}
\]

\textbf{Output:} The optimal values of \( a \) (intercept) and \( b \) (slope) will give us the best fitting line that minimizes the maximum deviation from the observed values.

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

\section*{Linear Programming Model for Line Fitting}

Given a set of observed values of \( y \) and corresponding values of \( x \), we aim to find the best fitting line of the form:

\[
y = bx + a
\]

where \( a \) is the intercept and \( b \) is the slope. 

Let the observed values be defined as follows:

\[
\begin{align*}
y_k & \text{ for } k = 1, \ldots, K \\
x_k & \text{ for } k = 1, \ldots, K
\end{align*}
\]

We define the deviations from the predicted values as:

\[
d_k = y_k - (bx_k + a) \quad \text{for } k = 1, \ldots, K
\]

Our objective is to minimize the maximum deviation, which can be formulated as:

\[
\min \quad t
\]

subject to the constraints:

\[
\begin{align*}
y_k - (bx_k + a) & \leq t \quad \text{for } k = 1, \ldots, K \\
-(y_k - (bx_k + a)) & \leq t \quad \text{for } k = 1, \ldots, K \\
t & \geq 0
\end{align*}
\]

The above constraints ensure that \( t \) is at least as large as the maximum positive and negative deviations.

Thus, the complete formulation in a linear programming format is:

\[
\begin{align*}
\text{Minimize} \quad & t \\
\text{subject to} \quad & y_k - bx_k - a \leq t, \quad k = 1, \ldots, K \\
& -y_k + bx_k + a \leq t, \quad k = 1, \ldots, K \\
& t \geq 0
\end{align*}
\]

\textbf{Output:} The optimal values of \( a \) (intercept) and \( b \) (slope) will give us the best fitting line that minimizes the maximum deviation from the observed values.

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define the problem
problem = pulp.LpProblem("Line_Fitting_Min_Max_Deviation", pulp.LpMinimize)

#### Define the variables
a = pulp.LpVariable('a', lowBound=None)
b = pulp.LpVariable('b', lowBound=None)
t = pulp.LpVariable('t', lowBound=0)

#### Data
data = {
    'NumObs': 19,
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3],
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Extract data values
num_obs = data['NumObs']
Y = data['Y']
X = data['X']

#### Define the objective function
problem += t, "Minimize_Max_Deviation"

#### Add constraints
for k in range(num_obs):
    y_k = Y[k]
    x_k = X[k]
    
    #### y_k - (b * x_k + a) <= t
    problem += y_k - (b * x_k + a) <= t, f"Constraint_Pos_{k}"
    
    #### -(y_k - (b * x_k + a)) <= t --> -y_k + (b * x_k + a) <= t
    problem += -y_k + (b * x_k + a) <= t, f"Constraint_Neg_{k}"

#### Solve the problem
problem.solve()

#### Print the results
print(f"Optimal Intercept (a): {pulp.value(a)}")
print(f"Optimal Slope (b): {pulp.value(b)} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```


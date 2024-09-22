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

\section*{Linear Programming Model for Fitting a Line}

Given a set of observed values for \( y \) and \( x \):

\[
\begin{aligned}
y & = [y_1, y_2, \ldots, y_K] \\
x & = [x_1, x_2, \ldots, x_K]
\end{aligned}
\]

We aim to fit the best straight line of the form:

\[
y = bx + a
\]

where we want to minimize the maximum deviation of the observed values of \( y \) from the predicted values given by the linear relationship.

Let \( d_k \) be the deviation for each observation, defined as:

\[
d_k = y_k - (bx_k + a)
\]

Thus, we want to minimize the maximum absolute deviation:

\[
\min \max_{k=1,2,\ldots,K} |d_k|
\]

This can be transformed into a linear programming problem. Define \( M \) as the maximum deviation:

\[
\text{subject to:} \\
d_k \leq M, \quad \forall k \\
-d_k \leq M, \quad \forall k
\]

The complete linear programming formulation is:

\[
\begin{aligned}
\text{Minimize} \quad & M \\
\text{subject to} \quad & y_k - (bx_k + a) \leq M, \quad \forall k \\
& -(y_k - (bx_k + a)) \leq M, \quad \forall k \\
& b \text{ and } a \text{ free variables}
\end{aligned}
\]

The output of this linear programming formulation will provide us with the values for:

\[
\begin{aligned}
\text{intercept} & = a \\
\text{slope} & = b
\end{aligned}
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

Given a set of observed values for \( y \) and \( x \):

\[
\begin{aligned}
y & = [y_1, y_2, \ldots, y_K] \\
x & = [x_1, x_2, \ldots, x_K]
\end{aligned}
\]

We aim to fit the best straight line of the form:

\[
y = bx + a
\]

where we want to minimize the maximum deviation of the observed values of \( y \) from the predicted values given by the linear relationship.

Let \( d_k \) be the deviation for each observation, defined as:

\[
d_k = y_k - (bx_k + a)
\]

Thus, we want to minimize the maximum absolute deviation:

\[
\min \max_{k=1,2,\ldots,K} |d_k|
\]

This can be transformed into a linear programming problem. Define \( M \) as the maximum deviation:

\[
\text{subject to:} \\
d_k \leq M, \quad \forall k \\
-d_k \leq M, \quad \forall k
\]

The complete linear programming formulation is:

\[
\begin{aligned}
\text{Minimize} \quad & M \\
\text{subject to} \quad & y_k - (bx_k + a) \leq M, \quad \forall k \\
& -(y_k - (bx_k + a)) \leq M, \quad \forall k \\
& b \text{ and } a \text{ free variables}
\end{aligned}
\]

The output of this linear programming formulation will provide us with the values for:

\[
\begin{aligned}
\text{intercept} & = a \\
\text{slope} & = b
\end{aligned}
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumObs': 19, 'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumObs': 19, 
    'Y': [1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5, 1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3], 
    'X': [0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0]
}

#### Extract data
num_obs = data['NumObs']
y = data['Y']
x = data['X']

#### Initialize the Linear Programming problem
problem = pulp.LpProblem("Minimize_Max_Absolute_Deviation", pulp.LpMinimize)

#### Decision Variables
b = pulp.LpVariable("b", cat='Continuous')  #### slope
a = pulp.LpVariable("a", cat='Continuous')  #### intercept
M = pulp.LpVariable("M", lowBound=0, cat='Continuous')  #### max deviation

#### Define the objective function to minimize M
problem += M

#### Add the constraints for each observation
for k in range(num_obs):
    d_k = y[k] - (b * x[k] + a)
    problem += d_k <= M  #### y_k - (bx_k + a) <= M
    problem += -d_k <= M  #### -(y_k - (bx_k + a)) <= M

#### Solve the problem
problem.solve()

#### Output the results
print(f'Slope (b): {pulp.value(b)}')
print(f'Intercept (a): {pulp.value(a)}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

